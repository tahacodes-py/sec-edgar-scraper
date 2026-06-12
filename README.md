# SEC EDGAR Bulk Filing Scraper

A Python tool that retrieves company filing data from the SEC's public EDGAR API and merges raw filing documents into a single combined output file.

## What it does
- Takes a list of company CIK numbers
- Fetches each company's filing history via SEC's submissions API
- Generates direct URLs to raw filing documents
- Downloads and merges filing contents into a single output file
- Logs the status of every record (completed, failed, skipped, duplicate)
- Streams data efficiently to handle large-scale retrieval without memory issues

## How to run
```bash
pip install requests
python secscraper.py
```

## Output
- `mega.txt` — combined filing contents (4500+ lines from test run)
- `log.csv` — status log for every processed record
