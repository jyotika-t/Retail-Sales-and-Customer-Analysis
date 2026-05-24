# 🛒 Retail Sales & Customer Analytics Project

> **Resume-ready Data Analyst portfolio project** — End-to-end analytics pipeline covering
> data cleaning, EDA, RFM segmentation, SQL queries, Python visualizations, and Power BI dashboard.

---

## 📊 Project Overview

Retail companies generate enormous volumes of sales data daily. This project simulates the work
of a real Data Analyst answering critical business questions:

- Which products drive maximum revenue?
- Which regions are underperforming?
- Who are the most valuable customers?
- What are the sales growth trends?
- Which categories need strategic investment?

---

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
│   └── run_all.py              ← ⭐ Runs the full pipeline in one click
│
├── sql/
│   └── retail_analytics_queries.sql  ← 25 production-quality SQL queries
│
├── powerbi/
│   └── powerbi_setup_guide.md  ← Complete guide: DAX measures + 4-page dashboard
│
├── outputs/
│   ├── charts/                 ← All 22 charts auto-saved here as PNG
│   └── reports/
│       └── kpi_summary.csv     ← Auto-generated KPI report
│
├── docs/
│   └── business_recommendations.md ← Insights & recommendations
│
├── requirements.txt            ← Python dependencies
└── README.md                   ← This file
```

---

## 📦 Dataset

| Field | Details |
|---|---|
| Source | Superstore Sales (Kaggle / provided train.csv) |
| Rows | 9,800 |
| Columns | 18 |
| Date Range | 2014 – 2017 |
| Key Fields | Order Date, Customer, Region, Category, Sub-Category, Sales |

---

## 🚀 Quick Start

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or in **Google Colab**:
```python
!pip install pandas numpy matplotlib seaborn openpyxl
```

### Step 2 — Run Full Pipeline

```bash
cd retail_analytics_project/notebooks
python run_all.py
```

This runs all 4 scripts in sequence and saves:
- ✅ `../data/cleaned_data.csv`
- ✅ `../data/rfm_segments.csv`
- ✅ 22 charts in `../outputs/charts/`
- ✅ `../outputs/reports/kpi_summary.csv`

### Step 3 — Run Individual Scripts

```bash
python 01_data_cleaning.py       # Clean & engineer features
python 02_eda_analysis.py        # EDA: 11 charts
python 03_customer_analytics.py  # RFM: 5 charts
python 04_advanced_analytics.py  # Advanced: 6 charts + forecast
```

---

## 📈 Charts Generated (22 Total)

| # | Chart | Script |
|---|---|---|
| 01 | Sales by Category (bar + pie) | EDA |
| 02 | Monthly Sales Trend by Year | EDA |
| 03 | Regional Performance (3-panel) | EDA |
| 04 | Top 10 Sub-Categories | EDA |
| 05 | Customer Segment Analysis | EDA |
| 06 | Ship Mode Analysis | EDA |
| 07 | Top 15 Customers | EDA |
| 08 | Quarterly Sales Heatmap | EDA |
| 09 | Sales Distribution (histogram) | EDA |
| 10 | Category × Segment Heatmap | EDA |
| 11 | Year-over-Year Growth | EDA |
| 12 | RFM Segment Distribution | Customer |
| 13 | RFM Scatter (Recency vs Monetary) | Customer |
| 14 | CLV by Segment | Customer |
| 15 | RFM Score Heatmap | Customer |
| 16 | Customer Behavior Distribution | Customer |
| 17 | Pareto Analysis (80/20) | Advanced |
| 18 | Customer Cohort Retention Heatmap | Advanced |
| 19 | Sales Forecast + Confidence Band | Advanced |
| 20 | Top 15 States by Revenue | Advanced |
| 21 | Revenue Band Distribution | Advanced |
| 22 | Weekday Sales Pattern | Advanced |

---

## 🗄️ SQL Queries (25 Total)

Organized in 7 sections in `sql/retail_analytics_queries.sql`:

| Section | Queries |
|---|---|
| A — Sales KPIs | Overall KPIs, Annual Summary, MoM, QoQ, YoY Growth |
| B — Product Analysis | Category, Sub-category, Top 20 Products, Pareto |
| C — Regional Analysis | Region, State, City breakdowns |
| D — Customer Analytics | Segment, Top customers, RFM in SQL, New vs Returning |
| E — Shipping Analysis | Ship mode performance, Avg ship time by region |
| F — Business Intelligence | High-value orders, Low-value repeat orders |
| G — Power BI Views | 4 pre-built SQL views for Power BI connection |

---

## 📊 Power BI Dashboard (4 Pages)

See `powerbi/powerbi_setup_guide.md` for full setup instructions.

| Page | Content |
|---|---|
| 1. Executive Summary | KPI cards, monthly trend, category donut, regional bar |
| 2. Sales Deep Dive | Category trend, sub-category, YoY, matrix heatmap |
| 3. Customer Analytics | Segment, RFM, top customers, retention KPIs |
| 4. Regional Performance | Filled map, city ranking, category × region matrix |

**DAX Measures included:** 25+ measures covering revenue, growth, YTD, MTD, customer KPIs.

---

## 🔍 Key Business Insights

1. **Technology** is the top revenue category (36%+ of total), driven by Phones and Copiers.
2. **West region** leads revenue; **South region** has the fewest orders — opportunity area.
3. **Consumer segment** drives volume; **Home Office** has the highest avg order value.
4. **~20% of products drive ~80% of revenue** (Pareto rule confirmed).
5. **Q4 (Oct–Dec)** consistently peaks — holiday season drives sales spikes.
6. **Standard Class** shipping carries 60%+ of orders — cost vs speed trade-off present.
7. **Champions & Loyal Customers** (RFM) should receive retention-focused campaigns.
8. **At Risk / Cant Lose Them** customers have high monetary value but long recency — winback needed.

---

## 💡 Business Recommendations

See `docs/business_recommendations.md` for the full strategy document.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.8+ | Data cleaning, analysis, visualization |
| Pandas | Data manipulation |
| NumPy | Numerical computing |
| Matplotlib + Seaborn | Data visualization (22 charts) |
| MySQL / DB Fiddle | SQL analytics (25 queries) |
| Power BI Desktop | Interactive dashboard (4 pages, 25 DAX measures) |
| GitHub | Version control and portfolio hosting |

---

## 👤 About This Project

Built as a **portfolio project** to demonstrate end-to-end data analyst skills:
- Data wrangling and cleaning
- Exploratory Data Analysis
- Customer segmentation (RFM)
- Business KPI tracking
- SQL reporting
- Dashboard design (Power BI)
- Business storytelling and recommendations

---

## 📁 GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit: Retail Sales Analytics Portfolio Project"
git remote add origin https://github.com/yourusername/retail-sales-analytics
git push -u origin main
```

Recommended GitHub topics to add: `data-analytics`, `python`, `sql`, `power-bi`, `eda`, `rfm-analysis`, `retail`, `portfolio`
