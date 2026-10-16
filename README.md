# Marketing Campaign Conversion Analytics — Future Interns Task 3

## Project Overview

This project analyzes the UCI Bank Marketing dataset to understand campaign subscription conversion and compare outcomes across contact methods, months, job categories, and campaign contact frequency. Python was used for data inspection, cleaning, and analysis. Power BI was used to build an interactive dashboard.

## Objective

- Measure the overall subscription conversion rate.
- Compare outcomes by contact method.
- Explore monthly and job-category differences.
- Understand how conversion varies with the number of campaign contacts.
- Present findings and practical recommendations in a Power BI dashboard.

## Dataset

- **Source:** UCI Machine Learning Repository — Bank Marketing
- **Official page:** https://archive.ics.uci.edu/dataset/222/bank+marketing
- **File used:** `bank-additional-full.csv`
- **Records analyzed:** 41,188
- **Outcome:** `y` indicates whether the contacted customer subscribed (`yes` or `no`).

This dataset measures bank marketing contacts and subscriptions. It does not contain a website visitor → lead → customer funnel, so the project focuses on campaign-contact conversion rather than website funnel stages.

## Tools

- Python
- pandas
- Power BI Desktop
- DAX measures for KPI cards

## Data Preparation and Analysis

Python was used to load the semicolon-separated CSV, inspect shape and data types, check missing values and exact duplicate rows, standardize column names and text fields, convert numeric fields, validate the subscription outcome, and create derived fields for conversion, age groups, and campaign contact-frequency groups. The analysis summaries were exported as CSV files for Power BI.

The category `unknown` was retained as a category rather than automatically treated as missing. Duplicate rows were inspected and were not blindly removed because the source does not provide a unique customer identifier for verifying them.

## Key Results

- **Contacts analyzed:** 41,188
- **Subscriptions:** 4,640
- **Did not subscribe:** 36,548
- **Overall subscription conversion rate:** 11.27%
- **Cellular contact conversion rate:** 14.74%
- **Telephone contact conversion rate:** 5.23%
- **Conversion after one campaign contact:** 13.04%
- **Conversion for six or more campaign contacts:** 5.49%

These are descriptive results from this dataset; they do not prove that a contact method or contact frequency causes a conversion outcome.

## Dashboard Contents

The Power BI report includes:

- KPI cards for total contacts, subscriptions, non-subscriptions, and conversion rate
- Conversion rate by contact method
- Conversion rate by campaign month
- Conversion rate by job category
- Conversion rate by campaign contact frequency

## Recommendations

1. Review cellular campaigns as a promising channel for follow-up, while considering campaign cost and audience differences if those data become available.
2. Review the value and timing of repeated contacts. Conversion rates were lower in the higher-contact groups in this dataset, so test contact limits and follow-up timing rather than assuming that more contacts always improve outcomes.
3. Interpret monthly rates together with the number of records in each month. Some months have far fewer records, so high rates from smaller groups should be treated cautiously.
4. Use these findings as descriptive guidance and validate any campaign changes with controlled testing and additional business context.

## Project Files

A typical project folder contains:

```text
Future Interns - Task 3/
├── data/
│   └── bank-additional-full.csv
├── Python Analysis/
│   ├── bank_marketing_analysis.py
│   └── outputs/
│       ├── cleaned_bank_marketing.csv
│       ├── contact_method_summary.csv
│       ├── monthly_summary.csv
│       ├── job_summary.csv
│       ├── contact_frequency_summary.csv
│       └── age_group_summary.csv
├── Future_Interns_Task_3_Marketing_Campaign_Analysis.pbix
└── README.md
```

## How to Reproduce

1. Install pandas: `python -m pip install pandas`
2. Place `bank-additional-full.csv` in the `data` folder.
3. Run: `python "Python Analysis/bank_marketing_analysis.py"`
4. Open the `.pbix` file in Power BI Desktop to view the dashboard.

## Note

This is an internship learning project based on the public UCI Bank Marketing dataset. Conclusions describe associations in the available data and should not be interpreted as causal claims.
