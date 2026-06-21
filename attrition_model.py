import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings("ignore")

CLEAN_DIR = r"C:\Users\jaiki\Documents\hr_warehouse\data\processed"
OUTPUT_DIR = r"C:\Users\jaiki\Documents\hr_warehouse\ml\evaluation"

import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 55)
print("HR Attrition Prediction — Machine Learning")
print("=" * 55)

# ── LOAD CLEAN DATA ───────────────────────────────────────
print("\n1. Loading clean data...")
df = pd.read_csv(f"{CLEAN_DIR}\\fact_employee_history_clean.csv")
print(f"   Rows: {len(df):,} | Columns: {len(df.columns)}")

# ── FEATURE SELECTION ─────────────────────────────────────
print("\n2. Selecting features...")
FEATURES = [
    "Age", "YearsTenure", "YearsInCurrentRole",
    "BaseSalary", "LastSalaryIncreasePercent", "BonusPercent",
    "PerformanceRating", "ManagerRating", "PromotionLast3Years",
    "TrainingHours", "CertificationCount",
    "JobSatisfactionScore", "WorkLifeBalanceScore",
    "EngagementScore", "BurnoutScore",
    "AbsenteeismDays", "OvertimeHoursPerMonth",
    "DistanceFromOffice", "ProjectCount",
    "Gender", "MaritalStatus", "EducationLevel",
    "JobLevel", "Department", "Country", "WorkMode",
]

TARGET = "Attrition"

df_ml = df[FEATURES + [TARGET]].copy()
df_ml[TARGET] = (df_ml[TARGET] == "Yes").astype(int)

# ── ENCODE CATEGORICAL COLUMNS ────────────────────────────
print("\n3. Encoding categorical columns...")
cat_cols = ["Gender","MaritalStatus","EducationLevel","JobLevel",
            "Department","Country","WorkMode"]

le = LabelEncoder()
for col in cat_cols:
    df_ml[col] = le.fit_transform(df_ml[col].astype(str))

print(f"   Encoded {len(cat_cols)} categorical columns")

# ── TRAIN TEST SPLIT ──────────────────────────────────────
print("\n4. Splitting data...")
X = df_ml[FEATURES]
y = df_ml[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"   Train: {len(X_train):,} rows")
print(f"   Test:  {len(X_test):,} rows")
print(f"   Attrition rate in test: {y_test.mean()*100:.1f}%")

# ── TRAIN MODELS ──────────────────────────────────────────
print("\n5. Training models...")

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost":             XGBClassifier(n_estimators=200, learning_rate=0.05,
                                         max_depth=6, random_state=42,
                                         eval_metric="logloss"),
}

results = {}
for name, model in models.items():
    print(f"\n   Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    results[name] = {"model": model, "auc": auc, "y_pred": y_pred, "y_prob": y_prob}
    print(f"   AUC-ROC: {auc:.4f}")

# ── BEST MODEL ────────────────────────────────────────────
best_name = max(results, key=lambda x: results[x]["auc"])
best = results[best_name]
print(f"\n6. Best model: {best_name} (AUC = {best['auc']:.4f})")

print("\n   Classification Report:")
print(classification_report(y_test, best["y_pred"],
      target_names=["Active","Attrited"]))

# ── FEATURE IMPORTANCE ────────────────────────────────────
print("\n7. Top 15 features driving attrition:")
xgb_model = results["XGBoost"]["model"]
importance = pd.DataFrame({
    "Feature": FEATURES,
    "Importance": xgb_model.feature_importances_
}).sort_values("Importance", ascending=False)

for _, row in importance.head(15).iterrows():
    bar = "█" * int(row["Importance"] * 200)
    print(f"   {row['Feature']:<30} {row['Importance']:.4f} {bar}")

# ── GENERATE RISK SCORES ──────────────────────────────────
print("\n8. Generating risk scores for all employees...")
xgb_model_full = XGBClassifier(n_estimators=200, learning_rate=0.05,
                                 max_depth=6, random_state=42,
                                 eval_metric="logloss")
xgb_model_full.fit(X, y)
proba = xgb_model_full.predict_proba(X)[:, 1]
df["ML_RiskScore"] = (proba * 100).round(1)
df["RiskCategory"] = pd.cut(
    df["ML_RiskScore"],
    bins=[0, 30, 60, 100],
    labels=["Low", "Medium", "High"]
)

# Save risk scores
risk_output = df[["EmployeeID","EmployeeName","Department","Country",
                   "JobLevel","Attrition","AttritionRiskScore","ML_RiskScore","RiskCategory"]]
risk_output.to_csv(f"{OUTPUT_DIR}\\employee_risk_scores.csv", index=False)

print(f"\n   Risk category distribution:")
print(f"   Low risk:    {(df['RiskCategory']=='Low').sum():,} employees")
print(f"   Medium risk: {(df['RiskCategory']=='Medium').sum():,} employees")
print(f"   High risk:   {(df['RiskCategory']=='High').sum():,} employees")

# ── MODEL COMPARISON ─────────────────────────────────────
print("\n9. Model comparison summary:")
print(f"   {'Model':<25} {'AUC-ROC':>10}")
print(f"   {'-'*35}")
for name, res in sorted(results.items(), key=lambda x: x[1]['auc'], reverse=True):
    print(f"   {name:<25} {res['auc']:>10.4f}")

print(f"\n   Risk scores saved to ml\\evaluation\\employee_risk_scores.csv")
print("\n" + "=" * 55)
print("Machine Learning complete!")
print("=" * 55)