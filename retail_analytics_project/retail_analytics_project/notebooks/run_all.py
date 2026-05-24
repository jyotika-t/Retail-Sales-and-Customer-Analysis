"""
=============================================================
RETAIL SALES & CUSTOMER ANALYTICS PROJECT
run_all.py  —  Runs the complete pipeline in one click
=============================================================
Usage:
  python run_all.py

Or in Google Colab:
  !python run_all.py
=============================================================
"""

import subprocess
import sys
import os

STEPS = [
    ("01_data_cleaning.py",    "Step 1: Data Cleaning & Preprocessing"),
    ("02_eda_analysis.py",     "Step 2: Exploratory Data Analysis"),
    ("03_customer_analytics.py", "Step 3: Customer Analytics — RFM"),
    ("04_advanced_analytics.py", "Step 4: Advanced Analytics — Pareto, Cohort, Forecast"),
]

def run_step(script, title):
    print("\n" + "=" * 60)
    print(f"▶  {title}")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, script],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=False
    )
    if result.returncode != 0:
        print(f"\n❌  {script} FAILED with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"\n✅  {title} — DONE")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 60)
    print("🚀  RETAIL SALES & CUSTOMER ANALYTICS — FULL PIPELINE")
    print("=" * 60)
    for script, title in STEPS:
        run_step(script, title)
    print("\n" + "=" * 60)
    print("🎉  ALL STEPS COMPLETED SUCCESSFULLY!")
    print("     Charts saved in  → ../outputs/charts/")
    print("     Reports saved in → ../outputs/reports/")
    print("=" * 60)
