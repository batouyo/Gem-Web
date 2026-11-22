# Google Scholar bulk collection

The publications snapshot is refreshed in a manual, roughly six-month cycle for Tao Tan's Google Scholar profile. The collector uses the SerpApi Google Scholar Author API and reads its key from `SERPAPI_API_KEY`.

From the repository root, run:

```sh
export SERPAPI_API_KEY="<your SerpApi key>"
python3 scripts/publications/fetch_scholar.py
```

The first run requests pages of 100 articles until there is no next page. Successful raw responses and progress are stored in `raw/<run-id>/`. Raw responses retain all years. Cleaned JSON/CSV/report output keeps only articles with a publication year of 2021 or later; records with a missing or unrecognized year are excluded from those files and counted in the report.

If a run stops, running the command again resumes the latest incomplete run from its cached pages. Use `--resume <run-id>` to select a specific run, `--resume` to explicitly resume the latest incomplete run, or `--new-run` to start a separate crawl. To rebuild cleaned output from an already completed raw run without making API requests, run `python3 scripts/publications/fetch_scholar.py --clean-existing` (or pass a run ID).

Completed crawls update `publications.json`, `publications.csv`, and `fetch-report.md`. These files are not replaced until every page has been fetched successfully. A new crawl compares citation IDs and citation counts against the previous complete JSON snapshot using the same year filter.

The default limit is 20 HTTP attempts per crawl, including retries. To change it, pass `--max-requests N`; `0` removes the client-side limit. A stopped crawl can resume after increasing the limit. Timeout and transient retry settings are configurable with `--timeout` and `--retries`.

The structured JSON deduplicates by `citation_id` and keeps duplicate occurrences in `duplicate_records`. The CSV retains every raw article occurrence and adds review columns for repeated citation IDs and possible same-title, same-year matches. Missing source fields remain empty.
