#!/usr/bin/env python3
"""Fetch every article from Tao Tan's Google Scholar profile via SerpApi.

The API key is read only from SERPAPI_API_KEY. Successful page responses are
cached under raw/<run-id>/ so interrupted runs can resume without re-fetching
completed pages. Published JSON/CSV/report files are replaced only after a
complete, validated crawl.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ENDPOINT = "https://serpapi.com/search"
AUTHOR_ID = "lLg3WRkAAAAJ"
PAGE_SIZE = 100
FIELDS = (
    "title",
    "authors",
    "year",
    "publication",
    "citation_count",
    "link",
    "citation_id",
    "data_acquired_at",
)
CSV_FIELDS = FIELDS + ("source_page_start", "review_flags", "duplicate_reason", "duplicate_of")


class CollectionError(RuntimeError):
    """A safe-to-display collection error that never includes request secrets."""


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def atomic_write_json(path: Path, value: Any) -> None:
    atomic_write(path, json_bytes(value))


def sanitize_value(value: Any, secret: str) -> Any:
    """Remove credentials from API payloads before they can reach disk."""
    if isinstance(value, dict):
        return {
            key: sanitize_value(item, secret)
            for key, item in value.items()
            if str(key).lower() not in {"api_key", "apikey"}
        }
    if isinstance(value, list):
        return [sanitize_value(item, secret) for item in value]
    if isinstance(value, str):
        safe = value.replace(secret, "[REDACTED]") if secret else value
        return re.sub(r"(?i)(api[_-]?key\s*[=:]\s*)[^&\s,]+", r"\1[REDACTED]", safe)
    return value


def safe_error(error: BaseException, secret: str) -> str:
    text = str(error)
    if secret:
        text = text.replace(secret, "[REDACTED]")
    return re.sub(r"(?i)(api[_-]?key\s*[=:]\s*)[^&\s,]+", r"\1[REDACTED]", text)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def list_run_states(raw_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    states = []
    if not raw_dir.exists():
        return states
    for path in raw_dir.glob("*/run-state.json"):
        try:
            state = read_json(path)
            if isinstance(state, dict) and state.get("run_id") == path.parent.name:
                states.append((path, state))
        except (OSError, json.JSONDecodeError):
            continue
    return sorted(states, key=lambda item: item[1].get("started_at", ""), reverse=True)


def new_state(run_id: str) -> dict[str, Any]:
    now = iso_now()
    return {
        "run_id": run_id,
        "author_id": AUTHOR_ID,
        "started_at": now,
        "updated_at": now,
        "status": "in_progress",
        "pages": {},
        "request_attempts": 0,
        "last_error": "",
    }


def save_state(state_path: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = iso_now()
    atomic_write_json(state_path, state)


def choose_run(raw_dir: Path, resume_arg: str | None, new_run: bool) -> tuple[Path, dict[str, Any]]:
    states = list_run_states(raw_dir)
    if resume_arg:
        if resume_arg == "latest":
            selected = next(
                ((path, state) for path, state in states if state.get("status") in {"in_progress", "failed", "ready_to_publish"}),
                None,
            )
        else:
            selected = next(((path, state) for path, state in states if state["run_id"] == resume_arg), None)
        if selected is None:
            raise CollectionError(f"No incomplete run found for resume request: {resume_arg}")
        path, state = selected
        if state.get("status") == "published":
            raise CollectionError(f"Run {state['run_id']} is already published")
        return path, state

    if not new_run:
        selected = next(
            ((path, state) for path, state in states if state.get("status") in {"in_progress", "failed", "ready_to_publish"}),
            None,
        )
        if selected:
            return selected

    run_id = utc_now().strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex[:8]
    run_dir = raw_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    state = new_state(run_id)
    state_path = run_dir / "run-state.json"
    save_state(state_path, state)
    return state_path, state


def read_cached_page(run_dir: Path, start: int) -> dict[str, Any] | None:
    page_path = run_dir / f"page-{start:06d}.json"
    if not page_path.exists():
        return None
    try:
        data = read_json(page_path)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or data.get("search_metadata", {}).get("status") != "Success":
        return None
    if data.get("search_parameters", {}).get("author_id") != AUTHOR_ID:
        return None
    return data


def request_page(api_key: str, start: int, timeout: float, retries: int, state: dict[str, Any], max_requests: int) -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {
            "engine": "google_scholar_author",
            "author_id": AUTHOR_ID,
            "hl": "en",
            "num": PAGE_SIZE,
            "start": start,
            "api_key": api_key,
        }
    )
    request = urllib.request.Request(
        f"{ENDPOINT}?{query}",
        headers={"Accept": "application/json", "User-Agent": "Gem-Web-publication-collector/1.0"},
    )
    last_error: BaseException | None = None
    for attempt in range(retries + 1):
        if max_requests and state["request_attempts"] >= max_requests:
            raise CollectionError(
                f"API request limit reached ({max_requests}); saved pages are cached and the run can resume later."
            )
        state["request_attempts"] += 1
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = response.read()
            data = json.loads(payload.decode("utf-8"))
            if not isinstance(data, dict):
                raise CollectionError("SerpApi returned a JSON value that is not an object")
            status = data.get("search_metadata", {}).get("status")
            if status != "Success":
                message = data.get("error") or f"unexpected search status: {status or 'missing'}"
                raise CollectionError(str(message))
            if not isinstance(data.get("articles"), list):
                raise CollectionError("SerpApi response is missing its articles array")
            return data
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code == 429 or 400 <= error.code < 500:
                raise CollectionError(f"SerpApi HTTP {error.code}; check API access, quota, and request parameters.") from None
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, CollectionError) as error:
            last_error = error
            if isinstance(error, CollectionError):
                raise
        if attempt < retries:
            time.sleep(min(2**attempt, 8))
    message = safe_error(last_error or RuntimeError("unknown request failure"), api_key)
    raise CollectionError(f"Page at start={start} failed after {retries + 1} attempt(s): {message}")


def next_offset(data: dict[str, Any], start: int, count: int) -> int | None:
    next_url = data.get("serpapi_pagination", {}).get("next")
    if next_url:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(next_url).query)
        for key in ("start", "cstart"):
            if query.get(key):
                try:
                    candidate = int(query[key][0])
                    if candidate > start:
                        return candidate
                except (ValueError, TypeError):
                    pass
    if count >= PAGE_SIZE:
        return start + PAGE_SIZE
    return None


def fetch_all(
    api_key: str,
    state_path: Path,
    state: dict[str, Any],
    timeout: float,
    retries: int,
    max_requests: int,
) -> list[tuple[int, str, dict[str, Any]]]:
    run_dir = state_path.parent
    pages: list[tuple[int, str, dict[str, Any]]] = []
    start = 0
    visited: set[int] = set()
    while True:
        if start in visited:
            raise CollectionError(f"Pagination loop detected at start={start}")
        visited.add(start)
        data = read_cached_page(run_dir, start)
        acquired_at = state.get("pages", {}).get(str(start), {}).get("data_acquired_at", "")
        if data is None:
            print(f"[INFO] Fetching page start={start} (num={PAGE_SIZE})", flush=True)
            data = request_page(api_key, start, timeout, retries, state, max_requests)
            data = sanitize_value(data, api_key)
            acquired_at = iso_now()
            atomic_write_json(run_dir / f"page-{start:06d}.json", data)
            state["pages"][str(start)] = {
                "article_count": len(data.get("articles", [])),
                "data_acquired_at": acquired_at,
            }
            state["last_error"] = ""
            save_state(state_path, state)
        else:
            if not acquired_at:
                acquired_at = dt.datetime.fromtimestamp(
                    (run_dir / f"page-{start:06d}.json").stat().st_mtime, dt.timezone.utc
                ).replace(microsecond=0).isoformat().replace("+00:00", "Z")
                state["pages"][str(start)] = {"article_count": len(data.get("articles", [])), "data_acquired_at": acquired_at}
                save_state(state_path, state)
            print(f"[INFO] Using cached page start={start} ({len(data.get('articles', []))} articles)", flush=True)

        articles = data.get("articles", [])
        pages.append((start, acquired_at, data))
        following = next_offset(data, start, len(articles))
        if following is None:
            break
        start = following
    return pages


def citation_value(article: dict[str, Any]) -> Any:
    cited_by = article.get("cited_by")
    if isinstance(cited_by, dict):
        value = cited_by.get("value", "")
        return "" if value is None else value
    return ""


def normalize_article(article: Any, acquired_at: str, page_start: int) -> dict[str, Any]:
    article = article if isinstance(article, dict) else {}
    year = article.get("year", "")
    citations = citation_value(article)
    normalized = {
        "title": article.get("title") or "",
        "authors": article.get("authors") or "",
        "year": year if year is not None else "",
        "publication": article.get("publication") or "",
        "citation_count": citations,
        "link": article.get("link") or "",
        "citation_id": article.get("citation_id") or "",
        "data_acquired_at": acquired_at,
        "source_page_start": page_start,
        "review_flags": [],
        "duplicate_reason": "",
        "duplicate_of": "",
    }
    return normalized


def title_key(title: Any) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", str(title or "").lower()))


def build_records(pages: list[tuple[int, str, dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    publications: list[dict[str, Any]] = []
    duplicate_records: list[dict[str, Any]] = []
    csv_rows: list[dict[str, Any]] = []
    by_citation: dict[str, dict[str, Any]] = {}
    by_title_year: dict[tuple[str, str], dict[str, Any]] = {}

    for page_start, acquired_at, page in pages:
        for article in page.get("articles", []):
            record = normalize_article(article, acquired_at, page_start)
            citation_id = str(record["citation_id"]).strip()
            title = title_key(record["title"])
            year = str(record["year"]).strip()
            title_year = (title, year) if title and year else None

            existing_citation = by_citation.get(citation_id) if citation_id else None
            if existing_citation is not None:
                record["duplicate_reason"] = "duplicate_citation_id"
                record["duplicate_of"] = citation_id
                existing_citation["review_flags"] = sorted(set(existing_citation["review_flags"] + ["duplicate_citation_id"]))
                duplicate_records.append(dict(record))
                csv_rows.append(dict(record))
                continue

            similar = by_title_year.get(title_year) if title_year else None
            if similar is not None and str(similar.get("citation_id", "")) != citation_id:
                record["review_flags"].append("possible_title_year_duplicate")
                record["duplicate_reason"] = "possible_title_year_duplicate"
                record["duplicate_of"] = similar.get("citation_id", "")
                similar["review_flags"] = sorted(set(similar["review_flags"] + ["possible_title_year_duplicate"]))
                duplicate_records.append(dict(record))

            publications.append(record)
            csv_rows.append(dict(record))
            if citation_id:
                by_citation[citation_id] = record
            if title_year and title_year not in by_title_year:
                by_title_year[title_year] = record

    return publications, duplicate_records, csv_rows


def missing_counts(publications: list[dict[str, Any]]) -> dict[str, int]:
    data_fields = FIELDS[:-1]
    result = {}
    for field in data_fields:
        result[field] = sum(1 for record in publications if record.get(field) in (None, ""))
    return result


def load_previous(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = read_json(path)
    except (OSError, json.JSONDecodeError) as error:
        raise CollectionError(f"Cannot read previous publications snapshot: {error}") from None
    records = data.get("publications") if isinstance(data, dict) else None
    if not isinstance(records, list):
        raise CollectionError("Previous publications snapshot has an unexpected format")
    return records


def compare_snapshots(previous: list[dict[str, Any]], current: list[dict[str, Any]]) -> dict[str, Any]:
    old_by_id = {str(item.get("citation_id")): item for item in previous if item.get("citation_id")}
    new_by_id = {str(item.get("citation_id")): item for item in current if item.get("citation_id")}
    added = [item for key, item in new_by_id.items() if key not in old_by_id]
    removed = [item for key, item in old_by_id.items() if key not in new_by_id]
    changed = []
    for key, item in new_by_id.items():
        before = old_by_id.get(key)
        if before is None:
            continue
        old_count = before.get("citation_count", "")
        new_count = item.get("citation_count", "")
        if old_count != new_count:
            changed.append(
                {
                    "citation_id": key,
                    "title": item.get("title", ""),
                    "previous_citation_count": old_count,
                    "current_citation_count": new_count,
                }
            )
    return {"new_publications": added, "removed_publications": removed, "citation_changes": changed}


def csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    import io

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDS, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for record in rows:
        output = dict(record)
        output["review_flags"] = ";".join(record.get("review_flags", []))
        writer.writerow(output)
    return buffer.getvalue().encode("utf-8-sig")


def markdown_report(
    fetched_at: str,
    run_id: str,
    pages: list[tuple[int, str, dict[str, Any]]],
    publications: list[dict[str, Any]],
    duplicate_records: list[dict[str, Any]],
    csv_rows: list[dict[str, Any]],
    missing: dict[str, int],
    comparison: dict[str, Any],
    request_attempts: int,
    previous_count: int,
) -> str:
    years = Counter(str(record.get("year", "")).strip() or "（缺失）" for record in publications)
    raw_count = sum(len(page.get("articles", [])) for _, _, page in pages)
    page_lines = "\n".join(
        f"| {start} | {len(data.get('articles', []))} | {acquired} |"
        for start, acquired, data in pages
    ) or "| — | 0 | — |"
    year_lines = "\n".join(f"| {year} | {count} |" for year, count in sorted(years.items(), key=lambda item: (item[0] == "（缺失）", item[0]), reverse=False))
    missing_lines = "\n".join(f"| `{field}` | {count} / {len(publications)} |" for field, count in missing.items())
    duplicate_lines = "\n".join(
        f"| {item.get('duplicate_reason', '')} | {item.get('title', '')} | {item.get('year', '')} | {item.get('citation_id', '')} | {item.get('duplicate_of', '')} |"
        for item in duplicate_records
    ) or "| — | — | — | — | — |"
    citation_lines = "\n".join(
        f"| {item['title']} | {item['citation_id']} | {item['previous_citation_count']} | {item['current_citation_count']} |"
        for item in comparison["citation_changes"]
    ) or "| — | — | — | — |"
    new_lines = "\n".join(
        f"| {item.get('title', '')} | {item.get('year', '')} | {item.get('citation_id', '')} |"
        for item in comparison["new_publications"]
    ) or "| — | — | — |"
    removed_lines = "\n".join(
        f"| {item.get('title', '')} | {item.get('year', '')} | {item.get('citation_id', '')} |"
        for item in comparison["removed_publications"]
    ) or "| — | — |"
    estimated_cost = request_attempts

    return f"""# Google Scholar 论文采集报告

