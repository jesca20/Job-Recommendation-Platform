import pandas as pd
import os

applications_file = "data/applications.csv"

# Initialize file if not exists
if not os.path.exists(applications_file):
    pd.DataFrame(columns=["title", "company", "url", "status", "score"]).to_csv(applications_file, index=False)

def save_application(job, status, score):
    df = pd.read_csv(applications_file)
    new_entry = {
        "title": job["title"],
        "company": job["company"],
        "url": job["url"],
        "status": status,
        "score": score
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(applications_file, index=False)

def get_applications():
    return pd.read_csv(applications_file)
