"""
=============================================================
RETAIL SALES & CUSTOMER ANALYTICS PROJECT
Step 3: Customer Analytics — RFM Segmentation & CLV
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

# ─────────────────────────────────────────────────────────────
# RFM ANALYSIS
# Recency  = Days since last order
# Frequency = Total number of orders
# Monetary  = Total money spent
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("RFM CUSTOMER SEGMENTATION")
print("=" * 60)

# Snapshot date = day after the latest order in the dataset
snapshot_date = df["Order Date"].max() + pd.Timedelta(days=1)
print(f"Snapshot Date: {snapshot_date.date()}")

rfm = df.groupby("Customer ID").agg(
    CustomerName=("Customer Name", "first"),
    Segment=("Segment", "first"),
    Region=("Region", "first"),
    Recency=("Order Date", lambda x: (snapshot_date - x.max()).days),
    Frequency=("Order ID", "nunique"),
    Monetary=("Sales", "sum")
).reset_index()

# Score each dimension 1–5 (5 = best)
rfm["R_Score"] = pd.qcut(rfm["Recency"],  q=5, labels=[5, 4, 3, 2, 1])
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5])
rfm["M_Score"] = pd.qcut(rfm["Monetary"],  q=5, labels=[1, 2, 3, 4, 5])

rfm["R_Score"] = rfm["R_Score"].cat.codes.replace(-1, 0) + 1
rfm["F_Score"] = rfm["F_Score"].cat.codes.replace(-1, 0) + 1
rfm["M_Score"] = rfm["M_Score"].cat.codes.replace(-1, 0) + 1

rfm["RFM_Score"]     = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
rfm["RFM_Score_Str"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

# ── CUSTOMER SEGMENTS ──────────────────────────────────────
def rfm_segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    total = r + f + m
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3 and m >= 3:
        return "Loyal Customers"
    elif r >= 4 and f <= 2:
        return "New Customers"
    elif r >= 3 and m >= 3 and f <= 2:
        return "Potential Loyalists"
    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2 and m <= 2:
        return "Lost / Churned"
    elif r <= 2 and m >= 3:
        return "Cant Lose Them"
    elif r >= 3 and total >= 10:
        return "About to Sleep"
    else:
        return "Needs Attention"

rfm["Customer_Segment"] = rfm.apply(rfm_segment, axis=1)

print(f"\nTotal Customers Segmented: {len(rfm)}")
print(f"\nCustomer Segment Distribution:")
print(rfm["Customer_Segment"].value_counts().to_string())

# ── CLV (Customer Lifetime Value) ─────────────────────────
rfm["CLV"] = rfm["Frequency"] * rfm["Monetary"]

# ── SAVE RFM DATA ─────────────────────────────────────────
rfm.to_csv("../data/rfm_segments.csv", index=False)
print("\n✅  RFM data saved → ../data/rfm_segments.csv")


# ─────────────────────────────────────────────────────────────
# CHART 12: RFM SEGMENT DISTRIBUTION
# ─────────────────────────────────────────────────────────────
seg_counts = rfm["Customer_Segment"].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

colors = sns.color_palette("tab10", len(seg_counts))

# Bar chart
axes[0].bar(seg_counts.index, seg_counts.values, color=colors, edgecolor="white")
axes[0].set_title("Customer Segment Distribution (Count)", fontweight="bold")
axes[0].set_ylabel("Number of Customers")
axes[0].tick_params(axis="x", rotation=35)
for i, v in enumerate(seg_counts.values):
    axes[0].text(i, v + 0.5, str(v), ha="center", fontsize=9)

# Pie chart
axes[1].pie(seg_counts.values, labels=seg_counts.index,
            autopct="%1.1f%%", colors=colors, startangle=140,
            pctdistance=0.8, textprops={"fontsize": 9})
axes[1].set_title("Customer Segment Share", fontweight="bold")

plt.suptitle("RFM Customer Segmentation", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "12_rfm_segments.png", bbox_inches="tight")
plt.show()
print("Saved: 12_rfm_segments.png")


# ─────────────────────────────────────────────────────────────
# CHART 13: RFM SCATTER — RECENCY vs MONETARY
# ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
segment_palette = {s: c for s, c in zip(rfm["Customer_Segment"].unique(),
                                          sns.color_palette("tab10", rfm["Customer_Segment"].nunique()))}

for seg, grp in rfm.groupby("Customer_Segment"):
    ax.scatter(grp["Recency"], grp["Monetary"],
               label=seg, alpha=0.6, s=60,
               color=segment_palette[seg])

ax.set_title("Recency vs Monetary Value by Customer Segment", fontsize=14, fontweight="bold")
ax.set_xlabel("Recency (Days since last order)")
ax.set_ylabel("Monetary Value ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "13_rfm_scatter.png", bbox_inches="tight")
plt.show()
print("Saved: 13_rfm_scatter.png")


# ─────────────────────────────────────────────────────────────
# CHART 14: CLV BY SEGMENT
# ─────────────────────────────────────────────────────────────
clv_seg = rfm.groupby("Customer_Segment")["CLV"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(clv_seg.index, clv_seg.values,
               color=sns.color_palette("viridis", len(clv_seg)))
ax.set_title("Customer Lifetime Value (CLV) by Segment", fontsize=14, fontweight="bold")
ax.set_xlabel("Total CLV ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar in bars:
    w = bar.get_width()
    ax.text(w + 200, bar.get_y() + bar.get_height()/2,
            f"${w:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "14_clv_by_segment.png")
plt.show()
print("Saved: 14_clv_by_segment.png")


# ─────────────────────────────────────────────────────────────
# CHART 15: RFM SCORE HEATMAP
# ─────────────────────────────────────────────────────────────
rfm_heat = rfm.groupby(["R_Score", "F_Score"])["Monetary"].mean().unstack()

fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(rfm_heat, annot=True, fmt=",.0f", cmap="RdYlGn",
            linewidths=0.5, ax=ax)
ax.set_title("Average Monetary Value — RFM Heatmap\n(Recency Score vs Frequency Score)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Frequency Score")
ax.set_ylabel("Recency Score (5=Most Recent)")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "15_rfm_heatmap.png")
plt.show()
print("Saved: 15_rfm_heatmap.png")


# ─────────────────────────────────────────────────────────────
# CHART 16: ORDERS PER CUSTOMER (FREQUENCY DISTRIBUTION)
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(rfm["Frequency"], bins=20, color="#3498DB", edgecolor="white")
axes[0].set_title("Order Frequency Distribution", fontweight="bold")
axes[0].set_xlabel("Number of Orders per Customer")
axes[0].set_ylabel("Number of Customers")

axes[1].hist(rfm["Monetary"], bins=30, color="#E74C3C", edgecolor="white")
axes[1].set_title("Customer Spend Distribution", fontweight="bold")
axes[1].set_xlabel("Total Spend ($)")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.suptitle("Customer Purchase Behavior", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "16_customer_behavior.png", bbox_inches="tight")
plt.show()
print("Saved: 16_customer_behavior.png")


# ─────────────────────────────────────────────────────────────
# PRINT TOP AND BOTTOM CUSTOMERS
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("🏆  TOP 10 CUSTOMERS (by Monetary Value)")
print("=" * 60)
top10 = rfm.nlargest(10, "Monetary")[["CustomerName", "Recency", "Frequency", "Monetary", "Customer_Segment"]]
print(top10.to_string(index=False))

print("\n" + "=" * 60)
print("⚠️   BOTTOM 10 AT-RISK CUSTOMERS (High Monetary, High Recency)")
print("=" * 60)
at_risk = rfm[rfm["Customer_Segment"].isin(["At Risk", "Cant Lose Them"])]\
              .nlargest(10, "Monetary")[["CustomerName", "Recency", "Frequency", "Monetary"]]
print(at_risk.to_string(index=False))

print("\n✅  CUSTOMER ANALYTICS COMPLETE — Run 04_advanced_analytics.py next")
