"""
=============================================================
RETAIL SALES & CUSTOMER ANALYTICS PROJECT
Step 2: Exploratory Data Analysis (EDA)
=============================================================
Run AFTER 01_data_cleaning.py
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# ── CONFIG ──────────────────────────────────────────────────
DATA_PATH   = "../data/cleaned_data.csv"
OUTPUT_PATH = "../outputs/charts/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

PALETTE  = "Set2"
COLOR1   = "#2196F3"
COLOR2   = "#FF5722"
COLOR3   = "#4CAF50"

df = pd.read_csv(DATA_PATH, parse_dates=["Order Date", "Ship Date"])

print("=" * 60)
print("EDA — RETAIL SALES DATASET")
print(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# CHART 1: SALES BY CATEGORY
# ─────────────────────────────────────────────────────────────
cat_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Bar chart
axes[0].bar(cat_sales.index, cat_sales.values,
            color=[COLOR1, COLOR2, COLOR3], edgecolor="white", linewidth=1.5)
axes[0].set_title("Total Sales by Category", fontsize=14, fontweight="bold")
axes[0].set_ylabel("Total Sales ($)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for i, v in enumerate(cat_sales.values):
    axes[0].text(i, v + 2000, f"${v:,.0f}", ha="center", fontsize=10, fontweight="bold")

# Pie chart
axes[1].pie(cat_sales.values, labels=cat_sales.index,
            autopct="%1.1f%%", colors=[COLOR1, COLOR2, COLOR3],
            startangle=140, explode=[0.05, 0, 0],
            textprops={"fontsize": 11})
axes[1].set_title("Sales Distribution by Category", fontsize=14, fontweight="bold")

plt.suptitle("Category Performance Overview", fontsize=16, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "01_sales_by_category.png", bbox_inches="tight")
plt.show()
print("Saved: 01_sales_by_category.png")


# ─────────────────────────────────────────────────────────────
# CHART 2: MONTHLY SALES TREND
# ─────────────────────────────────────────────────────────────
monthly = (df.groupby(["Order Year", "Order Month"])["Sales"]
             .sum()
             .reset_index()
             .rename(columns={"Sales": "Monthly Sales"}))
monthly["Period"] = pd.to_datetime(
    monthly["Order Year"].astype(int).astype(str) + "-" + monthly["Order Month"].astype(int).astype(str).str.zfill(2)
)
monthly = monthly.sort_values("Period")

fig, ax = plt.subplots(figsize=(14, 6))
for yr, grp in monthly.groupby("Order Year"):
    ax.plot(grp["Period"], grp["Monthly Sales"], marker="o",
            label=str(yr), linewidth=2)
ax.set_title("Monthly Sales Trend by Year", fontsize=14, fontweight="bold")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(title="Year")
ax.grid(axis="y", alpha=0.4)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "02_monthly_trend.png")
plt.show()
print("Saved: 02_monthly_trend.png")


# ─────────────────────────────────────────────────────────────
# CHART 3: REGIONAL PERFORMANCE
# ─────────────────────────────────────────────────────────────
region_sales = df.groupby("Region")["Sales"].agg(["sum", "mean", "count"])
region_sales.columns = ["Total Sales", "Avg Order Value", "Order Count"]
region_sales = region_sales.sort_values("Total Sales", ascending=False)

print("\n📊  REGIONAL PERFORMANCE TABLE:")
print(region_sales.to_string())

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

# Total sales
colors = sns.color_palette(PALETTE, len(region_sales))
axes[0].barh(region_sales.index, region_sales["Total Sales"], color=colors)
axes[0].set_title("Total Sales by Region", fontweight="bold")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
for i, v in enumerate(region_sales["Total Sales"]):
    axes[0].text(v + 1000, i, f"${v:,.0f}", va="center", fontsize=9)

# Avg order value
axes[1].barh(region_sales.index, region_sales["Avg Order Value"], color=colors)
axes[1].set_title("Avg Order Value by Region", fontweight="bold")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Order count
axes[2].barh(region_sales.index, region_sales["Order Count"], color=colors)
axes[2].set_title("Order Count by Region", fontweight="bold")

plt.suptitle("Regional Performance Dashboard", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "03_regional_performance.png", bbox_inches="tight")
plt.show()
print("Saved: 03_regional_performance.png")


# ─────────────────────────────────────────────────────────────
# CHART 4: TOP 10 SUB-CATEGORIES
# ─────────────────────────────────────────────────────────────
sub_cat = (df.groupby("Sub-Category")["Sales"].sum()
             .sort_values(ascending=True).tail(10))

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(sub_cat.index, sub_cat.values,
               color=sns.color_palette("coolwarm", len(sub_cat)))
ax.set_title("Top 10 Sub-Categories by Sales", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Sales ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar in bars:
    w = bar.get_width()
    ax.text(w + 500, bar.get_y() + bar.get_height()/2,
            f"${w:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "04_top_subcategories.png")
plt.show()
print("Saved: 04_top_subcategories.png")


# ─────────────────────────────────────────────────────────────
# CHART 5: CUSTOMER SEGMENT ANALYSIS
# ─────────────────────────────────────────────────────────────
seg = df.groupby("Segment")["Sales"].agg(["sum", "mean", "count"]).reset_index()
seg.columns = ["Segment", "Total Sales", "Avg Sales", "Order Count"]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
seg_colors = ["#3498DB", "#E74C3C", "#2ECC71"]

axes[0].bar(seg["Segment"], seg["Total Sales"], color=seg_colors, edgecolor="white")
axes[0].set_title("Total Sales by Customer Segment", fontweight="bold")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for i, row in seg.iterrows():
    axes[0].text(i, row["Total Sales"] + 5000,
                 f"${row['Total Sales']:,.0f}", ha="center", fontsize=10)

axes[1].bar(seg["Segment"], seg["Avg Sales"], color=seg_colors, edgecolor="white")
axes[1].set_title("Average Order Value by Segment", fontweight="bold")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.suptitle("Customer Segment Performance", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "05_segment_analysis.png", bbox_inches="tight")
plt.show()
print("Saved: 05_segment_analysis.png")


# ─────────────────────────────────────────────────────────────
# CHART 6: SHIP MODE ANALYSIS
# ─────────────────────────────────────────────────────────────
ship = df.groupby("Ship Mode")["Sales"].agg(["sum", "count"]).reset_index()
ship.columns = ["Ship Mode", "Total Sales", "Orders"]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
ship_colors = sns.color_palette("husl", len(ship))

axes[0].pie(ship["Orders"], labels=ship["Ship Mode"],
            autopct="%1.1f%%", colors=ship_colors, startangle=90)
axes[0].set_title("Order Count by Ship Mode", fontweight="bold")

axes[1].bar(ship["Ship Mode"], ship["Total Sales"], color=ship_colors)
axes[1].set_title("Total Revenue by Ship Mode", fontweight="bold")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(rotation=15)

plt.suptitle("Shipping Mode Analysis", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "06_ship_mode.png", bbox_inches="tight")
plt.show()
print("Saved: 06_ship_mode.png")


# ─────────────────────────────────────────────────────────────
# CHART 7: TOP 15 CUSTOMERS
# ─────────────────────────────────────────────────────────────
top_customers = (df.groupby("Customer Name")["Sales"]
                   .sum()
                   .sort_values(ascending=False)
                   .head(15))

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_customers.index, top_customers.values,
               color=sns.color_palette("viridis", 15))
ax.set_title("Top 15 Customers by Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Sales ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.invert_yaxis()
for bar in bars:
    w = bar.get_width()
    ax.text(w + 200, bar.get_y() + bar.get_height()/2,
            f"${w:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "07_top_customers.png")
plt.show()
print("Saved: 07_top_customers.png")


# ─────────────────────────────────────────────────────────────
# CHART 8: QUARTERLY SALES HEATMAP
# ─────────────────────────────────────────────────────────────
pivot = df.pivot_table(values="Sales", index="Order Quarter",
                       columns="Order Year", aggfunc="sum")

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="YlOrRd",
            linewidths=0.5, ax=ax,
            annot_kws={"size": 10})
ax.set_title("Quarterly Sales Heatmap (by Year)", fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Quarter")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "08_quarterly_heatmap.png")
plt.show()
print("Saved: 08_quarterly_heatmap.png")


# ─────────────────────────────────────────────────────────────
# CHART 9: SALES DISTRIBUTION (HISTOGRAM)
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df["Sales"], bins=60, color=COLOR1, edgecolor="white", alpha=0.8)
axes[0].set_title("Sales Distribution", fontweight="bold")
axes[0].set_xlabel("Sales ($)")
axes[0].set_ylabel("Frequency")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Log scale for better view
axes[1].hist(np.log1p(df["Sales"]), bins=60, color=COLOR2, edgecolor="white", alpha=0.8)
axes[1].set_title("Sales Distribution (Log Scale)", fontweight="bold")
axes[1].set_xlabel("Log(Sales)")
axes[1].set_ylabel("Frequency")

plt.suptitle("Sales Value Distribution Analysis", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "09_sales_distribution.png", bbox_inches="tight")
plt.show()
print("Saved: 09_sales_distribution.png")


# ─────────────────────────────────────────────────────────────
# CHART 10: CATEGORY × SEGMENT HEATMAP
# ─────────────────────────────────────────────────────────────
cat_seg = df.pivot_table(values="Sales", index="Category",
                         columns="Segment", aggfunc="sum")

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(cat_seg, annot=True, fmt=",.0f", cmap="Blues",
            linewidths=0.5, ax=ax)
ax.set_title("Sales: Category × Segment Heatmap", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "10_category_segment_heatmap.png")
plt.show()
print("Saved: 10_category_segment_heatmap.png")


# ─────────────────────────────────────────────────────────────
# CHART 11: YEAR-OVER-YEAR GROWTH
# ─────────────────────────────────────────────────────────────
yoy = df.groupby("Order Year")["Sales"].sum().reset_index()
yoy["YoY Growth %"] = yoy["Sales"].pct_change() * 100

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.bar(yoy["Order Year"], yoy["Sales"], color=COLOR1, alpha=0.7, label="Total Sales")
ax2.plot(yoy["Order Year"], yoy["YoY Growth %"], color=COLOR2,
         marker="o", linewidth=2.5, label="YoY Growth %")
ax2.axhline(0, color="grey", linestyle="--", alpha=0.5)

ax1.set_title("Year-over-Year Sales Growth", fontsize=14, fontweight="bold")
ax1.set_ylabel("Total Sales ($)", color=COLOR1)
ax2.set_ylabel("YoY Growth (%)", color=COLOR2)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "11_yoy_growth.png")
plt.show()
print("Saved: 11_yoy_growth.png")


# ─────────────────────────────────────────────────────────────
# PRINT KPI SUMMARY
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("📊  KEY PERFORMANCE INDICATORS SUMMARY")
print("=" * 60)
print(f"  Total Revenue        : ${df['Sales'].sum():>15,.2f}")
print(f"  Total Orders         : {df['Order ID'].nunique():>15,}")
print(f"  Total Customers      : {df['Customer ID'].nunique():>15,}")
print(f"  Total Products       : {df['Product ID'].nunique():>15,}")
print(f"  Avg Order Value      : ${df.groupby('Order ID')['Sales'].sum().mean():>15,.2f}")
print(f"  Best Region          : {df.groupby('Region')['Sales'].sum().idxmax():>15}")
print(f"  Best Category        : {df.groupby('Category')['Sales'].sum().idxmax():>15}")
print(f"  Best Sub-Category    : {df.groupby('Sub-Category')['Sales'].sum().idxmax():>15}")
print(f"  Best Customer Segment: {df.groupby('Segment')['Sales'].sum().idxmax():>15}")
print("=" * 60)

print("\n✅  EDA COMPLETE — Run 03_customer_analytics.py next")
