import pandas as pd
import re
import os

os.makedirs("data", exist_ok=True)

df = pd.read_csv("data/raw_jobs.csv")

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df["title"] = df["title"].fillna("Unknown")
df["company"] = df["company"].fillna("Unknown")
df["location"] = df["location"].fillna("Remote/Not Specified")
df["salary"] = df["salary"].fillna("Not Provided")
df["skills"] = df["skills"].fillna("")
df["date_posted"] = df["date_posted"].fillna("Unknown")

# Standardize location text
df["location"] = df["location"].str.strip().str.title()

# Work type flag
df["work_type"] = df["location"].apply(
    lambda x: "Remote" if "remote" in x.lower() else "Region-Specific Remote"
)

# Clean salary text
def extract_salary_numbers(salary_text):
    text = str(salary_text)
    numbers = re.findall(r"\d[\d,]*", text)
    if len(numbers) >= 2:
        return f"{numbers[0]} - {numbers[1]}"
    elif len(numbers) == 1:
        return numbers[0]
    return None

df["salary_clean"] = df["salary"].apply(extract_salary_numbers)

# Split and normalize skills
def normalize_skills(skill_text):
    parts = [s.strip() for s in str(skill_text).split(",") if s.strip()]
    return ", ".join(sorted(set(parts)))

df["skills_clean"] = df["skills"].apply(normalize_skills)

# Detect key portfolio skills
target_skills = ["Python", "SQL", "Excel", "Power BI", "Tableau", "AWS", "R"]

def detect_target_skills(row):
    combined_text = f"{row['title']} {row['skills_clean']}".lower()
    found = [skill for skill in target_skills if skill.lower() in combined_text]
    return ", ".join(found)

df["detected_skills"] = df.apply(detect_target_skills, axis=1)

df.to_csv("data/cleaned_jobs.csv", index=False)
print(f"Saved cleaned dataset with {len(df)} rows to data/cleaned_jobs.csv")