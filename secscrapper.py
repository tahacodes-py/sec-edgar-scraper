import requests
import csv
import os
import time
HEADERS = {"User-Agent": "Taha Ahmed tahaahmed@email.com"}
OUTPUT_FILE = "mega.txt"
LOG_FILE = "log.csv"
TEST_CIKS = ["0000320187", "0000320193", "0000789019"]
def fetch_submissions(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()
def build_txt_url(cik, accession):
    acc_clean = accession.replace("-", "")
    cik_plain = str(int(cik))
    return f"https://www.sec.gov/Archives/edgar/data/{cik_plain}/{acc_clean}/{accession}.txt"
def download_and_append(url, out_file):
    r = requests.get(url, headers=HEADERS, stream=True, timeout=30)
    if r.status_code == 200:
        with open(out_file, "a", encoding="utf-8", errors="ignore") as f:
            for chunk in r.iter_content(chunk_size=8192, decode_unicode=True):
                if chunk:
                    f.write(chunk)
        return True
    return False
def run(cik_list):
    with open(LOG_FILE, "w", newline="") as log:
        writer = csv.writer(log)
        writer.writerow(["CIK", "Accession", "Status"])
        for cik in cik_list:
            print(f"\nProcessing CIK: {cik}")
            try:
                data = fetch_submissions(cik)
                filings = data.get("filings", {}).get("recent", {})
                accessions = filings.get("accessionNumber", [])
                print(f"  Found {len(accessions)} filings")

                for acc in accessions[:5]:  # limit to 5 per CIK for test run
                    url = build_txt_url(cik, acc)
                    print(f"  Downloading: {acc}")
                    try:
                        success = download_and_append(url, OUTPUT_FILE)
                        status = "done" if success else "failed"
                    except Exception as e:
                        status = f"error: {e}"
                    writer.writerow([cik, acc, status])
                    print(f"  Status: {status}")
                    time.sleep(0.5)  # be polite to SEC servers

            except Exception as e:
                print(f"  Failed to fetch submissions: {e}")
                writer.writerow([cik, "N/A", f"submissions_error: {e}"])
    print(f"\nDone. Output: {OUTPUT_FILE} | Log: {LOG_FILE}")
if __name__ == "__main__":
    run(TEST_CIKS)