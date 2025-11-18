#This is to download all papers from medRxiv whose titles contain any of the following terms: "Lung Cancer," "lung carcinoma," or "adenocarcinoma."


import requests
import json
import time
import os

def scrape_medrxiv_from_file(
    url_file="loop.txt",
    keywords=("Lung Cancer", "lung carcinoma", "lung carcinoma", "adenocarcinoma"),
    out_file="medrxiv_LungCancer_2020.json",
    delay=1.0
):
    matched = []
    seen_dois = set()

    # If we already have partial results, resume
    if os.path.exists(out_file):
        with open(out_file, "r", encoding="utf-8") as f:
            matched = json.load(f)
        seen_dois = {item["doi"] for item in matched if "doi" in item}
        print(f"Loaded {len(matched)} matched records from '{out_file}' (unique DOIs: {len(seen_dois)})")

    # Read URL list
    with open(url_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("API_URL")]

    print(f"Found {len(urls)} URLs in '{url_file}'.")

    # Loop over all URLs
    for i, url in enumerate(urls, start=1):
        print(f"\n[{i}/{len(urls)}] Requesting: {url}")
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"⚠️ HTTP {resp.status_code} error — skipping this URL.")
            continue

        data = resp.json()
        papers = data.get("collection", [])
        print(f"Retrieved {len(papers)} records from this page.")

        added_this_page = 0
        for paper in papers:
            title = paper.get("title", "")
            if title and any(kw.lower() in title.lower() for kw in keywords):
                doi = paper.get("doi", "")
                if doi and doi not in seen_dois:
                    version = paper.get("version", "")
                    matched.append({
                        "title": title,
                        "doi": doi,
                        "authors": paper.get("authors"),
                        "date": paper.get("date"),
                        "version": version,
                        "url": f"https://www.medrxiv.org/content/{doi}v{version}" if doi and version else None,
                        "pdf": f"https://www.medrxiv.org/content/{doi}v{version}.full.pdf" if doi and version else None
                    })
                    seen_dois.add(doi)
                    added_this_page += 1

        print(f"✅ Added {added_this_page} new matched records this page. Total matched so far = {len(matched)}")

        # Save progress
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(matched, f, indent=2, ensure_ascii=False)
        print(f"💾 Progress saved to '{out_file}'.")

        time.sleep(delay)

    print("\n✅ Finished scraping all URLs.")
    print(f"Total unique matched records: {len(matched)}")

if __name__ == "__main__":
    scrape_medrxiv_from_file(
        url_file="loop.txt",
        keywords=("alzheimer", "dementia"),
        out_file="medrxiv_LungCancer_202x.json",
        delay=1.0
    )
