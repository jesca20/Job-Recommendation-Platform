import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_remoteok():
    url = "https://remoteok.io/remote-dev-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Failed to fetch jobs, status: {r.status_code}")
        return
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    for row in soup.find_all("tr", class_="job"):
        try:
            title = row.find("h2").text.strip()
            company = row.find("h3").text.strip()
            tags = [tag.text.strip() for tag in row.find_all("div", class_="tag")]
            link = "https://remoteok.io" + row.get("data-href", "")
            jobs.append({
                "title": title,
                "company": company,
                "tags": str(tags),
                "url": link
            })
        except:
            continue

    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(jobs)
    df.to_csv("data/jobs.csv", index=False, encoding="utf-8")
    print("Saved jobs.csv with", len(jobs), "jobs")

if __name__ == "__main__":
    scrape_remoteok()
