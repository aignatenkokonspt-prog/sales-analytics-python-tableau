# Sales Overview / ABC Analysis

An end-to-end data analytics project featuring a Python ETL pipeline for data preprocessing and an interactive Tableau dashboard for multi-angle sales performance analysis.

Live Dashboard Link: **[Live Interactive Dashboard on Tableau Public](https://public.tableau.com/app/profile/ann.ign/viz/Parameters_17899346849220/Sales?publish=yes)**


## Tech Stack

* **Python:** `pandas`
* **BI Platform:** `Tableau Desktop` / `Tableau Public`
* **Methods:** `ABC Analys` / `Pareto Analys`, `Dynamic Parameter Controls`

## Dashboard Preview

![Dashboard Preview](dashboard_preview.png)


---

## Technical Overview & Workflow

### 1. Python Data Pipeline (pandas)
**Python script:** [data_cleaning.py](data_cleaning.py)

Automated ETL script  processing raw sales logs into a cleaned, analytics-ready dataset:
* **Initial Audit:** Assessed missing data ratios (df.isnull().mean()) and schema structure.
* **Date Parsing & Formatting:** Parsed mixed raw date strings into standard YYYY-MM-DD objects (pd.to_datetime).
* **String Cleaning & Currency Standardizing:** Stripped currency text prefixes (Price:, $, GBP), handled whitespaces, and converted raw text prices into clean floats (pd.to_numeric).
* **Missing Value Imputation:** Assigned Unknown attributes to unassigned categorical fields (Department, Manager) to fill attribution gaps.
* **Feature Engineering:** Calculated gross revenue (Price * Quantity) and extracted customer loyalty tags (CARD vs GUEST) from Customer_ID.
* **Automated Excel Reporting:** Generated multi-sheet Excel reports with automated revenue share calculations (Share (%)) grouped by Manager, Department, City, and Customer Type.


### 2. Dashboard Capabilities & Diagnostic Value
The Tableau dashboard serves as a dynamic diagnostic tool, allowing users to analyze performance across **Department**, **City Store**, and **Manager** levels via integrated parameters:

* **ABC Concentration Analysis:** Instantly identifies core revenue drivers (~80% of sales, Group A) vs low-revenue segments (~5% of sales, Group C) to prioritize focus areas.
* **Attribution Audit (Unknown Tracking):** Tracks unattributed transactions (Unknown categories/managers) to isolate gaps in data entry.
* **Loyalty Program Oversight:** Monitors card issuance (CARD vs GUEST) per sales manager to highlight managers with low loyalty prompt rates during checkout.
* **Manager Benchmarking:** Identifies top-performing managers to establish sales standards, structure onboarding programs, or pair weaker performers for peer training.
* **Trend & Seasonality Monitoring:** Displays daily revenue sparklines per segment to track short-term spikes, dips, or recurring sales patterns.

---





