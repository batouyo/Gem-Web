#!/usr/bin/env python3
"""Read-only P0 inventory generator for the legacy Gem-Web static site.

Run from any directory with: python3 scripts/audit_site_p0.py
The script reads Git-tracked pre-P0 files and writes only docs/ inventories.
It never edits, moves, or deletes the existing website source or assets.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import mimetypes
import posixpath
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit, quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
HTML_ROOT = "html"
SKIP_PREFIXES = ("docs/",)
SKIP_FILES = {"scripts/audit_site_p0.py"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif", ".tif", ".tiff", ".bmp"}
FONT_EXTS = {".woff", ".woff2", ".ttf", ".otf", ".eot"}
DOC_EXTS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".odt"}
DATA_EXTS = {".json", ".bib", ".csv", ".xml", ".yaml", ".yml"}
CODE_EXTS = {".py", ".sh", ".ts", ".tsx", ".jsx"}
URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I | re.S)
MONTHS = {m.lower(): i for i, m in enumerate(("January February March April May June July August September October November December").split(), 1)}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})


def tracked_files() -> list[str]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, stdout=subprocess.PIPE)
    return [p.decode("utf-8", "surrogateescape") for p in result.stdout.split(b"\0") if p]


def should_scan(path: str) -> bool:
    return not path.startswith(SKIP_PREFIXES) and path not in SKIP_FILES


def read_text(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return ""


class PageParser(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.title_parts: list[str] = []
        self.title_on = False
        self.headings: list[tuple[str, str]] = []
        self.heading_on: int | None = None
        self.heading_parts: list[str] = []
        self.text_parts: list[str] = []
        self.refs: list[dict[str, str | int]] = []
        self.links: list[dict[str, str | bool | int]] = []
        self.images: list[str] = []
        self.css_inline: list[str] = []
        self.semantic_parts: dict[str, list[str]] = defaultdict(list)
        self.semantic_stack: list[tuple[str, set[str]]] = []
        self.in_style = False
        self.struct = Counter()
        self.style_attrs = 0
        self.style_blocks = 0
        self.times: list[str] = []
        self.viewport = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        ancestors = set(self.stack)
        in_nav = tag == "nav" or "nav" in ancestors or "navbar" in a.get("class", "").lower().split()
        in_footer = tag == "footer" or "footer" in ancestors
        self.struct[tag] += 1
        for token in ("navbar", "container", "card", "breadcrumb", "pagination", "article-post"):
            if token in a.get("class", "").lower().split():
                self.struct["class:" + token] += 1
        if tag == "style":
            self.in_style = True
            self.style_blocks += 1
        if tag == "title":
            self.title_on = True
        if tag in {"h1", "h2", "h3", "h4"}:
            self.heading_on = len(self.headings)
            self.headings.append((tag, ""))
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        if tag == "time" and a.get("datetime"):
            self.times.append(a["datetime"])
        if "style" in a:
            self.style_attrs += 1
            self.css_inline.append(a["style"])
        for attr in ("src", "href", "poster", "data", "background"):
            value = a.get(attr, "").strip()
            if value:
                self.refs.append({"raw": value, "kind": attr, "tag": tag, "line": self.getpos()[0], "in_nav": int(in_nav), "in_footer": int(in_footer)})
                if tag == "a" and attr == "href":
                    self.links.append({"raw": value, "text": "", "in_nav": in_nav, "line": self.getpos()[0]})
                if tag == "img" and attr == "src" and not in_nav and not in_footer:
                    self.images.append(value)
        if a.get("srcset"):
            for candidate in re.split(r",\s*(?![^()]*\))", a["srcset"]):
                value = candidate.strip().split()[0] if candidate.strip() else ""
                if value:
                    self.refs.append({"raw": value, "kind": "srcset", "tag": tag, "line": self.getpos()[0], "in_nav": int(in_nav), "in_footer": int(in_footer)})
                    if tag == "img" and not in_nav and not in_footer:
                        self.images.append(value)
        if tag not in self.VOID:
            self.stack.append(tag)
            semantic = {token for token in a.get("class", "").split() if token in {"paper_title", "paper_time", "paper_info", "People_name", "People_info_right_part"}}
            self.struct["semantic-open:" + ",".join(sorted(semantic))] += 1 if semantic else 0
            self.semantic_stack.append((tag, semantic))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title_on = False
        if tag == "style":
            self.in_style = False
        if tag in {"h1", "h2", "h3", "h4"}:
            self.heading_on = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                del self.stack[i:]
                break
        for i in range(len(self.semantic_stack) - 1, -1, -1):
            if self.semantic_stack[i][0] == tag:
                del self.semantic_stack[i:]
                break

    def handle_data(self, data: str) -> None:
        if self.title_on:
            self.title_parts.append(data)
        if self.heading_on is not None:
            self.headings[self.heading_on] = (self.headings[self.heading_on][0], self.headings[self.heading_on][1] + data)
        if data.strip():
            self.text_parts.append(data.strip())
        if self.in_style:
            self.css_inline.append(data)
        for _, classes in self.semantic_stack:
            for token in classes:
                self.semantic_parts[token].append(data)

    def handle_entityref(self, name: str) -> None:
        self.handle_data(html.unescape("&" + name + ";"))


def parsed_page(path: str) -> tuple[PageParser, str]:
    raw = read_text(path)
    p = PageParser()
    try:
        p.feed(raw)
        p.close()
    except Exception:
        pass
    return p, raw


def resolve_ref(raw: str, source: str, known: set[str], folded: dict[str, list[str]]) -> dict[str, str]:
    raw = html.unescape(raw.strip().strip("\"'"))
    try:
        u = urlsplit(raw)
    except ValueError:
        return {"status": "unparseable", "target": "", "normalized": ""}
    if u.scheme or u.netloc:
        return {"status": "external", "target": "", "normalized": u.geturl()}
    decoded = unquote(u.path).strip()
    if not decoded:
        return {"status": "fragment-only" if u.fragment else "empty", "target": "", "normalized": ""}
    if source.startswith(HTML_ROOT + "/"):
        # Resolve relative URLs in the web URL namespace. Parent segments cannot escape
        # the site's `/` root, even though the repository has files beside html/.
        source_rel = source[len(HTML_ROOT) + 1:]
        site_path = posixpath.normpath(decoded if decoded.startswith("/") else posixpath.join("/" + posixpath.dirname(source_rel), decoded))
        candidate = posixpath.normpath(HTML_ROOT + "/" + site_path.lstrip("/"))
    elif decoded.startswith("/"):
        candidate = posixpath.normpath(HTML_ROOT + "/" + decoded.lstrip("/"))
    else:
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(source), decoded))
    if candidate in {"html", "html/."}:
        candidate = "html/index.html"
    if decoded.endswith("/"):
        candidate = candidate.rstrip("/") + "/index.html"
    if candidate in known:
        return {"status": "resolved", "target": candidate, "normalized": candidate}
    # Directory index resolution (the Nginx config declares index.html/index.htm).
    for index_name in (candidate.rstrip("/") + "/index.html", candidate.rstrip("/") + "/index.htm"):
        if index_name in known:
            return {"status": "resolved-directory-index", "target": index_name, "normalized": candidate}
    matches = folded.get(candidate.casefold(), [])
    if len(matches) == 1:
        return {"status": "case-mismatch", "target": matches[0], "normalized": candidate}
    if len(matches) > 1:
        return {"status": "ambiguous-case-match", "target": "|".join(matches), "normalized": candidate}
    return {"status": "missing", "target": "", "normalized": candidate}


def css_urls(text: str) -> list[str]:
    return [html.unescape(m.group(2).strip()) for m in URL_RE.finditer(text) if m.group(2).strip()]


def slugify(text: str, fallback: str) -> str:
    text = unicodedata.normalize("NFKD", html.unescape(text)).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text[:76].rstrip("-") or re.sub(r"[^a-z0-9]+", "-", fallback.lower()).strip("-") or "untitled")


def iso_date(text: str, filename: str = "") -> str:
    s = html.unescape(text).replace("\xa0", " ")
    patterns = [r"\b(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})\b", r"(20\d{2})年\s*(\d{1,2})月\s*(\d{1,2})日"]
    for pat in patterns:
        m = re.search(pat, s)
        if m:
            try:
                return date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
            except ValueError:
                pass
    mon = r"\b(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?\s+(\d{1,2})(?:st|nd|rd|th)?[,]?\s+(20\d{2})\b"
    m = re.search(mon, s, re.I)
    if m:
        try:
            return date(int(m.group(3)), MONTHS[m.group(1).lower()[:3]], int(m.group(2))).isoformat()
        except ValueError:
            pass
    m = re.search(r"\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?[,]?\s+(20\d{2})\b", s, re.I)
    if m:
        try:
            return date(int(m.group(3)), MONTHS[m.group(2).lower()[:3]], int(m.group(1))).isoformat()
        except ValueError:
            pass
    m = re.search(r"(?<!\d)(20\d{2})(\d{2})(\d{2})(?!\d)", filename)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
        except ValueError:
            pass
    return ""


def page_type(path: str, p: PageParser, raw: str) -> str:
    low = path.lower()
    rel = path[len("html/"):] if path.startswith("html/") else path
    body = " ".join(p.text_parts).lower()
    title = " ".join(p.title_parts).lower()
    headings = " ".join(x[1] for x in p.headings).lower()
    if rel.lower() == "index.html": return "home"
    if "template-mundana-bootstrap-html-master/" in low: return "template-example"
    if re.search(r"(^|/)(test|test[-_])", rel.lower()): return "test-or-experiment"
    if rel.lower() in {"all_news.html", "news/index.html"} or "history-pagination" in raw.lower(): return "news-list"
    if rel.lower() == "all_research.html": return "research-list"
    # Keep frame/iframe documents as separate legacy routes until their embedding role is confirmed.
    if "frame" in low or "iframe" in raw.lower():
        return "news-fragment-or-frame" if "news" in low else "embedded-fragment"
    if "education" in low: return "education"
    if "contact" in low: return "contact"
    if "partner" in low or "collaboration" in title: return "partners"
    if "vacanc" in low or "vancancies" in low: return "vacancies"
    if re.search(r"(^|/)team(?:\.html)?$", rel.lower()) or "team_member" in raw.lower(): return "team"
    if rel.lower().startswith("team/") and (p.semantic_parts.get("People_name") or p.images): return "team-profile"
    if "demo" in low or "solution" in low and "research" not in low: return "demo"
    if re.search(r"(^|/)(new\d|news[_/])", rel.lower()) and (p.headings or "news" in body or "news" in title):
        return "news-detail"
    if re.match(r"^news_\d{8}/news_\d{8}.*\.html$", rel.lower()) and (p.semantic_parts.get("paper_title") or p.semantic_parts.get("paper_info")):
        return "news-detail"
    if "news" in low and (p.headings or "article" in raw.lower()): return "news-detail"
    if "publication" in low or "publications" in low or "publication" in title:
        return "publications"
    if "research" in low or "paper_info" in low or "research" in title:
        return "research-detail" if "paper_info" in low or "research/" in low or "_research/" in low else "research"
    if "new" in title or "news" in headings: return "news-or-article-review"
    return "other/unknown"


def group_for(path: str) -> str:
    low = path.lower()
    if "/news_" in low or re.search(r"/new\d", low) or "history_news" in low: return "news"
    if "research" in low or "paper_info" in low: return "research"
    if "/team/" in low or "team.html" in low: return "team"
    if "/assets/" in low: return "shared site assets"
    if any(k in low for k in ("logo", "favicon", "web_logo")): return "brand/shared"
    if "publication" in low or "output" in low or low.endswith(".bib"): return "publication/data"
    return "general or needs manual classification"


def file_category(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".html": return "HTML page"
    if ext in IMAGE_EXTS: return "image"
    if ext in {".css", ".scss", ".sass"}: return "stylesheet"
    if ext in {".js", ".mjs", ".cjs"}: return "script"
    if ext in FONT_EXTS: return "font"
    if ext in DOC_EXTS: return "document"
    if ext in DATA_EXTS: return "data"
    if ext in CODE_EXTS: return "helper/source script"
    if ext in {".conf", ".yaml", ".yml", ".toml"} or Path(path).name.lower().startswith("dockerfile"): return "deployment/config"
    return "other tracked file"


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with (ROOT / path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def clean(s: str, limit: int = 140) -> str:
    return re.sub(r"\s+", " ", html.unescape(s)).strip()[:limit]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "baseline/screenshots").mkdir(parents=True, exist_ok=True)
    files = [p for p in tracked_files() if should_scan(p) and (ROOT / p).is_file()]
    known = set(files)
    folded: dict[str, list[str]] = defaultdict(list)
    for p in files:
        folded[p.casefold()].append(p)
    html_files = sorted(p for p in files if p.lower().endswith((".html", ".htm")))
    pages: dict[str, dict[str, object]] = {}
    refs: list[dict[str, str | int]] = []
    for path in html_files:
        parser, raw = parsed_page(path)
        typ = page_type(path, parser, raw)
        title = clean("".join(parser.title_parts)) or Path(path).stem
        headings = [(tag, clean(txt)) for tag, txt in parser.headings if clean(txt)]
        main_heading = next((text for tag, text in headings if tag == "h1" and text.lower() not in {"news", "research", "publications", "contact"}), "")
        if not main_heading:
            main_heading = next((text for _, text in headings if text.lower() not in {"news", "research", "publications", "contact"}), "")
        if not main_heading:
            main_heading = clean("".join(parser.semantic_parts.get("paper_title", [])) or "".join(parser.semantic_parts.get("People_name", [])))
        page = {"path": path, "parser": parser, "raw": raw, "type": typ, "title": title, "heading": main_heading, "headings": headings}
        pages[path] = page
        for r in parser.refs:
            resolved = resolve_ref(str(r["raw"]), path, known, folded)
            refs.append({**r, "source": path, **resolved})
        for css in parser.css_inline:
            for raw_url in css_urls(css):
                resolved = resolve_ref(raw_url, path, known, folded)
                refs.append({"raw": raw_url, "kind": "inline-css-url", "tag": "style", "line": 0, "in_nav": 0, "in_footer": 0, "source": path, **resolved})
    # Parse statically linkable CSS files, including unreferenced stylesheets; dynamic JS is intentionally out of scope.
    for path in files:
        if Path(path).suffix.lower() == ".css":
            for raw_url in css_urls(read_text(path)):
                resolved = resolve_ref(raw_url, path, known, folded)
                refs.append({"raw": raw_url, "kind": "css-url", "tag": "css", "line": 0, "in_nav": 0, "in_footer": 0, "source": path, **resolved})
    refs_by_target: dict[str, list[str]] = defaultdict(list)
    target_case_errors: Counter[str] = Counter()
    for r in refs:
        target = str(r.get("target", ""))
        status = str(r.get("status", ""))
        if target:
            refs_by_target[target].append(str(r["source"]))
        if status == "case-mismatch":
            target_case_errors[target] += 1

    # Build incoming page-link and navigation maps.
    incoming: Counter[str] = Counter()
    nav_incoming: Counter[str] = Counter()
    for path, page in pages.items():
        parser = page["parser"]
        assert isinstance(parser, PageParser)
        for link in parser.links:
            res = resolve_ref(str(link["raw"]), path, known, folded)
            target = str(res.get("target", ""))
            if target in pages:
                incoming[target] += 1
                if bool(link["in_nav"]): nav_incoming[target] += 1

    # News-list data sources; links remain separate sources of truth until migration.
    list_counts: dict[str, Counter[str]] = {"homepage": Counter(), "all_news": Counter(), "history_js": Counter()}
    for source_name, source_path in (("homepage", "html/index.html"), ("all_news", "html/all_news.html")):
        page = pages.get(source_path)
        if not page: continue
        parser = page["parser"]
        assert isinstance(parser, PageParser)
        for link in parser.links:
            res = resolve_ref(str(link["raw"]), source_path, known, folded)
            target = str(res.get("target", ""))
            if target in pages and pages[target]["type"] in {"news-detail", "news-fragment-or-frame", "news-or-article-review"}:
                list_counts[source_name][target] += 1
    history_path = "html/news/history_news.js"
    history_text = read_text(history_path) if history_path in known else ""
    history_links = re.findall(r"[\"']href[\"']\s*:\s*[\"']([^\"']+)[\"']", history_text)
    for href in history_links:
        # href values are later assigned to anchors, so relative paths resolve from the embedding document.
        res = resolve_ref(href, "html/index.html", known, folded)
        target = str(res.get("target", ""))
        ref = {"raw": href, "kind": "js-data-href", "tag": "history_news.js", "line": 0, "in_nav": 0, "in_footer": 0, "source": history_path, "resolution_base": "html/index.html", **res}
        refs.append(ref)
        if target:
            list_counts["history_js"][target] += 1
            refs_by_target[target].append(history_path)
            if res.get("status") == "case-mismatch": target_case_errors[target] += 1

    # Route map: one row for each tracked HTML document; proposed routes are advisory only.
    route_rows: list[dict[str, object]] = []
    route_used: dict[str, str] = {}
    news_rows: list[dict[str, object]] = []
    news_slugs: dict[str, str] = {}
    news_dupe_titles: Counter[str] = Counter()
    for path, page in pages.items():
        parser = page["parser"]
        assert isinstance(parser, PageParser)
        typ = str(page["type"])
        title = str(page["title"])
        heading = str(page["heading"])
        rel = path[len("html/"):] if path.startswith("html/") else ""
        legacy = "/" + quote(rel, safe="/-._~") if rel else ""
        if rel.lower() == "index.html": legacy = "/index.html"
        slug_basis = heading or title
        if clean(slug_basis).lower() in {"", "imcl", "research", "news", "publications", "paper info", "article"}:
            slug_basis = re.sub(r"\.html?$", "", path[len("html/"):] if path.startswith("html/") else path).replace("/", "-")
        route_slug = slugify(slug_basis, Path(path).stem)
        status = "proposed"
        priority = "P2"
        notes: list[str] = []
        proposed = ""
        if not rel:
            status, priority = "outside-nginx-document-root", "P3"
            notes.append("HTML file is tracked outside html/, which docker-compose mounts as the Nginx document root.")
        elif typ == "home": proposed, priority = "/", "P1"
        elif typ == "news-list": proposed, priority = "/news/", "P1"
        elif typ == "news-detail":
            key = route_slug
            if key in news_slugs and news_slugs[key] != path:
                key = f"{key}-{Path(path).stem.lower()}"
                notes.append("Slug collision resolved with source filename suffix.")
            news_slugs[key] = path
            proposed, priority = f"/news/{key}/", "P1"
        elif typ == "research-list": proposed, priority = "/research/", "P1"
        elif typ in {"research", "research-detail"}:
            proposed, priority = f"/research/{route_slug}/", "P2"
        elif typ == "publications":
            year = re.search(r"(20\d{2})", Path(path).stem)
            proposed = f"/publications/{year.group(1)}/" if year else "/publications/"
            priority = "P1"
        elif typ == "team": proposed, priority = "/team/", "P1"
        elif typ == "team-profile": proposed, priority = f"/team/{route_slug}/", "P2"
        elif typ == "contact": proposed, priority = "/contact/", "P2"
        elif typ == "education": proposed, priority = "/education/", "P2"
        elif typ == "vacancies": proposed, priority = "/vacancies/", "P2"
        elif typ == "partners": proposed, priority = "/partners/", "P2"
        elif typ == "demo": proposed, priority = f"/demos/{route_slug}/", "P2"
        elif typ in {"template-example", "test-or-experiment", "embedded-fragment", "news-fragment-or-frame"}:
            status, priority = "manual-review-before-migration", "P3"
            proposed = ""
        else:
            status, priority = "manual-classification", "P3"
            notes.append("Content-based rule did not establish a confident page type.")
        if proposed in route_used and route_used[proposed] != path:
            original = proposed
            suffix = slugify(re.sub(r"\.html?$", "", rel).replace("/", "-"), Path(path).stem)
            parent = proposed.rstrip("/").rsplit("/", 1)[0]
            proposed = f"{parent}/{suffix}/"
            if proposed in route_used:
                proposed = f"{parent}/{suffix}-{len(route_rows)+1}/"
            notes.append(f"Unique proposal; primary candidate `{original}` also maps from `{route_used[original]}` and requires editorial choice.")
            if status == "proposed": status = "route-collision-review"
        if proposed:
            route_used[proposed] = path
        if rel.lower() == "index.html": notes.append("Nginx index resolution also serves this source at `/`.")
        if " " in rel or any(ord(c) > 127 for c in rel): notes.append("Legacy path contains a space and/or non-ASCII characters; browser URL encoding should be verified.")
        if "frame" in path.lower() or "_frame" in path.lower(): notes.append("Filename indicates a frame/fragment variant; not presumed obsolete.")
        if typ == "template-example": notes.append("Vendored Mundana example tree; retained pending usage/license review.")
        if typ == "test-or-experiment": notes.append("Test/experiment naming is evidence only; runtime use has not been checked.")
        local_images: list[str] = []
        local_scripts: list[str] = []
        for r in refs:
            if r["source"] != path: continue
            target = str(r.get("target", ""))
            if target and Path(target).suffix.lower() in IMAGE_EXTS and target not in local_images: local_images.append(target)
            if target and (Path(target).suffix.lower() in {".js", ".mjs"}) and target not in local_scripts: local_scripts.append(target)
        shared = [x for x, ok in (("nav", parser.struct["nav"] > 0), ("footer", parser.struct["footer"] > 0), ("container", parser.struct["class:container"] > 0)) if ok]
        page_notes = notes + (["Shared structure evidence: " + ", ".join(shared)] if shared else [])
        route_rows.append({"legacy_path": legacy, "source_file": path, "page_type": typ, "page_title": title, "main_heading": heading, "inbound_internal_link_count": incoming[path], "site_nav_entry": "yes" if nav_incoming[path] else "no", "shared_structure": ", ".join(shared), "associated_images": " | ".join(local_images), "associated_scripts": " | ".join(local_scripts), "proposed_path": proposed, "slug": route_slug if proposed else "", "migration_priority": priority, "status": status, "notes": " ".join(page_notes)})
        if typ == "news-detail":
            story_title = clean("".join(parser.semantic_parts.get("paper_title", []))) or heading or title
            lower_title = story_title.lower().strip()
            news_dupe_titles[lower_title] += 1
            body_text = " ".join(parser.text_parts)
            date_source = ""
            pubdate = ""
            for d in parser.times:
                pubdate = iso_date(d, path)
                if pubdate: date_source = "<time datetime>"; break
            if not pubdate:
                visible = "".join(parser.semantic_parts.get("paper_time", [])) + " " + body_text[:2400] + " " + story_title
                pubdate = iso_date(visible)
                if pubdate: date_source = "visible page text (first parseable date)"
            if not pubdate:
                pubdate = iso_date("", path)
                if pubdate: date_source = "filename date fallback"
            image_paths: list[str] = []
            for raw_img in parser.images:
                im = resolve_ref(raw_img, path, known, folded)
                target = str(im.get("target", ""))
                if target and Path(target).suffix.lower() in IMAGE_EXTS and target not in image_paths:
                    if not re.search(r"(^|[/_-])(logo|icon|web_logo)([/_.-]|$)", target, re.I): image_paths.append(target)
            cover = image_paths[0] if image_paths else ""
            if cover:
                img_dir = str(PurePosixPath(cover).parent) + "/"
                cover_note = "first resolvable non-logo body <img>; heuristic, verify editorial crop"
            else:
                img_dir, cover_note = "", "No reliable body <img> cover identified; inspect CSS backgrounds/embedded media manually."
            language = "mixed" if re.search(r"[\u4e00-\u9fff]", story_title) and re.search(r"[A-Za-z]", story_title) else ("Chinese" if re.search(r"[\u4e00-\u9fff]", story_title) else ("English/Latin" if re.search(r"[A-Za-z]", story_title) else "unknown"))
            index_n = list_counts["homepage"][path]
            all_n = list_counts["all_news"][path]
            hist_n = list_counts["history_js"][path]
            occurrences = sum(n > 0 for n in (index_n, all_n, hist_n))
            anomaly: list[str] = []
            if not pubdate: anomaly.append("date needs manual confirmation")
            if not cover: anomaly.append("cover not confidently identified")
            if occurrences > 1: anomaly.append("listed in multiple news sources; duplication is editorial, not necessarily duplicate content")
            if index_n > 1 or all_n > 1 or hist_n > 1: anomaly.append("duplicate entry within a source")
            news_rows.append({"source_file": path, "legacy_path": legacy, "title": story_title, "published_date_iso": pubdate, "date_source": date_source, "image_directory": img_dir, "cover_image_path": cover, "related_body_images": " | ".join(image_paths), "in_homepage": "yes" if index_n else "no", "homepage_link_count": index_n, "in_all_news": "yes" if all_n else "no", "all_news_link_count": all_n, "in_history_news_js": "yes" if hist_n else "no", "history_news_link_count": hist_n, "language_from_title": language, "slug": route_slug, "proposed_path": f"/news/{route_slug}/", "anomaly_or_review": "; ".join(anomaly), "extraction_notes": cover_note + ("; date extracted from " + date_source if date_source else "; date not reliably extracted")})
    # Disambiguate duplicate news slugs after all title collisions are known.
    slugs = Counter(str(r["slug"]) for r in news_rows)
    for r in news_rows:
        if slugs[str(r["slug"])] > 1:
            suffix = Path(str(r["source_file"])).stem.lower()
            r["slug"] = str(r["slug"]) + "-" + suffix
            r["proposed_path"] = "/news/" + str(r["slug"]) + "/"
            r["anomaly_or_review"] = (str(r["anomaly_or_review"]) + "; " if r["anomaly_or_review"] else "") + "slug collision; filename suffix added"
    news_title_counts = Counter(clean(str(r["title"])).lower() for r in news_rows)
    for r in news_rows:
        if news_title_counts[clean(str(r["title"])).lower()] > 1:
            r["anomaly_or_review"] = (str(r["anomaly_or_review"]) + "; " if r["anomaly_or_review"] else "") + "duplicate normalized title candidate"

    # Asset inventory with SHA-256 duplicate groups and explicit rows for broken local references.
    hash_to_paths: dict[str, list[str]] = defaultdict(list)
    file_rows: list[dict[str, object]] = []
    size_by_path: dict[str, int] = {}
    hash_by_path: dict[str, str] = {}
    for path in files:
        try:
            size = (ROOT / path).stat().st_size
            digest = sha256(path)
        except OSError:
            size, digest = 0, ""
        size_by_path[path], hash_by_path[path] = size, digest
        if digest and size > 0: hash_to_paths[digest].append(path)
    for path in files:
        ext = Path(path).suffix.lower()
        srcs = sorted(set(refs_by_target.get(path, [])))
        statuses = "case-mismatch" if target_case_errors[path] else (f"referenced by {len(srcs)} source file(s)" if srcs else "not seen in HTML/CSS static scan; dynamic/data use possible")
        file_rows.append({"path": path, "category": file_category(path), "extension": ext or "[none]", "mime_type": mimetypes.guess_type(path)[0] or "", "size_bytes": size_by_path[path], "sha256": hash_by_path[path], "duplicate_hash_paths": " | ".join(sorted(hash_to_paths[hash_by_path[path]])) if len(hash_to_paths[hash_by_path[path]]) > 1 else "", "referenced_by_count": len(srcs), "referenced_by": " | ".join(srcs[:30]) + (f" | …(+{len(srcs)-30})" if len(srcs) > 30 else ""), "reference_status": statuses, "suggested_group": group_for(path), "notes": "Hash covers repository bytes; zero references do not imply unused."})
    missing_rows: list[dict[str, object]] = []
    missing_seen: set[tuple[str, str, str]] = set()
    for r in refs:
        if str(r["status"]) not in {"missing", "case-mismatch", "ambiguous-case-match", "unparseable"}: continue
        key = (str(r["source"]), str(r["raw"]), str(r["status"]))
        if key in missing_seen: continue
        missing_seen.add(key)
        missing_rows.append({"path": str(r.get("normalized", "")), "category": "unresolved local reference", "extension": Path(str(r.get("normalized", ""))).suffix.lower(), "mime_type": "", "size_bytes": "", "sha256": "", "duplicate_hash_paths": "", "referenced_by_count": 1, "referenced_by": str(r["source"]), "reference_status": str(r["status"]), "suggested_group": "manual link validation", "notes": f"raw={r['raw']}; kind={r['kind']}; line={r['line']}; base={r.get('resolution_base','source file')}; matched={r.get('target','')}"})
    file_rows.extend(missing_rows)
    write_csv(OUT / "route-map.csv", ["legacy_path", "source_file", "page_type", "page_title", "main_heading", "inbound_internal_link_count", "site_nav_entry", "shared_structure", "associated_images", "associated_scripts", "proposed_path", "slug", "migration_priority", "status", "notes"], route_rows)
    write_csv(OUT / "news-inventory.csv", ["source_file", "legacy_path", "title", "published_date_iso", "date_source", "image_directory", "cover_image_path", "related_body_images", "in_homepage", "homepage_link_count", "in_all_news", "all_news_link_count", "in_history_news_js", "history_news_link_count", "language_from_title", "slug", "proposed_path", "anomaly_or_review", "extraction_notes"], news_rows)
    write_csv(OUT / "asset-inventory.csv", ["path", "category", "extension", "mime_type", "size_bytes", "sha256", "duplicate_hash_paths", "referenced_by_count", "referenced_by", "reference_status", "suggested_group", "notes"], file_rows)

    # Measured counts for reports and checks.
    types = Counter(str(p["type"]) for p in pages.values())
    ext_counts = Counter(Path(p).suffix.lower() or "[none]" for p in files)
    category_counts = Counter(file_category(p) for p in files)
    zero_byte_files = sum(size == 0 for size in size_by_path.values())
    root_files = sorted(p for p in files if "/" not in p)
    dirs = Counter(p.split("/", 2)[1] if p.startswith("html/") and "/" in p[len("html/"):] else "html (top-level)" for p in files if p.startswith("html/"))
    bad_refs = [r for r in refs if r["status"] in {"missing", "case-mismatch", "ambiguous-case-match", "unparseable"}]
    ref_status_counts = Counter(str(r["status"]) for r in refs)
    duplicate_groups = [v for v in hash_to_paths.values() if len(v) > 1]
    shared_nav = sum(bool(p["parser"].struct["nav"]) for p in pages.values())
    shared_footer = sum(bool(p["parser"].struct["footer"]) for p in pages.values())
    viewport_count = sum(bool(p["parser"].viewport) for p in pages.values())
    style_attr_total = sum(p["parser"].style_attrs for p in pages.values())
    style_block_total = sum(p["parser"].style_blocks for p in pages.values())
    css_media = sum(len(re.findall(r"@media\b", read_text(p), re.I)) for p in files if Path(p).suffix.lower() in {".css", ".scss"})
    html_page_counts = Counter("served" if p.startswith("html/") else "outside html/" for p in html_files)
    news_list_source_counts = {k: sum(v.values()) for k, v in list_counts.items()}
    history_refs_bad = [r for r in refs if r["source"] == history_path and r["status"] in {"missing", "case-mismatch", "ambiguous-case-match"}]
    top_asset_dirs = Counter()
    for p in files:
        if not p.startswith("html/"): continue
        rel = p[5:]
        top_asset_dirs[rel.split("/", 1)[0] if "/" in rel else "(html root)"] += 1
    current_branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()

    def table(counter: Counter[str], limit: int = 30) -> str:
        return "\n".join(f"| `{k or '[none]'}` | {v} |" for k, v in counter.most_common(limit)) or "| — | 0 |"

    key_pages = [(p, pages[p]) for p in ("html/index.html", "html/all_news.html", "html/all_research.html", "html/Publication2025.html", "html/Team.html") if p in pages]
    route_collision_groups: dict[str, list[str]] = defaultdict(list)
    for r in route_rows:
        if r["proposed_path"]: route_collision_groups[str(r["proposed_path"])].append(str(r["source_file"]))
    collisions = {k: v for k, v in route_collision_groups.items() if len(v) > 1}
    route_status_counts = Counter(str(r["status"]) for r in route_rows)
    route_priority_counts = Counter(str(r["migration_priority"]) for r in route_rows)
    news_without_cover = [str(r["source_file"]) for r in news_rows if not r["cover_image_path"]]
    issue_rows: list[dict[str, str]] = []
    issue_seen: set[tuple[str, str, str]] = set()
    for r in sorted(bad_refs, key=lambda x: (str(x["source"]), int(x["line"]), str(x["raw"]))):
        key = (str(r["source"]), str(r["raw"]), str(r["status"]))
        if key in issue_seen:
            continue
        issue_seen.add(key)
        issue_rows.append({"source": key[0], "raw": key[1], "status": key[2], "target": str(r.get("target", "")), "line": str(r.get("line", 0))})
        if len(issue_rows) >= 18:
            break
    issue_sample_md = "\n".join(f"| `{x['source']}` | `{clean(x['raw'], 90)}` | {x['status']} | `{x['target']}` | {x['line']} |" for x in issue_rows) or "| — | — | — | — | — |"
    report = f"""# P0 项目盘点与基线报告

