import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/cleaned_jobs.csv")

# ---------------------------
# Top skills
# ---------------------------
skills_series = df["skills_clean"].dropna().str.split(", ")
all_skills = skills_series.explode()
top_skills = all_skills.value_counts().head(10)

print("\nTop 10 skills:")
print(top_skills)

plt.figure(figsize=(10, 6))
top_skills.plot(kind="bar")
plt.title("Top 10 Skills in Remote OK Job Listings")
plt.xlabel("Skill")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/top_skills.png")
plt.close()

# ---------------------------
# Jobs by location
# ---------------------------
top_locations = df["location"].value_counts().head(10)

print("\nTop 10 locations:")
print(top_locations)

plt.figure(figsize=(10, 6))
top_locations.plot(kind="bar")
plt.title("Top 10 Job Locations")
plt.xlabel("Location")
plt.ylabel("Number of Jobs")
plt.tight_layout()
plt.savefig("outputs/jobs_by_city.png")
plt.close()

# ---------------------------
# Remote vs non-remote
# ---------------------------
work_counts = df["work_type"].value_counts()

print("\nWork type distribution:")
print(work_counts)

plt.figure(figsize=(7, 7))
work_counts.plot(kind="pie", autopct="%1.1f%%")
plt.title("Remote vs Region-Specific Remote Jobs")
plt.ylabel("")
plt.tight_layout()
plt.savefig("outputs/remote_vs_nonremote.png")
plt.close()

# ---------------------------
# Roles mentioning key skills
# ---------------------------
for skill in ["Python", "SQL", "Excel", "Power BI"]:
    count = df["detected_skills"].fillna("").str.contains(skill, case=False).sum()
    print(f"\nJobs mentioning {skill}: {count}")

# ---------------------------
# Salary mentions
# ---------------------------
salary_available = df["salary_clean"].notna().sum()
print(f"\nRows with salary info: {salary_available}")