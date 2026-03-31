# Healthcare Patient Survey Analytics

## Overview
Analysis of hospital patient survey data to evaluate performance, response rates, and patient satisfaction across healthcare facilities.

The project focuses on transforming raw survey data into structured insights and a Power BI dashboard for reporting.

## Objective
- Analyze survey response behavior across hospitals
- Identify top-performing facilities and regions
- Evaluate response rates and patient satisfaction
- Generate structured datasets for BI reporting

## Dataset
- Source: Patient survey dataset (hospital-level)
- Grain: Hospital × Measure

Key fields:
- Provider ID, Hospital Name, City, State, County
- Survey Response Rate %
- Number of Completed Surveys
- Patient Survey Star Rating
- Measure ID

## Process

### Data Preparation
- Converted mixed-type numeric fields to numeric
- Standardized date columns
- Removed duplicates at hospital level

### Data Modeling
- Created hospital-level summary dataset
- Ensured correct grain (Provider ID level)

### Analysis
- Survey volume by hospital
- Response rate by measure
- Top counties by response rate
- Top hospitals by rating
- Same-city hospital clustering
- Response rate vs satisfaction correlation


## Key Metrics

- **Survey Volume**
  Number of completed surveys per hospital

- **Survey Response Rate**
  Average response rate by measure and hospital

- **Top Performing Hospitals**
  Based on survey response rate

- **Geographic Performance**
  County-level and city-level comparisons

- **Weighted Response Rate**
  Accounts for survey volume per hospital

## Dashboard (Power BI)

- Surveys completed by hospital
- Response rate by measure
- Top hospitals and counties
- Drill-down: County → City → Hospital
- Additional insights dataset for reporting

## Key Insight

- Weak positive relationship between response rate and star rating  
- High variability across hospitals and regions  
- Survey volume impacts weighted performance metrics  

## Tech Stack
- Python (Pandas, NumPy)
- Data Cleaning & Aggregation
- Power BI