## 范围与证据口径

- 本次扫描基于本地 Git 跟踪文件；生成前的工作区干净，分支 `{current_branch}`，基线 Commit `{commit}`。
- Nginx 配置把 `html/` 挂载为文档根目录；因此 `html/` 下 HTML 文件按旧站路径映射，仓库外该目录的 HTML 会单独标识。
- “已验证”指源文件中直接可见的事实；页面实际运行行为、外部链接可用性、访客视角视觉结果则需浏览器验证。
- 扫描脚本静态解析 HTML 的 `src`/`href`/`srcset`/`poster`/`data`/`background`、内联样式和 CSS `url()`。不执行 JavaScript，也不访问网络；动态路径和外部资源不作为已验证。
- 只读扫描没有修改现有 HTML、CSS、JavaScript、部署配置或静态资源。

## 项目概况

Gem-Web 是澳门理工大学应用科学学院 IMCL（Intelligent Medical Computing Laboratory）实验室的静态网站。首页称实验室提供数字医疗解决方案；自定义域名见 `html/CNAME`。页面主要为独立 HTML，样式为传统 CSS/SCSS，交互使用 jQuery/Bootstrap 资源，内容以静态文件和 JavaScript 数据表为主。

| 指标 | 结果 |
|---|---:|
| Git 跟踪文件（扫描范围） | {len(files)} |
| HTML 文件（全仓库） | {len(html_files)} |
| HTML 位于 Nginx `html/` 根目录 | {html_page_counts.get('served', 0)} |
| HTML 位于 `html/` 外 | {html_page_counts.get('outside html/', 0)} |
| HTML 页面类型 | {len(types)} 类 |
| 新闻详情候选 | {len(news_rows)} |
| 资源/其他文件（按扩展名） | {len(files) - len(html_files)} |
| 静态引用异常（missing / 大小写 / 有歧义） | {len(bad_refs)} 条引用 |
| 非空文件 SHA-256 完全重复组 | {len(duplicate_groups)} 组 |
| 零字节跟踪文件 | {zero_byte_files} |

