import pandas as pd
import os

APPLICATION_FILE = "data/applications.csv"

# Save application to CSV
def save_application(title, company, url, status="Applied"):
    new_entry = {
        'title': title,
        'company': company,
        'url': url,
        'status': status
    }

    # Load existing or create new DataFrame
    if os.path.exists(APPLICATION_FILE):
        df = pd.read_csv(APPLICATION_FILE)
    else:
        df = pd.DataFrame(columns=['title', 'company', 'url', 'status'])

    # Append and save
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(APPLICATION_FILE, index=False)

# Get all tracked applications
def get_applications():
    if os.path.exists(APPLICATION_FILE):
        return pd.read_csv(APPLICATION_FILE)
    return pd.DataFrame(columns=['title', 'company', 'url', 'status'])

# Update application status (optional)
def update_application_status(title, company, new_status):
    if os.path.exists(APPLICATION_FILE):
        df = pd.read_csv(APPLICATION_FILE)
        mask = (df['title'] == title) & (df['company'] == company)
        df.loc[mask, 'status'] = new_status
        df.to_csv(APPLICATION_FILE, index=False)