- 作者：檀韬（Tao Tan）
- Google Scholar ID：`{AUTHOR_ID}`
- 数据获取时间：{fetched_at}
- 采集轮次：`{run_id}`
- 原始条目数：{raw_count}
- 去重后论文数：{len(publications)}
- CSV 审核行数：{len(csv_rows)}
- 疑似重复记录数：{len(duplicate_records)}
- 与上次完整快照比较：{previous_count} 篇旧记录

## 分页完整性

共获取 {len(pages)} 页；每页最多 {PAGE_SIZE} 条。采集在下一页不存在且末页不足 {PAGE_SIZE} 条时结束。SerpApi 文档说明单次最多返回 100 条，`start` 为结果偏移量。

| start | API 条数 | 数据获取时间 |
|---:|---:|---|
{page_lines}

## 各年份论文数量

| 年份 | 篇数 |
|---|---:|
{year_lines}

## 字段缺失情况

统计口径为去重后的 {len(publications)} 条论文；缺失字段保持为空，没有推测或补造。

| 字段 | 缺失数 / 论文总数 |
|---|---:|
{missing_lines}

## 重复记录供人工核验

按 `citation_id` 去重；相同标题和年份但不同 `citation_id` 的记录仍保留，并标记为疑似重复。CSV 包含所有原始论文条目，JSON 的 `publications` 为去重结果，`duplicate_records` 保留重复条目。