### 根目录文件

`{', '.join('`'+p+'`' for p in root_files) if root_files else '无根目录文件'}。` 重点用途：`docker-compose.yaml`/`default.conf` 提供 Nginx 静态服务配置；`GEM_library.bib` 和根目录 JSON 是出版物数据源/导出数据；`exceltojson.py`、`test.py` 是数据转换脚本。`first test.txt` 名称像临时文件，但仅凭名称无法确认是否可删除。

### HTML 子目录文件分布

| `html/` 一级目录 | Git 跟踪文件数 |
|---|---:|
{table(top_asset_dirs, 55)}

### 页面分类

| 类型（基于标题、结构和路径内容规则） | 数量 |
|---|---:|
{table(types)}

分类规则自动化且可复核；`other/unknown`、frame/fragment、测试和模板页面仍需人工判定。完整来源、旧 URL、标题、站内导航入口、图片/脚本和迁移建议见 `route-map.csv`。

| 路由状态 | 数量 |
|---|---:|
{table(route_status_counts)}

`route-collision-review` 页面虽然已在 CSV 中给出不同的临时建议路径，但它们共享较宽泛的内容分类路由，仍需内容负责人确认最终 URL；frame、template、test 页面则不预设新公开路由。

### 主要页面与系统结构

| 源文件 | 已确认用途/证据 |
|---|---|
""" + "\n".join(f"| `{p}` | `{d['type']}`；title：{clean(str(d['title']), 90)}；nav 标签：{d['parser'].struct['nav'] > 0}；页脚标签：{d['parser'].struct['footer'] > 0}。 |" for p, d in key_pages) + f"""

