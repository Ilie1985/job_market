import requests
import pandas as pd
from datetime import datetime
import os

URL = "https://remoteok.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-GB,en;q=0.9",
}

def extract_jobs():
    response = requests.get(URL, headers=HEADERS, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    data = response.json()
    jobs = []

    # Skip metadata row if present
    for item in data[1:]:
        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")

        if salary_min and salary_max:
            salary = f"{salary_min} - {salary_max}"
        elif salary_min:
            salary = str(salary_min)
        elif salary_max:
            salary = str(salary_max)
        else:
            salary = None

        jobs.append({
            "title": item.get("position"),
            "company": item.get("company"),
            "location": item.get("location"),
            "salary": salary,
            "skills": ", ".join(item.get("tags", [])) if item.get("tags") else "",
            "date_posted": item.get("date"),
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": item.get("url")
        })

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    df = extract_jobs()
    df.to_csv("data/raw_jobs.csv", index=False)

    print(df.head())
    print(f"\nSaved {len(df)} rows to data/raw_jobs.csv")