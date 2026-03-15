# import pandas as pd
# import re
# import os

# os.makedirs("data", exist_ok=True)

# df = pd.read_csv("data/raw_jobs.csv")

# # Remove duplicates
# df = df.drop_duplicates()

# # Handle missing values
# df["title"] = df["title"].fillna("Unknown")
# df["company"] = df["company"].fillna("Unknown")
# df["location"] = df["location"].fillna("Remote/Not Specified")
# df["salary"] = df["salary"].fillna("Not Provided")
# df["skills"] = df["skills"].fillna("")
# df["date_posted"] = df["date_posted"].fillna("Unknown")

# # Standardize location text
# df["location"] = df["location"].str.strip().str.title()

# # Work type flag
# df["work_type"] = df["location"].apply(
#     lambda x: "Remote" if "remote" in x.lower() else "Region-Specific Remote"
# )

# # Clean salary text
# def extract_salary_numbers(salary_text):
#     text = str(salary_text)
#     numbers = re.findall(r"\d[\d,]*", text)
#     if len(numbers) >= 2:
#         return f"{numbers[0]} - {numbers[1]}"
#     elif len(numbers) == 1:
#         return numbers[0]
#     return None

# df["salary_clean"] = df["salary"].apply(extract_salary_numbers)

# # Split and normalize skills
# def normalize_skills(skill_text):
#     parts = [s.strip() for s in str(skill_text).split(",") if s.strip()]
#     return ", ".join(sorted(set(parts)))

# df["skills_clean"] = df["skills"].apply(normalize_skills)

# # Detect key portfolio skills
# target_skills = ["Python", "SQL", "Excel", "Power BI", "Tableau", "AWS", "R"]

# def detect_target_skills(row):
#     combined_text = f"{row['title']} {row['skills_clean']}".lower()
#     found = [skill for skill in target_skills if skill.lower() in combined_text]
#     return ", ".join(found)

# df["detected_skills"] = df.apply(detect_target_skills, axis=1)

# df.to_csv("data/cleaned_jobs.csv", index=False)
# print(f"Saved cleaned dataset with {len(df)} rows to data/cleaned_jobs.csv")

import pandas as pd
import re
import os

os.makedirs("data", exist_ok=True)

df = pd.read_csv("data/raw_jobs.csv")

# ---------------------------
# 1. Keep original row count
# ---------------------------
original_rows = len(df)

# ---------------------------
# 2. Remove duplicates
# ---------------------------
df = df.drop_duplicates()
rows_after_dedup = len(df)

# ---------------------------
# 3. Handle missing values
# ---------------------------
df["title"] = df["title"].fillna("Unknown")
df["company"] = df["company"].fillna("Unknown")
df["location"] = df["location"].fillna("Unknown")
df["salary"] = df["salary"].fillna("Not Provided")
df["skills"] = df["skills"].fillna("")
df["date_posted"] = df["date_posted"].fillna("Unknown")

# ---------------------------
# 4. Standardize text fields
# ---------------------------
df["title"] = df["title"].astype(str).str.strip()
df["company"] = df["company"].astype(str).str.strip()
df["location"] = df["location"].astype(str).str.strip()
df["salary"] = df["salary"].astype(str).str.strip()
df["skills"] = df["skills"].astype(str).str.strip()

# ---------------------------
# 5. Standardize location
# ---------------------------
def standardize_location(location_text):
    text = str(location_text).strip().lower()

    if text in ["", "unknown", "not provided"]:
        return "Unknown"

    if "remote/not specified" in text:
        return "Global Remote"
    if text == "remote":
        return "Global Remote"
    if "remote - us" in text or "remote, united states" in text or "us remote" in text:
        return "US Remote"
    if "united states" in text and "remote" in text:
        return "US Remote"
    if "uk remote" in text or "remote - uk" in text:
        return "UK Remote"
    if "europe" in text and "remote" in text:
        return "Europe Remote"
    if "remote" in text:
        return "Other Remote"

    return location_text.strip().title()

df["location_clean"] = df["location"].apply(standardize_location)

# ---------------------------
# 6. Create cleaner work type
# ---------------------------
def assign_work_type(location_clean):
    text = str(location_clean).lower()
    if "remote" in text:
        return "Remote"
    elif text == "unknown":
        return "Unknown"
    return "Location-Specific"

df["work_type"] = df["location_clean"].apply(assign_work_type)

# ---------------------------
# 7. Parse salary safely
# ---------------------------
def parse_salary_range(salary_text):
    text = str(salary_text).lower().replace(",", "").strip()

    # treat obvious missing values as missing
    if text in ["", "not provided", "unknown", "none", "nan"]:
        return pd.Series([None, None, None, False])

    numbers = re.findall(r"\d+", text)
    numbers = [int(n) for n in numbers]

    if len(numbers) == 0:
        return pd.Series([None, None, None, False])

    salary_min = None
    salary_max = None
    salary_mid = None

    if len(numbers) >= 2:
        salary_min = numbers[0]
        salary_max = numbers[1]
    elif len(numbers) == 1:
        salary_min = numbers[0]
        salary_max = numbers[0]

    # invalid if zero or negative
    if salary_min is None or salary_max is None:
        return pd.Series([None, None, None, False])

    if salary_min <= 0 or salary_max <= 0:
        return pd.Series([None, None, None, False])

    # swap if reversed
    if salary_min > salary_max:
        salary_min, salary_max = salary_max, salary_min

    # unrealistic filtering
    # adjust if needed for your project
    if salary_min < 10000 or salary_max > 1000000:
        return pd.Series([None, None, None, False])

    salary_mid = (salary_min + salary_max) / 2
    return pd.Series([salary_min, salary_max, salary_mid, True])