- `docker-compose.yaml` 以 `nginx:alpine` 将主机 `49306` 端口映射到容器 `80`，只读挂载 `default.conf` 和 `html/`。
- `default.conf` 配置 `index.html`/`index.htm`，没有应用后端或 API 代理。
- `html/assets/` 有 {sum(1 for p in files if p.startswith('html/assets/'))} 个跟踪文件；`html/template-mundana-bootstrap-html-master/` 保存模板副本及构建文件。
- Gulpfile 提供 SCSS 编译、watch 和 open 任务；`html/package.json` 仅列 Gulp 开发依赖，未显示 Astro/Vite/TypeScript 应用构建。
- Python 辅助脚本包括根级 Excel 转输出格式脚本、将 JSON 写为 `window.PAPERS_JSON` 的 `test.py`，以及 BibTeX 转 JSON 脚本。脚本的当前路径/工作目录假设应在未来数据流程整理时核实。
- 代码中可见 Bootstrap、jQuery、Popper 和 Font Awesome；Google Fonts/Font Awesome CSS 通过外部 CDN 引用。外网加载与许可证/版本稳定性未做在线验证。

### 文件扩展名分布

| 扩展名 | 数量 |
|---|---:|
{table(ext_counts, 45)}

### 静态资源与链接检查

- `{len(refs)}` 个 HTML/CSS 静态引用候选中，`{sum(r['status'] in {'resolved','resolved-directory-index'} for r in refs)}` 个能按本地文件解析，`{sum(r['status']=='external' for r in refs)}` 个为外部 URL，`{ref_status_counts['fragment-only']}` 个为仅 fragment、`{ref_status_counts['empty']}` 个为空引用；另有 `{len(bad_refs)}` 次无法精确解析或大小写不匹配。按来源/原文/状态去重后为 `{len(missing_rows)}` 行，见 `asset-inventory.csv` 的 `unresolved local reference`。
- 按文件用途分类：

