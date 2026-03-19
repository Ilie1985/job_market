# Job Market Intelligence Pipeline

## Project Overview
This project was built to answer a practical and career-relevant question:

**How can unstructured job listing data be transformed into a clean, structured dataset that can be analyzed for skill demand, location trends, remote work patterns, and salary availability?**

Instead of manually browsing job boards and trying to guess which tools and skills appear most often, I wanted to build a repeatable data pipeline that could automatically collect job listing data, clean it, store it, and analyze it.

The final outcome is a portfolio project that demonstrates an end-to-end workflow covering:

- data extraction
- data cleaning
- feature engineering
- structured storage
- exploratory analysis
- chart generation
- notebook-based reporting

This project was designed not only to show technical ability, but also to demonstrate analytical thinking and problem-solving.

---

## Data Source
The job listing data used in this project was collected from **Remote OK**, a public job board focused on remote opportunities.

Source used:
- **Remote OK** — https://remoteok.com/

The data collected from this source included fields such as:
- job title
- company
- location
- salary
- skills/tags
- date posted

Remote OK was chosen because it provides real-world job listing data that is suitable for a portfolio project and allows exploration of trends in remote job markets.

---

## The Problem I Wanted to Solve
Job listings contain useful information about the labour market, but the data is often difficult to work with in its raw form.

A typical job listing page may contain:
- inconsistent location labels
- missing salary fields
- mixed technical and descriptive keywords
- unstructured text
- repeated or incomplete values

Because of this, answering even simple questions becomes difficult:

- Which technical skills appear most frequently?
- Are jobs mainly remote, region-specific, or location-based?
- How often is salary information actually available?
- How visible are tools such as Python, SQL, Excel, and Power BI?

The core problem behind this project was:

> **How can messy job listing data be collected from the web, cleaned into a usable format, and turned into meaningful insights through a simple but complete data pipeline?**

---

## Why I Started This Project
I wanted to build a project for my data analysis / data engineering portfolio that felt realistic and useful.

I did not want a project that only showed a single chart or a single notebook. I wanted something that reflected the full lifecycle of data work:

1. collecting raw data  
2. dealing with messy and incomplete values  
3. transforming data into analysis-ready features  
4. storing the results in a structured format  
5. producing insights and visualizations  
6. documenting the process clearly  

This project gave me the opportunity to build something that sits between **data analysis** and **data engineering**:
- analysis, because I explore trends and answer questions from the data
- engineering, because I designed a pipeline with extraction, cleaning, storage, and reusable scripts

---

## My Thinking Process
When planning the project, I tried to balance four things:

- **realism** — using a real public job source
- **portfolio value** — building something relevant to data roles
- **technical difficulty** — challenging enough to show skill, but still manageable
- **clarity** — structured enough that someone reviewing the project can quickly understand it

### Why I chose job listing data
Job listings are a strong project topic because they are:
- real-world
- dynamic
- easy to explain in interviews
- full of useful business and market questions

They also connect well to my own goal of understanding technical skill demand.

### Why I chose this project design
I wanted the project to look like a real pipeline rather than a one-off script. That is why I separated the work into stages:

- scraping
- cleaning
- storing
- analyzing
- visualizing
- documenting

This made the project much stronger than simply collecting a CSV and plotting it.

### Why I chose Remote OK
I needed a source that was:
- public
- relevant to remote and technical roles
- manageable for a portfolio project
- rich enough to provide useful fields like title, company, location, salary, and tags

Remote OK was a suitable choice because it contains remote job listings with enough structured information to support data cleaning, analysis, and visualization.

---

## Solution Summary
The solution I built is a **Job Market Intelligence Pipeline**.

It works in the following stages:

### 1. Data extraction
A Python script retrieves job listing data from **Remote OK** and saves the raw output into a CSV file.

### 2. Data cleaning
A second script cleans the raw dataset by:
- removing duplicates
- filling missing values
- standardizing text fields
- cleaning location labels
- parsing salary information into numeric fields
- separating technical skills from descriptive tags

### 3. Data storage
The cleaned data is stored in both:
- a cleaned CSV file
- an SQLite database

### 4. Analysis
A notebook and Python analysis script are used to answer questions about:
- top technical skills
- top locations
- remote vs location-specific roles
- key mentions of Python, SQL, Excel, and Power BI
- salary availability and salary distribution

### 5. Visualization
Charts are generated and saved into the `outputs/` folder for use in the notebook and README.

---

## Technologies Used and Why I Chose Them

### Python
Python was used as the main language for the project because it supports the full pipeline in one ecosystem:
- web scraping
- cleaning
- storage
- analysis
- visualization

This allowed me to keep the project consistent and manageable.

### Requests
`requests` was used to retrieve source data from the web.

**Why I chose it:**  
It is simple, lightweight, and ideal for retrieving web content or structured responses.

### BeautifulSoup
`BeautifulSoup` was included as part of the scraping workflow for parsing HTML data.

**Why I chose it:**  
It is widely used, beginner-friendly, and suitable for extracting structured information from HTML pages.

### Selenium
`Selenium` was included as a fallback option for dynamic pages that may require browser rendering.

