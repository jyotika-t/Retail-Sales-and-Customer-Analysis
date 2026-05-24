"""
=============================================================
RETAIL SALES & CUSTOMER ANALYTICS PROJECT
Step 4: Advanced Analytics — Pareto, Cohort, Forecasting
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

DATA_PATH   = "../data/cleaned_data.csv"
OUTPUT_PATH = "../outputs/charts/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["Order Date", "Ship Date"])

print("=" * 60)
print("ADVANCED ANALYTICS")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# CHART 17: PARETO ANALYSIS — 80/20 RULE (Products)
# ─────────────────────────────────────────────────────────────
prod_sales = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
cumulative_pct = prod_sales.cumsum() / prod_sales.sum() * 100
pareto_df = pd.DataFrame({"Sales": prod_sales, "Cum_Pct": cumulative_pct}).reset_index()
pareto_df["Product_Rank"] = range(1, len(pareto_df) + 1)

# Find 80% threshold index
thresh_idx = (pareto_df["Cum_Pct"] <= 80).sum()
pct_products_for_80pct = thresh_idx / len(pareto_df) * 100

print(f"\n📊  PARETO: {pct_products_for_80pct:.1f}% of products drive 80% of revenue")
print(f"    That's {thresh_idx} products out of {len(pareto_df)} total.")

fig, ax1 = plt.subplots(figsize=(14, 6))
ax2 = ax1.twinx()

ax1.bar(pareto_df["Product_Rank"], pareto_df["Sales"],
        color="#3498DB", alpha=0.7, width=1.0, label="Product Sales")
ax2.plot(pareto_df["Product_Rank"], pareto_df["Cum_Pct"],
         color="#E74C3C", linewidth=2, label="Cumulative %")
ax2.axhline(80, color="green", linestyle="--", linewidth=1.5, label="80% Line")
ax2.axvline(thresh_idx, color="orange", linestyle="--", linewidth=1.5,
            label=f"Top {thresh_idx} products")

ax1.set_xlabel("Product Rank")
ax1.set_ylabel("Sales ($)", color="#3498DB")
ax2.set_ylabel("Cumulative Revenue %", color="#E74C3C")
ax2.set_ylim(0, 105)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right")

ax1.set_title("Pareto Analysis — Product Revenue (80/20 Rule)",
              fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "17_pareto_analysis.png")
plt.show()
print("Saved: 17_pareto_analysis.png")


# ─────────────────────────────────────────────────────────────
# CHART 18: CUSTOMER COHORT ANALYSIS (First-Order Month)
# ─────────────────────────────────────────────────────────────
# Assign each customer their first order month
customer_first_order = df.groupby("Customer ID")["Order Date"].min().reset_index()
customer_first_order.columns = ["Customer ID", "First Order Date"]
customer_first_order["Cohort Month"] = customer_first_order["First Order Date"].dt.to_period("M")

df2 = df.merge(customer_first_order[["Customer ID", "Cohort Month"]], on="Customer ID")
df2["Order Month Period"] = df2["Order Date"].dt.to_period("M")
df2["Cohort Index"] = (df2["Order Month Period"] - df2["Cohort Month"]).apply(lambda x: x.n if pd.notna(x) else np.nan)
df2 = df2.dropna(subset=["Cohort Index"])
df2["Cohort Index"] = df2["Cohort Index"].astype(int)

cohort_data = df2.groupby(["Cohort Month", "Cohort Index"])["Customer ID"].nunique().reset_index()
cohort_pivot = cohort_data.pivot_table(index="Cohort Month", columns="Cohort Index",
                                        values="Customer ID")

# Retention rate
cohort_size = cohort_pivot.iloc[:, 0]
retention = cohort_pivot.divide(cohort_size, axis=0) * 100

# Show only first 12 months for clarity
retention_12 = retention.iloc[:, :12]

fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(retention_12.astype(float), annot=True, fmt=".0f",
            cmap="YlGn", linewidths=0.4, ax=ax,
            annot_kws={"size": 8})
ax.set_title("Customer Cohort Retention Rate (%) — First 12 Months",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Months Since First Purchase")
ax.set_ylabel("Cohort (First Purchase Month)")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "18_cohort_analysis.png")
plt.show()
print("Saved: 18_cohort_analysis.png")


# ─────────────────────────────────────────────────────────────
# CHART 19: SIMPLE SALES FORECAST (Moving Average)
# ─────────────────────────────────────────────────────────────
monthly_sales = (df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
                   .sum()
                   .reset_index())
monthly_sales.columns = ["Period", "Sales"]
monthly_sales["Period"] = monthly_sales["Period"].dt.to_timestamp()
monthly_sales = monthly_sales.sort_values("Period")

# 3-month rolling average
monthly_sales["MA_3"]  = monthly_sales["Sales"].rolling(3).mean()
monthly_sales["MA_6"]  = monthly_sales["Sales"].rolling(6).mean()

# Naive forecast: extend last 6-month average for 6 months
last_date = monthly_sales["Period"].max()
forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=6, freq="MS")
last_avg = monthly_sales["Sales"].tail(6).mean()
forecast_df = pd.DataFrame({"Period": forecast_dates, "Forecast": last_avg})

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(monthly_sales["Period"], monthly_sales["Sales"],
        label="Actual Sales", color="#3498DB", linewidth=2, marker="o", markersize=4)
ax.plot(monthly_sales["Period"], monthly_sales["MA_3"],
        label="3-Month MA", color="#E67E22", linewidth=2, linestyle="--")
ax.plot(monthly_sales["Period"], monthly_sales["MA_6"],
        label="6-Month MA", color="#9B59B6", linewidth=2, linestyle="--")
ax.plot(forecast_df["Period"], forecast_df["Forecast"],
        label="6-Month Forecast", color="#E74C3C", linewidth=2.5,
        linestyle=":", marker="s", markersize=6)
ax.axvline(last_date, color="grey", linestyle="--", alpha=0.5, label="Forecast Start")

ax.fill_between(forecast_df["Period"],
                forecast_df["Forecast"] * 0.85,
                forecast_df["Forecast"] * 1.15,
                alpha=0.15, color="#E74C3C", label="±15% Confidence Band")

ax.set_title("Monthly Sales Trend + 6-Month Forecast",
             fontsize=14, fontweight="bold")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "19_sales_forecast.png")
plt.show()
print("Saved: 19_sales_forecast.png")


# ─────────────────────────────────────────────────────────────
# CHART 20: TOP STATES BY REVENUE
# ─────────────────────────────────────────────────────────────
state_sales = df.groupby("State")["Sales"].sum().sort_values(ascending=False).head(15)

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(state_sales.index, state_sales.values,
               color=sns.color_palette("coolwarm", len(state_sales)))
ax.set_title("Top 15 States by Total Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Sales ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.invert_yaxis()
for bar in bars:
    w = bar.get_width()
    ax.text(w + 500, bar.get_y() + bar.get_height()/2,
            f"${w:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "20_top_states.png")
plt.show()
print("Saved: 20_top_states.png")


# ─────────────────────────────────────────────────────────────
# CHART 21: REVENUE BAND DISTRIBUTION
# ─────────────────────────────────────────────────────────────
band_counts = df["Revenue Band"].value_counts()

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(band_counts.index, band_counts.values,
              color=sns.color_palette("RdYlGn", len(band_counts)))
ax.set_title("Order Volume by Revenue Band", fontsize=14, fontweight="bold")
ax.set_ylabel("Number of Orders")
ax.set_xlabel("Revenue Band")
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
            str(int(bar.get_height())), ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "21_revenue_bands.png")
plt.show()
print("Saved: 21_revenue_bands.png")


# ─────────────────────────────────────────────────────────────
# CHART 22: WEEKDAY SALES PATTERN
# ─────────────────────────────────────────────────────────────
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_sales = (df.groupby("Order Day")["Sales"]
                   .agg(["sum", "count"])
                   .reindex(day_order)
                   .reset_index())
weekday_sales.columns = ["Day", "Total Sales", "Order Count"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].bar(weekday_sales["Day"], weekday_sales["Total Sales"],
            color=sns.color_palette("husl", 7))
axes[0].set_title("Sales by Day of Week", fontweight="bold")
axes[0].set_ylabel("Total Sales ($)")
axes[0].tick_params(axis="x", rotation=30)
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

axes[1].bar(weekday_sales["Day"], weekday_sales["Order Count"],
            color=sns.color_palette("husl", 7))
axes[1].set_title("Order Count by Day of Week", fontweight="bold")
axes[1].set_ylabel("Number of Orders")
axes[1].tick_params(axis="x", rotation=30)

plt.suptitle("Day-of-Week Sales Patterns", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "22_weekday_pattern.png", bbox_inches="tight")
plt.show()
print("Saved: 22_weekday_pattern.png")


# ─────────────────────────────────────────────────────────────
# EXPORT BUSINESS INSIGHTS TABLE
# ─────────────────────────────────────────────────────────────
insights = {
    "Metric": [
        "Total Revenue", "Total Orders", "Unique Customers",
        "Best Region", "Best Category", "Best Sub-Category",
        "Best Customer Segment", "Avg Order Value",
        "% Products = 80% Revenue", "Top State"
    ],
    "Value": [
        f"${df['Sales'].sum():,.2f}",
        f"{df['Order ID'].nunique():,}",
        f"{df['Customer ID'].nunique():,}",
        df.groupby("Region")["Sales"].sum().idxmax(),
        df.groupby("Category")["Sales"].sum().idxmax(),
        df.groupby("Sub-Category")["Sales"].sum().idxmax(),
        df.groupby("Segment")["Sales"].sum().idxmax(),
        f"${df.groupby('Order ID')['Sales'].sum().mean():,.2f}",
        f"{pct_products_for_80pct:.1f}%",
        df.groupby("State")["Sales"].sum().idxmax()
    ]
}
insights_df = pd.DataFrame(insights)
insights_df.to_csv("../outputs/reports/kpi_summary.csv", index=False)
print("\n✅  KPI Summary saved → ../outputs/reports/kpi_summary.csv")
print("\n✅  ADVANCED ANALYTICS COMPLETE — Check ../outputs/charts/ for all charts")
print("=" * 60)
print(insights_df.to_string(index=False))