| 类型 | 跟踪文件数 |
|---|---:|
{table(category_counts, 30)}

- 异常样例（完整来源、原始 URL、解析目标见资产清单）：

| 来源文件 | 原始引用 | 状态 | 候选目标 | 行 |
|---|---|---|---|---:|
{issue_sample_md}
- 检查对空格、中文、百分号编码、查询字符串和 fragment 进行解码/分离；文件名匹配按大小写敏感，另报告唯一的 case-fold 候选。
- SHA-256 完全重复组为 `{len(duplicate_groups)}`，只统计非空文件的字节完全重复；没有删除或移动资源。
- 未被扫描到的文件只标为“HTML/CSS 静态扫描未发现”，不等价于废弃；JS 拼接/动态资源、模板条件代码和外部网络资源未求值。`history_news.js` 中的字面量 href 单独解析，但不执行脚本。
- 资源完整清单包含路径、类型、字节数、SHA-256、重复路径、引用源和建议归属，详见 `asset-inventory.csv`。

### 部署与历史文件

- `html/CNAME` 写有 `www.gemlab.site`；仓库是否由 GitHub Pages 直接发布，以及当前线上部署链路，不由这份文件单独证明。
- `html/template-mundana-bootstrap-html-master/README.md` 把模板描述为 MIT；同目录 `package.json` 另列 WowThemesNet License URL。使用/重分发资产前应核对实际许可证文件和具体资源来源，不按模板副本整体推定许可。
- 文件名含 `test`、旧式 `_frame`、多份年份出版物页和模板示例均作为候选待审，不自动判废。页面分类和证据在路由表中。