| 原因 | 标题 | 年份 | citation_id | 对照 citation_id |
|---|---|---:|---|---|
{duplicate_lines}

## 与前一完整快照比较

### 新增论文（{len(comparison['new_publications'])}）

| 标题 | 年份 | citation_id |
|---|---:|---|
{new_lines}

### 引用量变化（{len(comparison['citation_changes'])}）

| 标题 | citation_id | 上次 | 本次 |
|---|---|---:|---:|
{citation_lines}

### 本次未见的旧论文（{len(comparison['removed_publications'])}）

| 标题 | 年份 | citation_id |
|---|---:|---|
{removed_lines}

## API 请求与额度估算

- HTTP API 请求尝试次数（含重试）：{request_attempts}
- 额度消耗保守估算：{estimated_cost} 次搜索请求
- 已完成分页的本地缓存命中不发起 API 请求，因而不增加本轮请求数。
- SerpApi 服务端缓存命中可能免费；本报告按每次 HTTP 尝试一次搜索请求估算，实际扣额以账户面板为准。

报告生成时间：{fetched_at}
"""


def transactional_publish(output_dir: Path, files: dict[str, bytes]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    staged: dict[Path, Path] = {}
    backups: dict[Path, Path | None] = {}
    replaced: list[Path] = []
    try:
        for name, payload in files.items():
            destination = output_dir / name
            fd, temp_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=output_dir)
            temp_path = Path(temp_name)
            staged[destination] = temp_path
            with os.fdopen(fd, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
        for destination in staged:
            if destination.exists():
                fd, backup_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".bak", dir=output_dir)
                os.close(fd)
                backup = Path(backup_name)
                shutil.copy2(destination, backup)
                backups[destination] = backup
            else:
                backups[destination] = None
        for destination, temp_path in staged.items():
            os.replace(temp_path, destination)
            replaced.append(destination)
    except Exception:
        for destination in reversed(replaced):
            backup = backups.get(destination)
            if backup and backup.exists():
                os.replace(backup, destination)
            else:
                try:
                    destination.unlink()
                except FileNotFoundError:
                    pass
        raise
    finally:
        for path in list(staged.values()) + [item for item in backups.values() if item is not None]:
            try:
                path.unlink()
            except FileNotFoundError:
                pass


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("docs/publications-scholar"))
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds (default: 30)")
    parser.add_argument("--retries", type=int, default=3, help="Retries after transient errors (default: 3)")
    parser.add_argument("--max-requests", type=int, default=20, help="Maximum HTTP attempts in this run (default: 20; 0 is unlimited)")
    parser.add_argument("--resume", nargs="?", const="latest", help="Resume the latest incomplete run or a specific run ID")
    parser.add_argument("--new-run", action="store_true", help="Start a new crawl instead of auto-resuming an incomplete run")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    api_key = os.environ.get("SERPAPI_API_KEY", "").strip()
    if not api_key:
        print("SERPAPI_API_KEY is required; the key is never written to files or output.", file=sys.stderr)
        return 2
    if args.timeout <= 0 or args.retries < 0 or args.max_requests < 0:
        print("timeout must be positive; retries and max-requests cannot be negative.", file=sys.stderr)
        return 2

    output_dir = args.output_dir
    raw_dir = output_dir / "raw"
    try:
        state_path, state = choose_run(raw_dir, args.resume, args.new_run)
        print(f"[INFO] Run {state['run_id']} started from cached progress where available.", flush=True)
        pages = fetch_all(api_key, state_path, state, args.timeout, args.retries, args.max_requests)
        if not pages:
            raise CollectionError("No pages were returned; refusing to publish an empty snapshot")

        publications, duplicate_records, csv_rows = build_records(pages)
        fetched_at = iso_now()
        previous = load_previous(output_dir / "publications.json")
        comparison = compare_snapshots(previous, publications)
        missing = missing_counts(publications)
        report = markdown_report(
            fetched_at,
            state["run_id"],
            pages,
            publications,
            duplicate_records,
            csv_rows,
            missing,
            comparison,
            state["request_attempts"],
            len(previous),
        )
        structured = {
            "schema_version": 1,
            "source": "SerpApi Google Scholar Author API",
            "author": {"name": "Tao Tan", "name_zh": "檀韬", "google_scholar_id": AUTHOR_ID},
            "profile_url": f"https://scholar.google.com/citations?user={AUTHOR_ID}&hl=en",
            "fetched_at": fetched_at,
            "run_id": state["run_id"],
            "pagination": {
                "page_size": PAGE_SIZE,
                "page_starts": [start for start, _, _ in pages],
                "raw_article_count": sum(len(page.get("articles", [])) for _, _, page in pages),
                "complete": True,
            },
            "publications": publications,
            "duplicate_records": duplicate_records,
            "comparison": comparison,
            "missing_fields": missing,
            "api_request_attempts": state["request_attempts"],
        }
        state["status"] = "ready_to_publish"
        state["last_error"] = ""
        save_state(state_path, state)
        transactional_publish(
            output_dir,
            {
                "publications.json": json_bytes(structured),
                "publications.csv": csv_bytes(csv_rows),
                "fetch-report.md": report.encode("utf-8"),
            },
        )
        state["status"] = "published"
        state["published_at"] = fetched_at
        save_state(state_path, state)
        print(
            f"[INFO] Complete: {len(publications)} unique publications from {len(pages)} pages; "
            f"{len(duplicate_records)} suspected duplicate record(s).",
            flush=True,
        )
        return 0
    except CollectionError as error:
        if "state" in locals() and "state_path" in locals():
            state["status"] = "failed"
            state["last_error"] = safe_error(error, api_key)
            save_state(state_path, state)
        print(f"[ERROR] {safe_error(error, api_key)}", file=sys.stderr)
        return 1
    except Exception as error:
        if "state" in locals() and "state_path" in locals():
            state["status"] = "failed"
            state["last_error"] = safe_error(error, api_key)
            save_state(state_path, state)
        print(f"[ERROR] Unexpected failure: {safe_error(error, api_key)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
