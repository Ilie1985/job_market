import pandas as pd
import sqlite3

df = pd.read_csv("data/cleaned_jobs.csv")

conn = sqlite3.connect("jobs.db")
df.to_sql("jobs", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

print("Data stored successfully in jobs.db")