## 功能与内容维护方式

- 首页 `html/index.html` 将 7 篇最新新闻卡片直接写在 HTML 中；此外页面含 `#history-list`/分页容器，加载 `html/news/history_news.js` 并通过内联脚本读取 `window.HISTORY_NEWS` 生成历史列表。两部分的链接、日期、标题和缩略图分别维护。
- `html/all_news.html` 是独立静态新闻列表，当前有 `{news_list_source_counts['all_news']}` 个活动详情链接、指向 `{sum(1 for r in news_rows if int(r['all_news_link_count']) > 0)}` 篇不同新闻；文件中另保留注释掉的旧卡片，不加载 `history_news.js`。其中 `{sum(int(r['all_news_link_count']) > 1 for r in news_rows)}` 篇在活动列表重复出现。
- `html/news/history_news.js` 暴露 `{news_list_source_counts['history_js']}` 个可解析 href；扫描还发现首页 `{news_list_source_counts['homepage']}` 个静态新闻详情链接。`{sum('multiple news sources' in str(r['anomaly_or_review']) for r in news_rows)}` 篇新闻出现在两个或以上维护入口；标题、日期和图片可能不一致。
- 新闻详情多数是单独 HTML，图片通常放在 `html/news_YYYYMMDD.../` 或成员/研究项目目录。标题、日期和封面提取规则各异；完整逐篇记录见 `news-inventory.csv`。
- `{len(news_without_cover)}` 篇新闻未能从正文 `<img>` 稳定识别封面（可能使用背景图、frame 或无图），封面字段保留为空；文件路径见 `news-inventory.csv`。日期均由页面文本或文件名规则提取，仍建议编辑复核。
- 标题识别结果为 English/Latin `{sum(r['language_from_title']=='English/Latin' for r in news_rows)}` 篇、mixed `{sum(r['language_from_title']=='mixed' for r in news_rows)}` 篇、Chinese `{sum(r['language_from_title']=='Chinese' for r in news_rows)}` 篇；日期有 `{sum(r['date_source']=='visible page text (first parseable date)' for r in news_rows)}` 篇从可见页面文本提取、`{sum(r['date_source']=='filename date fallback' for r in news_rows)}` 篇回退到文件名规则，仍建议人工复核。
- 出版物以 BibTeX、不同 `output*.json`（包含 `output([...])` JavaScript 回调格式）和手写年份 HTML 并存；不同年份页面及主导航可能未同步。

## 组件化发现

详见 `component-inventory.md`。扫描到 `{shared_nav}` 个页面有 `<nav>`、`{shared_footer}` 个页面有 `<footer>`，`{style_block_total}` 个内联 `<style>` 块、`{style_attr_total}` 个 HTML `style` 属性；{viewport_count}/{len(html_files)} 个 HTML 带 viewport meta。页面容器/Bootstrap 卡片/nav/footer 是 Astro Layout 与组件的主要候选，但类名重复不代表语义一致，迁移时要按模板族归并。

## 视觉/交互基线

源码层面的页面基线与不能实测的项目见 `baseline/visual-baseline.md`。当前环境未安装 Chromium/Chrome/Firefox 或 Playwright/Selenium，因而未生成桌面/手机截图，也没有声称实际浏览器渲染已通过。

## 后续工作建议

1. 先把页面路由和新闻元数据定成唯一数据源，优先处理首页新闻、新闻列表和详情页。
2. P1 先锁定保留 Logo/绿色品牌调性、信息层级、桌面与移动断点；以首页、新闻列表、详情、研究列表为设计样板。
3. P2 建公共站点 Layout、导航、页脚、Hero、新闻卡、文章正文、Research 卡和 publications table，再逐类迁移。
4. 在迁移任何资源前使用本清单中的引用和哈希信息；对所有旧 URL 生成重定向/别名策略，并把当前静态引用异常列入逐项修复验收。

## 可重复执行

运行 `python3 scripts/audit_site_p0.py` 可基于 Git 跟踪的站点源码重新生成三个 CSV 与本文中的统计。当前脚本检查 CSV 结构、HTML 路由唯一性并报告未解析静态引用；人工内容判断和截图仍需单独验收。
"""
    (OUT / "legacy-inventory.md").write_text(report, encoding="utf-8")

    # Component recommendations are tied to measured markup and concrete source files.
    component_doc = f"""# 重复结构与组件盘点

本文件只记录现有 HTML 可复用结构，不创建或迁移任何组件。页面标签计数来自当前 Git 跟踪的 {len(html_files)} 个 HTML 文件。注意：有相同 class 不一定代表内容语义、样式和交互相同，应分模板族迁移。

## 观测到的重复结构

| 结构/候选组件 | 源码证据 | 复用建议 |
|---|---|---|
| SiteLayout / Navigation | {shared_nav} 页含 `<nav>`；`index.html`、`all_research.html`、`Publication2025.html`、`Team.html`、`Contact.html` 都有重复 Bootstrap navbar、Logo、9 个栏目链接 | Astro `BaseLayout` + `SiteHeader`；导航项单一配置，逐个验证旧链接与断点折叠。多个历史页面菜单目标不一致，不能盲目复制单页版本。 |
| SiteFooter | {shared_footer} 页含 `<footer>` 标签；旧页也可能用非 footer div 实现 | `SiteFooter` 统一实验室名称/学校归属/版权；先盘点旧 footer 文案差异。 |
| PageHero / PageHeader | `index.html` 的 jumbotron 介绍区；新闻详情、Team、Contact 等重复用 Bootstrap `jumbotron`、container/row/col 结构 | 抽取参数化标题、日期、说明和可选封面；首页独特大 Hero 保留为变体。 |
| NewsCard / NewsGrid | 首页硬编码新闻卡片，含缩略图、标题、日期；`all_news.html` 有旧卡片结构；history 脚本以 JS 对象存新闻 | 单一 Markdown collection 驱动首页、归档列表和详情；组件只渲染数据，封面字段需编辑确认。 |
| NewsArticle | 多个 `New*.html` 详情页以标题/日期/图像/正文/返回按钮构成；部分标题、正文、插图和布局写法不同 | Markdown frontmatter + `NewsLayout`；将图注、链接、嵌入内容与中英双语变体作为显式字段/Markdown 内容块。 |
| ResearchCard / ResearchDetail | `all_research.html` 中多个项目卡片链接到 `Research/*.html`，同时有 `_research` 成员目录和 paper-info/frame 页 | 统一 `ResearchCard` 与研究详情 layout；保留成员研究页、项目页、论文说明页的区别。 |
| PublicationTable | `Publication2025.html` 等表格按年/其他年份加载 `output*.json`；旧的 `publications2024.html` 等为另一套硬编码/数据驱动表 | TypeScript publication schema + 一份归一化数据；year filter/list view 用配置控制，确保年份和字段有版本校验。 |
| Pagination | 首页 CSS 声明 `#history-pagination`、`.page-item`，且加载历史新闻 JS；需由页面脚本和浏览器运行确认是否执行 | 新站优先用静态分页或 Astro 生成归档；页码/无 JS 状态需可访问。 |
| Breadcrumb | 本次扫描未发现稳定、广泛使用的 `<nav aria-label="breadcrumb">` / `.breadcrumb` 结构 | 不作为现有必迁组件；新路由如需层级导航再设计。 |
| Button / Return link | 多页复用 Bootstrap `.btn`、`btn-dark/success`，详情页常见 Return | `Button` 可依赖设计 token/链接组件；不要把不同操作和颜色一概合并。 |
| Container / Grid | Bootstrap `.container`、`.row`、`.col-*` 在主要页面重复；具体宽度跟 Bootstrap 栅格及局部 CSS 叠加 | Astro layout 复用容器，SCSS design tokens 控制页面最大宽度、间距和响应断点。 |

## 重复样式与不一致线索

