from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import os
import time

URL = "https://remoteok.com/remote-dev-jobs"

def run_selenium_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    time.sleep(5)

    jobs = []

    cards = driver.find_elements(By.CSS_SELECTOR, "tr.job")

    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h2").text
        except:
            title = None

        try:
            company = card.find_element(By.CSS_SELECTOR, "h3").text
        except:
            company = None

        try:
            location = card.find_element(By.CSS_SELECTOR, ".location").text
        except:
            location = None

        try:
            salary = card.find_element(By.CSS_SELECTOR, ".salary").text
        except:
            salary = None

        try:
            date_posted = card.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
        except:
            date_posted = None

        try:
            tags = card.find_elements(By.CSS_SELECTOR, ".tag")
            skills = ", ".join([tag.text for tag in tags if tag.text.strip()])
        except:
            skills = ""

        if title or company:
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "skills": skills,
                "date_posted": date_posted,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": URL
            })

    driver.quit()
    return pd.DataFrame(jobs)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = run_selenium_scraper()
    df.to_csv("data/raw_jobs.csv", index=False)
    print(f"Saved {len(df)} rows to data/raw_jobs.csv")