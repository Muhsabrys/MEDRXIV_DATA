```markdown
# MEDRXIV_DATA

A small toolkit to scrape medRxiv records (via medRxiv API pages listed in loop.txt), filter papers by title keywords, save matched records to JSON, and generate PDF download links. This repository contains a Python scraper and the URL list used for scraping.

Contents
- Obain_URLs.py — Python scraper that reads API URLs from `loop.txt`, filters papers by keywords in the title, and writes matched records to a JSON file.
- loop.txt — A list of medRxiv API page URLs (one per line). The scraper reads this file to request each page.
- README.md — This file: explains the repository, how the code works, and how to download PDFs.

Overview of the scraper (Obain_URLs.py)
- Purpose: Visit each medRxiv API URL in `loop.txt`, parse the JSON response, and collect records whose titles contain any of the specified keywords. Matched records are saved to a JSON file (so you can resume work later).
- Key behavior:
  - Reads `loop.txt` and ignores empty lines and lines starting with the string `API_URL`.
  - Requests each URL with requests.get(url).
  - Expects the response to be JSON and to contain a top-level "collection" array with paper objects.
  - For each paper in the collection, checks whether the title contains any of the given keywords (case-insensitive substring match).
  - Avoids duplicates by tracking seen DOIs. If a DOI is already recorded, subsequent records with the same DOI are skipped.
  - Builds per-paper metadata and stores it in the output JSON. Fields included for each matched paper:
    - title — paper title
    - doi — the paper DOI as returned by the API (used to build content and PDF URLs)
    - authors — authors list (from API)
    - date — date metadata from the API
    - version — version number (from API)
    - url — constructed human-facing URL: https://www.medrxiv.org/content/{doi}v{version}
    - pdf — constructed PDF URL: https://www.medrxiv.org/content/{doi}v{version}.full.pdf
  - Supports resuming: if the out_file already exists, it loads prior matches and resumes, skipping DOIs already seen.
  - Saves progress after processing each page so partial progress is preserved.
  - Sleeps for `delay` seconds between page requests.

How the PDF download works (pattern)
- The script constructs PDF URLs using the DOI and version like:
  - https://www.medrxiv.org/content/{doi}v{version}.full.pdf
- Once you have the JSON output file from the scraper (e.g., `medrxiv_alzheimer_dementia_202x.json`), extract `.pdf` fields and download them with wget or another tool.

Quick usage instructions

1) Requirements
- Python 3.7+ recommended
- pip install requests
- (Optional) jq for command-line JSON parsing

2) Running the scraper
- Edit `loop.txt` to include medRxiv API page URLs (one per line).
- Optional: Edit the keyword tuple and output name at the bottom of `Obain_URLs.py` or call scrape_medrxiv_from_file with your arguments.
- Example (run directly):
  ```bash
  python Obain_URLs.py
  ```
  The script's default call in the file uses:
  - keywords=("alzheimer", "dementia")
  - out_file="medrxiv_alzheimer_dementia_202x.json"
  - delay=1.0

3) Changing keywords or the output file
- Open `Obain_URLs.py` and edit the call to `scrape_medrxiv_from_file(...)` at the bottom, or import the function and call it from another script with your parameters.

4) Extract PDF URLs and download with wget
- If you have jq installed, extract direct PDF links from the JSON:
  ```bash
  jq -r '.[] | select(.pdf != null) | .pdf' medrxiv_alzheimer_dementia_202x.json > pdf_links.txt
  ```
- Then download with wget, allowing resume (-c) and saving into a directory `pdfs/`:
  ```bash
  mkdir -p pdfs
  wget -c -i pdf_links.txt -P pdfs/
  ```
- If you prefer Python for the download step, you can parse the JSON and download files programmatically (or use requests/wget wrappers).

Notes, caveats, and suggestions
- DOI uniqueness and versions:
  - The script uses DOI to deduplicate; different versions of the same DOI may have the same DOI string but different "version" fields. The code currently treats DOI as unique regardless of version. If you want to store multiple versions, change dedup logic to consider (doi, version).
- Rate limits and politeness:
  - Keep a reasonable delay between requests (the script uses `delay=1.0` by default). If you do many requests, increase the delay to avoid overloading the server.
- Error handling:
  - The script prints a message and skips pages with non-200 responses. You may want to add retry logic for transient errors.
- Input assumptions:
  - `loop.txt` should contain valid medRxiv API JSON endpoint URLs that return JSON with a "collection" array. The file appears to be the source of API endpoints (the repository contains a substantial `loop.txt` list).
- Resuming:
  - The script will safely resume if the out_file exists — it loads the JSON and continues adding unmatched DOIs.

Suggested improvements (small roadmap ideas)
- Use a robust logging framework (python logging) rather than print statements.
- Add CLI arguments (argparse) to configure url_file, out_file, keywords, delay, and resume options.
- Add exponential backoff/retries on 5xx errors or network errors.
- Consider writing per-page output files or using a database / SQLite for very large runs.
- Make download step optional and implement PDF downloads directly in the script (with retry and chunked downloads).

Repository owner / attribution
- This repository belongs to Muhsabrys (the GitHub user provided). Please check the repository for license and contact details if you plan to publish results.

If you want, I can also:
- produce a small dedicated download script that reads the output JSON and downloads PDFs with retries, or
- convert the script to a CLI with argparse so you can pass keywords and filenames from the command line.

```
```
