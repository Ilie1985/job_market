import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/cleaned_jobs.csv")

# ---------------------------
# Top technical skills
# ---------------------------
technical_series = df["technical_skills_detected"].replace("", pd.NA).dropna().str.split(", ")
technical_exploded = technical_series.explode()
top_technical_skills = technical_exploded.value_counts().head(10)

print("\nTop 10 technical skills:")
print(top_technical_skills)

plt.figure(figsize=(10, 6))
top_technical_skills.plot(kind="bar")
plt.title("Top 10 Technical Skills")
plt.xlabel("Technical Skill")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/top_skills.png")
plt.close()

# ---------------------------
# Top locations
# ---------------------------
top_locations = df["location_clean"].value_counts().head(10)

print("\nTop 10 cleaned locations:")
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
plt.title("Remote vs Region-Specific / Unknown Jobs")
plt.ylabel("")
plt.tight_layout()
plt.savefig("outputs/remote_vs_nonremote.png")
plt.close()

# ---------------------------
# Roles mentioning key skills
# ---------------------------
print("\nKey skill mentions:")
for skill in ["Python", "SQL", "Excel", "Power BI"]:
    count = df["technical_skills_detected"].fillna("").str.contains(skill, case=False).sum()
    print(f"{skill}: {count}")

# ---------------------------
# Salary summary and histogram
# ---------------------------
salary_data = df.loc[df["salary_valid"] == True, "salary_mid"].dropna()

if not salary_data.empty:
    print("\nSalary summary:")
    print(f"Rows with usable salary data: {salary_data.shape[0]}")
    print(f"Minimum estimated salary: {salary_data.min()}")
    print(f"Maximum estimated salary: {salary_data.max()}")
    print(f"Average estimated salary: {round(salary_data.mean(), 2)}")

    plt.figure(figsize=(10, 6))
    salary_data.plot(kind="hist", bins=15)
    plt.title("Salary Distribution")
    plt.xlabel("Estimated Salary")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("outputs/salary_histogram.png")
    plt.close()
else:
    print("\nNo usable salary data available for histogram.")