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
    out_file="medrxiv_LungCancer_202x.json",
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


Here’s an additional section you can append to your **README.md**. It explains how to extract the PDF URLs from the JSON output file and how to use `wget` across different operating systems to download the files locally.

---

## 📥 Extracting and Downloading PDFs

Once the scraper has finished, your output file (e.g., `medrxiv_LungCancer_2020.json`) will contain metadata for all matched papers, including direct links to the PDF versions.

### 1. Extract PDF URLs
You can extract all PDF links from the JSON file using a simple Python snippet:

```python
import json

with open("medrxiv_LungCancer_2020.json", "r", encoding="utf-8") as f:
    data = json.load(f)

pdf_urls = [item["pdf"] for item in data if item.get("pdf")]
print("\n".join(pdf_urls))
```

Save this list to a text file for easier batch downloading:

```python
with open("pdf_links.txt", "w", encoding="utf-8") as f:
    for url in pdf_urls:
        f.write(url + "\n")
```

This creates a file `pdf_links.txt` containing one PDF URL per line.

---

### 2. Install `wget`

`wget` is a command-line utility for downloading files from the web. Installation differs by operating system:

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update
  sudo apt install wget
  ```

- **Linux (Fedora/CentOS/RHEL):**
  ```bash
  sudo dnf install wget
  ```
  or
  ```bash
  sudo yum install wget
  ```

- **macOS (via Homebrew):**
  ```bash
  brew install wget
  ```

- **Windows:**
  - Option 1: Install via [Chocolatey](https://chocolatey.org/):
    ```powershell
    choco install wget
    ```
  - Option 2: Download binaries from [GNU Wget for Windows](https://eternallybored.org/misc/wget/).
  - Ensure `wget.exe` is added to your system PATH.

---

### 3. Download PDFs with `wget`

Once `wget` is installed, you can download all PDFs listed in `pdf_links.txt`:

```bash
wget -i pdf_links.txt -P ./pdfs
```

- `-i pdf_links.txt` tells `wget` to read URLs from the file.
- `-P ./pdfs` saves all downloaded files into a folder named `pdfs`.

---

### 4. Notes
- If downloads are interrupted, re-run the command; `wget` will skip already downloaded files.
- To limit download speed (helpful for large batches):
  ```bash
  wget --limit-rate=200k -i pdf_links.txt -P ./pdfs
  ```
- To resume partially downloaded files:
  ```bash
  wget -c -i pdf_links.txt -P ./pdfs
  ```
