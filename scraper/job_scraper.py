import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_remoteok():
    url = "https://remoteok.io/remote-dev-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch jobs: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")
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
        except Exception:
            continue

    if not jobs:
        return pd.DataFrame()

    df = pd.DataFrame(jobs)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/jobs.csv", index=False, encoding="utf-8")
    return df
