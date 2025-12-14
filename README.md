# Air Quality Data Analysis (India)

## Overview
This project presents an exploratory data analysis (EDA) of air quality measurements across multiple Indian cities. The goal is to understand pollution patterns, variability across locations, and relationships between particulate matter (PM2.5) and the Air Quality Index (AQI).

## Dataset
- Source: Kaggle – Air Quality Data in India
- Records: ~29,000 daily observations
- Features include PM2.5, PM10, gaseous pollutants, AQI, city, and date.

## Project Structure
Project_AirQuality/
│
├── data/
│   ├── dataset_original.csv
│   └── processed/
│       └── air_quality_clean_base.csv
│
├── src/
│   ├── data_loading.py
│   ├── cleaning.py
│   └── eda.py
│
├── notebooks/
│   └── eda_visuals.ipynb
│
└── README.md

## Analysis Steps
1. Data loading and validation
2. Basic cleaning and missing-value assessment
3. Exploratory data analysis:
   - AQI trends over time
   - Distribution of PM2.5
   - City-level comparisons
   - Relationship between PM2.5 and AQI

## Key Findings
- Air pollution levels vary significantly across cities and over time.
- PM2.5 displays a highly skewed distribution with extreme pollution events.
- Strong positive association observed between PM2.5 concentration and AQI.

## Tools & Technologies
- Python (pandas, matplotlib, seaborn)
- Jupyter Notebooks
- Linux environment
- Git/GitHub

## Notes
This project focuses on exploratory analysis. The cleaned dataset and insights can serve as a foundation for future predictive or modeling work.

