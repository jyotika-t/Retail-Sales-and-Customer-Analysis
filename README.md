Retail Sales and Customer Analysis Project 

Build to demonstrate end-to-end data analyst skills:
- Data wrangling and cleaning
- Exploratory Data Analysis
- Customer segmentation (RFM)
- Business KPI tracking
- SQL reporting
- Dashboard design (Power BI)
- Business storytelling and recommendations


## 🗂️ Project Structure

```
retail_analytics_project/
│
├── data/
│   ├── train.csv               ← Raw dataset (Superstore Retail, 9,800 rows)
│   └── cleaned_data.csv        ← Auto-generated after running Step 1
│   └── rfm_segments.csv        ← Auto-generated after running Step 3
│
├── notebooks/
│   ├── 01_data_cleaning.py     ← Data cleaning & feature engineering
│   ├── 02_eda_analysis.py      ← EDA: 11 charts covering all KPIs
│   ├── 03_customer_analytics.py← RFM segmentation + CLV analysis
│   ├── 04_advanced_analytics.py← Pareto, Cohort, Forecasting, States
│   └── run_all.py              ←  Runs the full pipeline in one click
│
├── sql/
│   └── retail_analytics_queries.sql  ← 25 production-quality SQL queries
│
├── powerbi/
│   └── powerbi_setup_guide.md  ← Complete guide: DAX measures + 4-page dashboard
│
├── outputs/
│   └── reports/
│       └── kpi_summary.csv     ← Auto-generated KPI report
│
├── docs/
│   └── business_recommendations.md ← Insights & recommendations
│
├── requirements.txt            ← Python dependencies
└── README.md                   ← This file
```
## 📦 Dataset

| Field | Details |
|---|---|
| Source | Superstore Sales (Kaggle / provided train.csv) |
| Rows | 9,800 |
| Columns | 18 |
| Date Range | 2014 – 2017 |
| Key Fields | Order Date, Customer, Region, Category, Sub-Category, Sales |

## 🚀 Quick Start

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

```bash
cd notebooks
python run_all.py
```

---
