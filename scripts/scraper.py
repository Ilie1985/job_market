import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import time

URL = "https://remoteok.com/remote-dev-jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-GB,en;q=0.9",
}

def safe_text(element):
    return element.get_text(strip=True) if element else None

def extract_jobs():
    response = requests.get(URL, headers=HEADERS, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Remote OK commonly uses table/list style job rows.
    # We try several selector patterns so your scraper is more robust.
    job_cards = soup.select("tr.job") or soup.select("table#jobsboard tr") or soup.select("article")

    for card in job_cards:
        title = None
        company = None
        location = None
        salary = None
        date_posted = None
        skills = []

        # Try multiple selectors because website markup can vary
        title_el = (
            card.select_one("h2")
            or card.select_one(".company_and_position [itemprop='title']")
            or card.select_one(".position")
        )

        company_el = (
            card.select_one("h3")
            or card.select_one("[itemprop='name']")
            or card.select_one(".companyLink h3")
        )

        location_el = (
            card.select_one(".location")
            or card.select_one("[title*='location']")
            or card.select_one(".region")
        )

        salary_el = (
            card.select_one(".salary")
            or card.select_one("[data-id='salary']")
            or card.select_one(".compensation")
        )

        date_el = (
            card.select_one("time")
            or card.select_one(".time")
            or card.select_one("[datetime]")
        )

        tag_elements = card.select(".tag") or card.select(".tags h3") or card.select(".tags span")

        title = safe_text(title_el)
        company = safe_text(company_el)
        location = safe_text(location_el)
        salary = safe_text(salary_el)
        date_posted = date_el.get("datetime") if date_el and date_el.has_attr("datetime") else safe_text(date_el)
        skills = [tag.get_text(strip=True) for tag in tag_elements if tag.get_text(strip=True)]

        # Skip empty rows
        if not title and not company:
            continue

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "skills": ", ".join(skills),
            "date_posted": date_posted,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": URL
        })

        time.sleep(0.2)  # small delay for respectful scraping

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    df = extract_jobs()
    df.to_csv("data/raw_jobs.csv", index=False)

    print(df.head())
    print(f"\nSaved {len(df)} rows to data/raw_jobs.csv")