- 当前至少 `{style_block_total}` 个内联 `<style>` 块和 `{style_attr_total}` 个内联 `style` 属性；首页自己覆写新闻卡片、hover、分页和历史条目布局。
- `{css_media}` 个 `@media` 声明可在 CSS/SCSS 文本中静态扫描到；`{viewport_count}/{len(html_files)}` 页含 viewport meta。尚未运行真实浏览器矩阵，不能由此推断所有页面适配有效。
- 导航文案和 href 存在版本漂移的证据：如首页/主栏目链接 `Publication2025.html`，旧新闻/论文页可能链接 `Publication2024.html` 或小写 `publications2024.html`；`all_news.html` 的合作伙伴链接曾出现 `article.html`。自动链接检查在资产清单中记录实际路径匹配。
- 部分 HTML 使用嵌套 `<p>`、硬编码像素宽度、不同年份文件命名风格；未对 DOM 进行完整规范性校验，迁移前应以模板样例确认。

## 建议复用顺序

1. **共享外壳**：`BaseLayout`、header/nav、footer、响应式容器。
2. **列表内容**：NewsCard / NewsGrid / archive entry、ResearchCard、PublicationTable。
3. **详情布局**：新闻文章与科研项目文章分开建 layout，共用媒体图/图注/元数据组件。
4. **交互控件**：Button、静态分页、导航折叠；先确定 Astro 输出和无 JavaScript 体验。

## 样本页

首页 `html/index.html`；新闻列表 `html/all_news.html` 和 `html/news/history_news.js`；新闻详情 `html/New20260923.html`（若存在，否则按新闻清单首条）；科研列表 `html/all_research.html`；论文页 `html/Publication2025.html`；团队 `html/Team.html`。路由和输入证据见 `route-map.csv`、`news-inventory.csv`。
"""
    (OUT / "component-inventory.md").write_text(component_doc, encoding="utf-8")

    # Visual baseline is explicitly source-based; no screenshots are fabricated.
    visual_doc = f"""# 当前网站视觉与功能基线（源码审阅）

## 验证范围

- 记录基于 HTML、`html/assets/css`、`html/assets/js` 的静态源码，不是浏览器截图或线上访问结果。
- 本运行环境没有 Chromium、Chrome、Firefox、Playwright 或 Selenium；未生成截图，`screenshots/README.md` 说明后续采集办法。
- 建议复测视口：桌面 1440×900、手机 390×844。当前工作未验证实际折行、图片裁切、滚动、键盘操作或外部 CDN 可用性。

## 代表页面

| 页面 | 导航与布局 | 字体/颜色/组件 | 可从源码确认的交互 | 待浏览器验证 |
|---|---|---|---|---|
| 首页 `html/index.html` | 顶部固定 Bootstrap navbar；IMCL 标题/介绍的 jumbotron；两列近期新闻卡片，后续有研究/新闻内容区 | Logo；`main.css`；Google Playfair Display + Source Sans Pro；绿色品牌色（局部 CSS 使用 `#03A87C`）、白色背景、粉/玫红 hover；圆角新闻图卡片 | 移动导航使用 Bootstrap `collapse` data attributes；7 篇最新新闻卡片硬编码在 HTML；页面加载 `history_news.js`，内联脚本消费历史新闻数据并生成列表/分页 | 1440 下 Hero 图片、首屏高度、两列卡片；390 下菜单折叠、新闻卡片堆叠；脚本加载及分页实际表现 |
| 新闻列表 `html/all_news.html` | 固定导航后是静态新闻链接列表；另保留大段注释掉的旧卡片 | 与主站共用 `main.css`；主色绿、Bootstrap link/button | 当前活动新闻项是普通 `<a>` 链接；未引用首页的 `history_news.js` | 视觉呈现、顺序/分页表现、注释内容是否需要保留 |
| 新闻详情 `html/New20260923.html`（如该页不存在则选新闻清单中的首篇） | 标题/日期/主图，正文为中央窄列，分节标题，文章后返回按钮 | Bootstrap jumbotron/container/grid；文章图片有圆角/阴影；文字行高与标题存在局部 `<style>` | 返回首页链接；菜单折叠 | 首图宽度、长标题换行、正文行长、移动端图片和按钮 |
| Research `html/all_research.html` | 固定导航；介绍/卡片式项目列表，主区域按 Bootstrap 网格呈现项目 | 绿色链接及 hover 色，项目缩略图/链接；共享 `main.css` | 项目标题链接到详情 HTML；导航链接 | 卡片数量和高度、长标题溢出、移动端列数和图片比例 |
| Publications `html/Publication2025.html` | 固定导航、年份切换、宽表格按年份筛选 | Bootstrap 主站风格与单页额外表格 CSS；标题/作者/出版物列 | 页面内 `output(jsonData)` 回调 + `output*.json` 脚本注入表格；窄屏媒体规则将表格转成块布局/隐藏表头 | 数据文件脚本加载、窄屏可读性、表头与字段标签、不同年份链接正确性 |
| Team `html/Team.html` | 固定导航；成员卡片/网格布局 | 共用 `main.css`，局部卡片 hover 边框/阴影 | 个人页面或相关链接；导航折叠 | 成员分组、卡片高度、图片比例、手机阅读顺序 |

## 共享视觉特征（源码证据）

- 站点使用 Mundana/Bootstrap 风格：`container`、`row`、`col-*`、`jumbotron`、`navbar`、`card`、`btn` 等类广泛出现。
- 多数主页面引用 `html/assets/css/main.css`，并从 CDN 请求 Google Fonts 与 Font Awesome。
- 品牌识别集中在 IMCL/GEMLab Logo、绿色主色和“智能医学计算实验室”文字；具体 Logo 文件引用各页不完全一致，迁移应保留可验证的原始资产。
- 页内存在内联 CSS 与 inline style（全站合计 `{style_block_total}` 个 `<style>` 块、`{style_attr_total}` 个 `style=` 属性），会使同一组件的间距、宽度及颜色在页面间漂移。
- 静态扫描发现 `{viewport_count}/{len(html_files)}` 个 HTML 页面具有 viewport meta；以源代码统计不能替代手机实测。

## 功能基线与可访问性待核验

- 主要导航、文章、卡片和按钮以链接实现；Bootstrap collapse 依赖 jQuery/Bootstrap JS bundle。
- 源码包含首页历史新闻列表/分页的生成逻辑及出版物 JSON 回调；浏览器实际运行、数据文件加载、分页行为、按钮/菜单触屏操作仍需验证。
- 建议检查图片 alt 文本覆盖、键盘焦点、对比度、标题顺序、表格移动端语义及 JavaScript 关闭时的回退行为；本次没有做无障碍自动化或人工浏览器审计。

## 截图索引

本次未创建截图，避免伪造渲染结果。后续安装/提供浏览器截图环境后，按以下名称保存到本目录 `screenshots/`：`home-desktop-1440x900.png`、`home-mobile-390x844.png`、`news-list-desktop-1440x900.png`、`news-detail-desktop-1440x900.png`、`research-desktop-1440x900.png`、`publications-mobile-390x844.png`、`team-desktop-1440x900.png`。使用本地只读静态服务器提供 `html/` 目录；记录浏览器版本、日期、字体网络状态和访问 URL。
"""
    (OUT / "baseline/visual-baseline.md").write_text(visual_doc, encoding="utf-8")
    screenshots_note = """# 截图状态

本次 P0 环境没有安装 Chromium/Chrome/Firefox，也没有 Playwright/Selenium，因此没有生成截图。请勿将源码审阅当成浏览器视觉验收。

后续操作：启动只读本地静态服务器（文档根目录 `html/`，不得改生产配置），浏览器分别设为 1440×900 和 390×844；按 `visual-baseline.md` 的清单截图，并记录浏览器版本、采集日期、CDN/字体是否加载。"""
    (OUT / "baseline/screenshots/README.md").write_text(screenshots_note, encoding="utf-8")

    risk_doc = """# P1–P5 重构风险清单

等级含义：高 = 会造成页面/内容/外部入口明显丢失或大面积返工；中 = 影响一组页面或需要人工修订；低 = 局部、可在常规验收中消化。建议阶段是处理窗口，不代表本 P0 已执行修复。

