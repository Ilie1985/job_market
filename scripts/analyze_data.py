import pandas as pd
import matplotlib.pyplot as plt
import os
import re

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

def salary_midpoint(value):
    if pd.isna(value):
        return None
    nums = re.findall(r"\d+", str(value).replace(",", ""))
    nums = [int(n) for n in nums]
    if len(nums) >= 2:
        return (nums[0] + nums[1]) / 2
    elif len(nums) == 1:
        return nums[0]
    return None

df["salary_mid"] = df["salary_clean"].apply(salary_midpoint)
salary_data = df["salary_mid"].dropna()

if not salary_data.empty:
    plt.figure(figsize=(10, 6))
    salary_data.plot(kind="hist", bins=15)
    plt.title("Salary Distribution")
    plt.xlabel("Estimated Salary")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("outputs/salary_histogram.png")
    plt.close()

    print("\nSalary summary:")
    print(f"Rows with usable salary data: {salary_data.shape[0]}")
    print(f"Minimum estimated salary: {salary_data.min()}")
    print(f"Maximum estimated salary: {salary_data.max()}")
    print(f"Average estimated salary: {round(salary_data.mean(), 2)}")
else:
    print("\nNo usable salary data available for histogram.")