"""
=============================================================
RETAIL SALES & CUSTOMER ANALYTICS PROJECT
Step 1: Data Cleaning & Preprocessing
=============================================================
Author   : Data Analyst Portfolio Project
Dataset  : Superstore Retail Sales (train.csv)
Tool     : Python (run in Google Colab or locally)
=============================================================
"""

# ── 1. INSTALL & IMPORT LIBRARIES ──────────────────────────
# Uncomment the line below if running in Google Colab:
# !pip install pandas numpy matplotlib seaborn openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")
plt.rcParams["figure.dpi"] = 150
plt.rcParams["figure.figsize"] = (12, 6)

# ── 2. LOAD DATA ────────────────────────────────────────────
# If running locally, make sure train.csv is in ../data/
# If on Colab, upload the file and change path to: '/content/train.csv'

DATA_PATH = "../data/train.csv"          # Change if needed
OUTPUT_PATH = "../outputs/charts/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("RETAIL SALES DATASET — FIRST LOOK")
print("=" * 60)
print(f"\nShape        : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumn Names :\n{df.columns.tolist()}")
print(f"\nData Types   :\n{df.dtypes}")
print(f"\nFirst 5 Rows :\n{df.head()}")


# ── 3. BASIC DATA QUALITY CHECK ─────────────────────────────
print("\n" + "=" * 60)
print("DATA QUALITY CHECK")
print("=" * 60)
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nDuplicate Rows: {df.duplicated().sum()}")
print(f"\nSales Statistics:\n{df['Sales'].describe()}")


# ── 4. DATA CLEANING ────────────────────────────────────────
print("\n" + "=" * 60)
print("CLEANING STEPS")
print("=" * 60)

# 4a. Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=False, errors="coerce")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=False, errors="coerce")
print("✅  Dates converted to datetime.")

# 4b. Extract date parts
df["Order Year"]    = df["Order Date"].dt.year
df["Order Month"]   = df["Order Date"].dt.month
df["Order Month Name"] = df["Order Date"].dt.strftime("%b")
df["Order Quarter"] = df["Order Date"].dt.quarter
df["Order Day"]     = df["Order Date"].dt.day_name()

# 4c. Shipping duration (days)
df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
print("✅  New date features created (Year, Month, Quarter, Ship Days).")

# 4d. Fill missing postal codes
df["Postal Code"] = df["Postal Code"].fillna(0).astype(int)
print("✅  Missing Postal Codes filled with 0.")

# 4e. Remove any fully duplicate rows
before = len(df)
df.drop_duplicates(inplace=True)
print(f"✅  Duplicate rows removed: {before - len(df)}")

# 4f. Strip whitespace from string columns
str_cols = df.select_dtypes(include="object").columns
df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())
print("✅  Whitespace stripped from all string columns.")

# 4g. Sales sanity check — remove negative/zero sales
neg_sales = df[df["Sales"] <= 0].shape[0]
df = df[df["Sales"] > 0].reset_index(drop=True)
print(f"✅  Removed {neg_sales} rows with zero/negative Sales.")

# ── 5. FEATURE ENGINEERING ──────────────────────────────────
print("\n" + "=" * 60)
print("FEATURE ENGINEERING")
print("=" * 60)

# Revenue bands
df["Revenue Band"] = pd.cut(
    df["Sales"],
    bins=[0, 50, 200, 500, 1000, df["Sales"].max() + 1],
    labels=["Low (<50)", "Medium (50-200)", "High (200-500)",
            "Very High (500-1K)", "Premium (>1K)"]
)

# Shipping speed label
df["Shipping Speed"] = pd.cut(
    df["Ship Days"],
    bins=[-1, 1, 3, 6, 100],
    labels=["Same/Next Day", "Express (2-3d)", "Standard (4-6d)", "Slow (7d+)"]
)

print("✅  Revenue Band and Shipping Speed columns added.")
print(f"\nFinal Cleaned Dataset Shape: {df.shape}")

# ── 6. SAVE CLEANED DATA ────────────────────────────────────
CLEAN_PATH = "../data/cleaned_data.csv"
df.to_csv(CLEAN_PATH, index=False)
print(f"\n✅  Cleaned data saved → {CLEAN_PATH}")


# ── 7. MISSING VALUE HEATMAP ────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 4))
sns.heatmap(df.isnull(), yticklabels=False, cbar=False,
            cmap="viridis", ax=ax)
ax.set_title("Missing Values Heatmap (After Cleaning)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "00_missing_heatmap.png")
plt.show()
print("Chart saved: 00_missing_heatmap.png")

print("\n✅  DATA CLEANING COMPLETE — Run 02_eda_analysis.py next")