df[["salary_min_num", "salary_max_num", "salary_mid", "salary_valid"]] = df["salary"].apply(parse_salary_range)

# ---------------------------
# 8. Clean general tags/skills
# ---------------------------
def normalize_tags(skill_text):
    parts = [s.strip().lower() for s in str(skill_text).split(",") if s.strip()]
    parts = sorted(set(parts))
    return ", ".join(parts)

df["skills_clean"] = df["skills"].apply(normalize_tags)

# ---------------------------
# 9. Separate technical vs descriptive tags
# ---------------------------
technical_skill_keywords = [
    "python", "sql", "excel", "power bi", "tableau", "aws", "azure", "gcp",
    "spark", "pandas", "numpy", "scikit-learn", "machine learning", "etl",
    "postgresql", "mysql", "sqlite", "docker", "kubernetes", "git", "linux",
    "java", "javascript", "typescript", "react", "node", "r", "scala", "hadoop",
    "airflow", "snowflake", "dbt", "terraform", "api", "mongodb", "redis"
]

descriptive_tag_keywords = [
    "senior", "lead", "junior", "support", "technical", "design", "digital nomad",
    "health", "software", "engineer", "engineering", "full-stack", "full stack",
    "manager", "founder", "executive", "backend", "frontend", "mobile", "marketing"
]

def detect_technical_skills(row):
    combined_text = f"{row['title']} {row['skills_clean']}".lower()
    found = [skill for skill in technical_skill_keywords if skill in combined_text]
    return ", ".join(sorted(set(found)))

def detect_descriptive_tags(row):
    combined_text = f"{row['title']} {row['skills_clean']}".lower()
    found = [tag for tag in descriptive_tag_keywords if tag in combined_text]
    return ", ".join(sorted(set(found)))

df["technical_skills_detected"] = df.apply(detect_technical_skills, axis=1)
df["descriptive_tags_detected"] = df.apply(detect_descriptive_tags, axis=1)

# Keep your old column too if you still want it
df["detected_skills"] = df["technical_skills_detected"]

# ---------------------------
# 10. Reorder useful columns
# ---------------------------
preferred_columns = [
    "title",
    "company",
    "location",
    "location_clean",
    "work_type",
    "salary",
    "salary_min_num",
    "salary_max_num",
    "salary_mid",
    "salary_valid",
    "skills",
    "skills_clean",
    "technical_skills_detected",
    "descriptive_tags_detected",
    "date_posted",
    "scraped_at",
    "source"
]

existing_columns = [col for col in preferred_columns if col in df.columns]
df = df[existing_columns]

# ---------------------------
# 11. Save cleaned file
# ---------------------------
df.to_csv("data/cleaned_jobs.csv", index=False)

# ---------------------------
# 12. Data quality summary
# ---------------------------
print("\n=== DATA CLEANING SUMMARY ===")
print(f"Original rows: {original_rows}")
print(f"Rows after duplicate removal: {rows_after_dedup}")
print(f"Duplicates removed: {original_rows - rows_after_dedup}")

print("\n=== MISSING VALUES ===")
print(df.isna().sum())

print("\n=== SALARY QUALITY ===")
print(f"Rows with valid salary data: {df['salary_valid'].sum()}")
print(f"Rows with invalid/missing salary data: {(~df['salary_valid']).sum() if df['salary_valid'].dtype == bool else df['salary_valid'].isna().sum()}")

if df["salary_valid"].sum() > 0:
    print(f"Minimum valid salary: {df.loc[df['salary_valid'], 'salary_min_num'].min()}")
    print(f"Maximum valid salary: {df.loc[df['salary_valid'], 'salary_max_num'].max()}")
    print(f"Average salary midpoint: {round(df.loc[df['salary_valid'], 'salary_mid'].mean(), 2)}")

print("\n=== LOCATION QUALITY ===")
print(df["location_clean"].value_counts().head(10))

print("\n=== TOP TECHNICAL SKILLS ===")
technical_series = df["technical_skills_detected"].replace("", pd.NA).dropna().str.split(", ")
technical_exploded = technical_series.explode()
print(technical_exploded.value_counts().head(10))

print("\n=== TOP DESCRIPTIVE TAGS ===")
desc_series = df["descriptive_tags_detected"].replace("", pd.NA).dropna().str.split(", ")
desc_exploded = desc_series.explode()
print(desc_exploded.value_counts().head(10))

print(f"\nSaved cleaned dataset with {len(df)} rows to data/cleaned_jobs.csv")