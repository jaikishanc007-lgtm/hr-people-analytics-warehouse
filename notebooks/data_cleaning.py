import pandas as pd
import numpy as np
import os

DATA_DIR = r"data\raw"
CLEAN_DIR = r"data\raw"
os.makedirs(CLEAN_DIR, exist_ok=True)

print("=" * 55)
print("HR Data Warehouse — Data Cleaning & EDA")
print("=" * 55)

# ── LOAD MAIN TABLE ───────────────────────────────────────
print("\n1. Loading fact_employee_history.csv...")
df = pd.read_csv(f"{DATA_DIR}\\fact_employee_history.csv")
print(f"   Raw rows: {len(df):,}")
print(f"   Columns:  {len(df.columns)}")

# ── CHECK DUPLICATES ──────────────────────────────────────
print("\n2. Checking duplicates...")
dupes = df[df["EmployeeID"].astype(str).str.endswith("_DUP")]
clean = df[~df["EmployeeID"].astype(str).str.endswith("_DUP")]
print(f"   Duplicate rows found: {len(dupes):,}")
print(f"   Clean rows:           {len(clean):,}")

# ── MISSING VALUES ────────────────────────────────────────
print("\n3. Missing values report:")
missing = df.isnull().sum()
missing = missing[missing > 0]
for col, count in missing.items():
    pct = count / len(df) * 100
    print(f"   {col:<35} {count:>6,} missing ({pct:.1f}%)")

# ── FIX MISSING VALUES ────────────────────────────────────
print("\n4. Fixing missing values...")
clean["ManagerRating"]           = clean["ManagerRating"].fillna(clean["ManagerRating"].median())
clean["EngagementScore"]         = clean["EngagementScore"].fillna(clean["EngagementScore"].median())
clean["TrainingHours"]           = clean["TrainingHours"].fillna(clean["TrainingHours"].median())
clean["CustomerSatisfactionScore"] = clean["CustomerSatisfactionScore"].fillna(clean["CustomerSatisfactionScore"].median())
print("   Done — filled with median values")

# ── FIX DEPARTMENT NAMING ─────────────────────────────────
print("\n5. Fixing department name inconsistencies...")
dept_fixes = {
    "Engg":           "Engineering",
    "Finance & Accts":"Finance & Accounting",
    "HR Dept":        "HR",
    "IT":             "IT Operations",
}
before = clean["Department"].nunique()
clean["Department"] = clean["Department"].replace(dept_fixes)
after = clean["Department"].nunique()
print(f"   Unique departments before: {before}")
print(f"   Unique departments after:  {after}")

# ── OUTLIER DETECTION ─────────────────────────────────────
print("\n6. Outlier detection:")
# Salary outliers
q1 = clean["BaseSalary"].quantile(0.25)
q3 = clean["BaseSalary"].quantile(0.75)
iqr = q3 - q1
salary_outliers = clean[(clean["BaseSalary"] < q1 - 1.5*iqr) | (clean["BaseSalary"] > q3 + 1.5*iqr)]
print(f"   Salary outliers:   {len(salary_outliers):,} rows")

# Overtime outliers
overtime_outliers = clean[clean["OvertimeHoursPerMonth"] > 50]
print(f"   Overtime outliers: {len(overtime_outliers):,} rows (>50 hrs/month)")

# ── DATA TYPES ────────────────────────────────────────────
print("\n7. Fixing data types...")
clean["HireDate"] = pd.to_datetime(clean["HireDate"])
clean["ExitDate"]  = pd.to_datetime(clean["ExitDate"], errors="coerce")
print("   HireDate and ExitDate converted to datetime")

# ── SUMMARY STATS ─────────────────────────────────────────
print("\n8. Key statistics:")
print(f"   Attrition rate:     {(clean['Attrition']=='Yes').mean()*100:.1f}%")
print(f"   Avg salary:         ${clean['BaseSalary'].mean():,.0f}")
print(f"   Avg burnout score:  {clean['BurnoutScore'].mean():.1f}")
print(f"   Avg engagement:     {clean['EngagementScore'].mean():.1f}")
print(f"   Avg training hours: {clean['TrainingHours'].mean():.1f}")
print(f"   Countries:          {clean['Country'].nunique()}")
print(f"   Departments:        {clean['Department'].nunique()}")
print(f"   Job levels:         {clean['JobLevel'].nunique()}")

# ── ATTRITION BY REASON ───────────────────────────────────
print("\n9. Attrition reasons:")
reasons = clean[clean["Attrition"]=="Yes"]["AttritionReason"].value_counts()
for reason, count in reasons.items():
    pct = count / (clean["Attrition"]=="Yes").sum() * 100
    print(f"   {reason:<25} {count:>5,} ({pct:.1f}%)")

# ── SAVE CLEAN DATA ───────────────────────────────────────
print("\n10. Saving cleaned data...")
clean.to_csv(f"{CLEAN_DIR}\\fact_employee_history_clean.csv", index=False)
print(f"    Saved to data\\processed\\fact_employee_history_clean.csv")
print(f"    Clean rows: {len(clean):,}")

print("\n" + "=" * 55)
print("Data cleaning complete!")
print("=" * 55)
