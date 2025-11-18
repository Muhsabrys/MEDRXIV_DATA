# medRxiv Scraper

This project provides a Python script to **scrape metadata of preprints from [medRxiv](https://www.medrxiv.org/)** based on user-defined keywords. It retrieves paper titles, DOIs, authors, publication dates, and generates links to the article and PDF.

---

## 📌 Features
- Reads a list of API endpoints from a text file (`loop.txt`).
- Queries medRxiv’s JSON API for preprints within a given date range.
- Filters papers by keywords in their titles (e.g., *Lung Cancer*, *adenocarcinoma*).
- Avoids duplicates by tracking DOIs.
- Saves results incrementally to a JSON file for resuming later.
- Configurable delay between requests to avoid overwhelming the API.

---

## 📂 Project Structure
```
.
├── loop.txt                  # List of medRxiv API URLs
├── scraper.py                # Main Python script
├── medrxiv_LungCancer_2020.json   # Example output file
└── README.md                 # Documentation
```

---

## ⚙️ Requirements
- Python 3.7+
- Libraries:
  - `requests`
  - `json` (built-in)
  - `os` (built-in)
  - `time` (built-in)

Install dependencies:
```bash
pip install requests
```

---

## 📄 Input File (`loop.txt`)
The script expects a text file containing API URLs. Example:

```
API_URL
https://api.medrxiv.org/details/medrxiv/2020-01-01/2020-12-31/0/json
https://api.medrxiv.org/details/medrxiv/2020-01-01/2020-12-31/100/json
https://api.medrxiv.org/details/medrxiv/2020-01-01/2020-12-31/200/json
...
```

- The first line (`API_URL`) is ignored.
- Each subsequent line is an API endpoint.

---

## ▶️ Usage
Run the script directly:

```bash
python scraper.py
```

By default, it will:
- Read URLs from `loop.txt`
- Search for keywords: `"Lung Cancer"`, `"lung carcinoma"`, `"adenocarcinoma"`
- Save results to `medrxiv_LungCancer_2020.json`

---

## 🔧 Customization
You can change parameters by editing the function call in `scraper.py`:

```python
scrape_medrxiv_from_file(
    url_file="loop.txt",
    keywords=("alzheimer", "dementia"),   # Replace with your keywords
    out_file="medrxiv_alzheimer_dementia_202x.json",
    delay=1.0
)
```

- **`url_file`**: Path to the file containing API URLs.
- **`keywords`**: Tuple of keywords to match in paper titles.
- **`out_file`**: Output JSON file to store matched papers.
- **`delay`**: Delay (in seconds) between requests.

---

## 📊 Output Format
The script saves results in JSON with the following fields:

```json
[
  {
    "title": "Example Paper Title",
    "doi": "10.1101/2020.01.01.123456",
    "authors": ["Author A", "Author B"],
    "date": "2020-05-01",
    "version": "1",
    "url": "https://www.medrxiv.org/content/10.1101/2020.01.01.123456v1",
    "pdf": "https://www.medrxiv.org/content/10.1101/2020.01.01.123456v1.full.pdf"
  }
]
```

---

## ✅ Notes
- The script resumes from existing output files, so you can stop and restart without losing progress.
- Ensure your keyword list is lowercase-insensitive (the script handles case automatically).
- Respect medRxiv’s API by keeping a reasonable delay between requests.