| 风险 | 等级 | 证据/影响 | 建议阶段 | 验证方法 |
|---|---|---|---|---|
| 独立 HTML 与重复模板导致迁移面大 | 高 | `route-map.csv` 覆盖全部 HTML；共享 nav/footer/Bootstrap 网格在多个页面重复，且局部差异并存 | P1 定模板族；P2 建公共 Layout；P3 分批迁移 | 按页面类型抽样比对导航、Hero、页脚、卡片和详情正文；迁移前后路由数量对照 |
| 新闻在详情、首页、列表和 JS 数组多处维护 | 高 | 首页卡片硬编码；`html/all_news.html` 有静态/注释内容（21 个链接指向 20 篇新闻，其中 1 篇重复）；`html/news/history_news.js` 另有 `HISTORY_NEWS` 数据；清单显示 10 篇出现在多个入口 | P2 建 Markdown collection；P3 批量迁移 | 以 `news-inventory.csv` 对照源条目；标题/日期/图/旧 URL 覆盖率须 100% 或逐项解释 |
| 新闻元数据/图片异常，自动迁移可能错配 | 高 | 日期格式不一、日期可能只在正文、首图只是启发式封面；部分列表链接可能大小写漂移 | P2 内容 schema；P3 迁移时人工复核 | 逐篇核对标题、日期、语言、封面、正文插图和 slug；按截图验收页面 |
| 旧 URL 变更造成外链与搜索流量损失 | 高 | `New*.html`、大小写混用、空格/中文路径和多个年份页面；新路由均为建议 | P1 定 route contract；P3 重定向/别名 | route-map 检查一对一/显式例外；自动生成 redirect 表；抽查旧链接 HTTP 状态及搜索索引 |
| 本地资源路径无效/大小写敏感 | 高 | 静态扫描产生的异常及大小写候选见 `asset-inventory.csv`；Linux Nginx 对大小写敏感 | P1 先修/登记已知路径；每个迁移阶段持续扫描 | Linux 环境解析所有本地 `src`/`href`/`srcset`/CSS URL，检查编码空格、中文路径；生成 404 清单 |
| JavaScript 动态引用未静态求值 | 中 | 审计只解析 HTML/CSS；JS 拼接路径、回调数据、iframe 动态加载可能未发现 | P2/P3 迁移数据交互时 | 搜索 `src=`, `location`, `fetch`, `document.write`, `innerHTML` 等动态代码；浏览器网络面板逐页确认 |
| Bootstrap/jQuery 组件与旧脚本依赖 | 中 | HTML 依赖 Bootstrap data attributes/jQuery/Popper；页面脚本顺序和插件行为可能脆弱 | P2 设计 Astro 交互策略；P4 收敛依赖 | 桌面/移动测试 nav collapse、分页、表格数据注入；禁用 JS 检查回退 |
| 出版物的数据格式与版本并存 | 高 | `.bib`、JSON、`output([...])` JS callback、年份 HTML 同时存在，字段大小写/命名不同 | P2 定 schema/importer；P3 统一迁移 | schema 校验记录数、年份、作者、标题、期刊和 DOI；与旧表逐年比较 |
| 模板/字体/图标及附件许可链不清 | 中 | Mundana README 称 MIT，而 `html/package.json` 提及 WowThemesNet License；CDN 字体/图标及 Office 文件各有来源 | P1/P2 内容和设计冻结前 | 对照实际许可证文件、外部字体/图标许可和每类图片来源；保留必要 attribution |
| Docker/Nginx 当前直接服务 `html/`，与 Astro 输出目录不匹配 | 高 | Compose bind mount `./html:/usr/share/nginx/html`；Nginx root 写死 | P4 静态构建切换 | 构建输出 smoke test、容器路径映射验证、404/资产路径检查；生产切换前在临时 compose 验证 |
| 外部 Google Fonts/Font Awesome CDN 可用性与隐私/稳定性 | 中 | 主页面直接引用 Google Fonts 和 Font Awesome CDN，网络失败会改变字体/图标表现 | P1 视觉基线；P2/P4 资源策略 | 离线/拦截 CDN 比较；审查缓存、版本、许可和隐私要求 |
| 没有浏览器截图/行为测试基线 | 中 | 当前执行环境无浏览器自动化工具；源码只能确认布局声明，不能确认实际渲染 | P1 | 在标准 Chromium 环境采集指定 desktop/mobile 截图并人工评审；建立每次迁移的视觉回归流程 |
| 疑似旧页/测试页被误删或遗漏 | 中 | `test*`、`_frame`、重复年份页和模板副本仍可能被外部链接或 iframe 使用；本任务不判废 | P1 内容 owner review；P3 route decision | 查全站 inbound link、服务日志/搜索引擎入口（若可得）、人工确认后才标“不迁移” |
| 语言混杂、HTML 结构/编码差异 | 中 | 英文页面与中文新闻/附件并存，标题日期和字符集/文件名格式不统一 | P2 schema 与 markdown 约定 | 检查 UTF-8、语言 frontmatter、中文 URL 编码、标题与摘要抽取；随机人工校对 |

## 验收门槛建议

- P1：页面/路由清单由内容负责人确认；桌面与手机视觉方向有可比较截图；保留品牌资产与字体策略确认。
- P2：Astro layout/components 有代表性原页对照；内容 schema 和资源命名约定确定。
- P3：页面、新闻、研究与出版物迁移均保留旧 URL 映射；无未解释资源 404；所有内容缺失有清单。
- P4：Docker/Nginx 使用构建输出的临时/预发布验收通过，回滚方案存在。
- P5：桌面/移动视觉回归、路由/链接检查、内容数量核对通过后再决定发布。
"""
    (OUT / "migration-risks.md").write_text(risk_doc, encoding="utf-8")

    # Consistency validation required by the P0 brief.
    expected = {
        "route-map.csv": (len(route_rows), ["legacy_path", "source_file", "page_type", "page_title", "main_heading", "inbound_internal_link_count", "site_nav_entry", "shared_structure", "associated_images", "associated_scripts", "proposed_path", "slug", "migration_priority", "status", "notes"]),
        "news-inventory.csv": (len(news_rows), ["source_file", "legacy_path", "title", "published_date_iso", "date_source", "image_directory", "cover_image_path", "related_body_images", "in_homepage", "homepage_link_count", "in_all_news", "all_news_link_count", "in_history_news_js", "history_news_link_count", "language_from_title", "slug", "proposed_path", "anomaly_or_review", "extraction_notes"]),
        "asset-inventory.csv": (len(file_rows), ["path", "category", "extension", "mime_type", "size_bytes", "sha256", "duplicate_hash_paths", "referenced_by_count", "referenced_by", "reference_status", "suggested_group", "notes"]),
    }
    validation_errors: list[str] = []
    for name, (count, fields) in expected.items():
        with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != fields: validation_errors.append(f"{name}: header mismatch")
            rows = list(reader)
            if len(rows) != count: validation_errors.append(f"{name}: expected {count} rows, got {len(rows)}")
            if any(None in row for row in rows): validation_errors.append(f"{name}: malformed CSV row")
    expected_map_sources = set(html_files)
    actual_map_sources = {str(r["source_file"]) for r in route_rows}
    if expected_map_sources != actual_map_sources: validation_errors.append("route-map coverage differs from tracked HTML set")
    news_source_set = {str(r["source_file"]) for r in news_rows}
    if len(news_source_set) != len(news_rows): validation_errors.append("news inventory has duplicate source rows")
    if collisions: validation_errors.append("proposed route collisions need explicit resolution: " + repr(collisions))
    if validation_errors:
        print("VALIDATION_FAILED")
        print("\n".join(validation_errors))
        return 2
    print(json.dumps({"tracked_files": len(files), "html_files": len(html_files), "page_types": types, "news_detail_candidates": len(news_rows), "static_reference_candidates": len(refs), "static_reference_issues": len(bad_refs), "missing_or_case_reference_rows": len(missing_rows), "sha256_duplicate_groups": len(duplicate_groups), "route_rows": len(route_rows), "news_rows": len(news_rows), "asset_rows": len(file_rows), "history_news_entries": len(history_links), "news_list_source_link_counts": news_list_source_counts, "validation": "PASS"}, ensure_ascii=False, default=dict, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