**Why I chose it:**  
I wanted the project design to reflect a more realistic scraping toolkit, not only static-page extraction.

### Pandas
`pandas` was used for:
- cleaning raw data
- transforming columns
- handling missing values
- building derived fields
- exploratory analysis

**Why I chose it:**  
It is one of the most important tools in Python for real-world data analysis and preprocessing.

### SQLite
SQLite was used to store the cleaned dataset in a relational database.

**Why I chose it:**  
It is lightweight, easy to set up, and appropriate for a portfolio-scale project. It allowed me to show structured storage without adding unnecessary deployment complexity.

### Matplotlib
`matplotlib` was used to generate charts.

**Why I chose it:**  
It is simple, reliable, and works well in both scripts and Jupyter Notebooks.

### Jupyter Notebook
The notebook was used to present the analysis in a readable format with both code and explanation.

**Why I chose it:**  
It is ideal for showing both technical work and thinking process in one place, which is important for portfolio presentation.

### Git and GitHub
Used for version control and project presentation.

**Why I chose them:**  
A good portfolio project should not only work locally; it should also be well-structured, reproducible, and easy to review.

---

## Project Workflow

### Phase 1: Scraping
The project begins by collecting job listing data from **Remote OK** and saving it into a raw CSV file.

Fields collected include:
- title
- company
- location
- salary
- skills/tags
- date posted

### Phase 2: Data Cleaning
The raw data is cleaned and standardized using pandas.

Cleaning includes:
- removing duplicate rows
- filling missing values
- normalizing text formatting
- standardizing location categories
- parsing salary minimum, maximum, and midpoint
- validating salary values
- separating technical skill detection from descriptive tags

### Phase 3: Storage
The cleaned data is saved into:
- `data/cleaned_jobs.csv`
- `jobs.db`

### Phase 4: Analysis
The data is analyzed to answer the following questions:
- Which technical skills appear most often?
- Which cleaned locations are most common?
- What is the distribution of remote, location-specific, and unknown roles?
- How often do Python, SQL, Excel, and Power BI appear?
- How much usable salary information is available?

### Phase 5: Visualization
Charts are created for:
- top technical skills
- top locations
- remote vs region-specific / unknown roles
- salary distribution

### Phase 6: Documentation and Portfolio Presentation
The final project includes:
- reusable scripts
- raw and cleaned data
- notebook-based explanation
- visual outputs
- a structured README

---

## Project Structure

```text
job_market/
│
├── dashboard/
│   └── dashboard_notes.md
├── data/
│   ├── raw_jobs.csv
│   └── cleaned_jobs.csv
├── notebooks/
│   └── analysis.ipynb
├── outputs/
│   ├── jobs_by_city.png
│   ├── remote_vs_nonremote.png
│   ├── salary_histogram.png
│   └── top_skills.png
├── scripts/
│   ├── analyze_data.py
│   ├── clean_data.py
│   ├── scraper.py
│   ├── selenium_scraper.py
│   └── store_data.py
├── jobs.db
├── README.md
└── requirements.txt

## Data Cleaning Improvements

One of the most important parts of this project was not just collecting data, but improving its quality.

The cleaned dataset includes new fields designed to make analysis more reliable:

- `location_clean`
- `work_type`
- `salary_min_num`
- `salary_max_num`
- `salary_mid`
- `salary_valid`
- `technical_skills_detected`
- `descriptive_tags_detected`

This improved the dataset, but also showed that real-world web data remains noisy and requires iterative refinement.

For example:
- many location values were missing or unclear
- salary information was only available for a subset of rows
- extracted tags mixed technical skills with descriptive terms

This reflects a realistic data challenge rather than a perfectly clean source.

---

## Results

### Top Technical Skills
This chart shows the most frequently detected technical skills.

### Top Locations
This chart shows the most common cleaned location values.

### Remote vs Region-Specific / Unknown
This chart compares remote, location-specific, and unknown work categories.

### Salary Distribution
This chart shows the distribution of valid estimated salary values.

---

## Key Findings

Some important findings from the analysis were:

- job listing data is highly useful but often noisy
- location information is often incomplete or inconsistent
- salary information is available for only a limited subset of listings
- remote work appears frequently, but a large number of roles also fall into unknown or location-specific categories
- detected skill frequencies depend strongly on how well skills are cleaned and classified

The project also highlighted an important lesson:

> building the pipeline is only part of the job — improving data quality is just as important.

---

## What Worked Well

This project successfully demonstrates:

- a structured scraping-to-analysis workflow
- raw and cleaned datasets
- reproducible preprocessing steps
- SQLite storage
- notebook-based exploratory analysis
- chart generation for reporting
- clear documentation of the purpose, process, and limitations

---

## Challenges and Limitations

Like most real-world data projects, this one has limitations:

- the data comes from a single source (**Remote OK**)
- salary data is sparse
- location data is not always standardized
- technical skill detection still depends on keyword matching
- some extracted tags are broad and noisy

These limitations are not failures — they are part of what made the project valuable. They show that working with web-based data involves iterative improvement rather than perfect first-pass results.