# 🏢 Enterprise HR People Analytics & Attrition Prediction Platform

**Tech Stack:** Python 3.13 | PostgreSQL 18 | XGBoost | scikit-learn | Power BI Desktop

A production-grade HR Data Warehouse featuring ML-powered attrition prediction, 1.6M+ rows of synthetic enterprise data, and a 5-page interactive Power BI dashboard.

## 📊 Dashboard Preview

![Executive Dashboard](Screenshot%202026-06-21%20031450.png)

![Attrition Deep Dive](Screenshot%202026-06-21%20031533.png)

![Predictive Analytics](Screenshot%202026-06-21%20031607.png)

## 🎯 Project Overview

This project simulates a real-world enterprise HR analytics platform used by multinational organizations to:
- Monitor workforce health and attrition trends
- Predict which employees are at risk of leaving
- Analyze training effectiveness and performance patterns
- Generate data-driven retention recommendations

## 🏗️ Architecture

Raw Data (CSV) → PostgreSQL Warehouse → Python Cleaning → ML Model → Power BI Dashboard

## 📁 Dataset

| Table | Rows | Description |
|---|---|---|
| fact_employee_history | 100,300 | Core employee lifecycle data |
| fact_attendance | 600,017 | Monthly attendance records |
| fact_performance_reviews | 350,004 | Quarterly review cycles |
| fact_training_records | 432,020 | Course enrollments and scores |
| dim_employees | 100,000 | Employee master |
| dim_managers | 15,000 | Manager hierarchy |
| dim_locations | 57 | Office locations |
| dim_departments | 40 | Department reference |
| dim_jobroles | 140 | Job role catalog |
| TOTAL | 1,597,578 | 224 MB |

## 🤖 Machine Learning

### Model Performance

| Model | AUC-ROC | Accuracy |
|---|---|---|
| Logistic Regression | 0.6780 | 84% |
| Random Forest | 0.7059 | 86% |
| XGBoost | 0.7238 | 87% |

### Top Attrition Drivers
1. BurnoutScore (18.1%)
2. ManagerRating (11.9%)
3. JobSatisfactionScore (9.7%)
4. PromotionLast3Years (9.7%)
5. YearsTenure (6.1%)

### Risk Categories
- Low Risk: 90,081 employees
- Medium Risk: 5,660 employees
- High Risk: 4,259 employees

## 📈 Power BI Dashboard

5 interactive pages with Basic/Advance toggle on every page:

| Page | Key Visuals |
|---|---|
| Executive Dashboard | KPI cards, attrition trend, revenue by industry, headcount |
| Workforce Analysis | Treemap, tenure bands, work mode, education breakdown |
| Attrition Deep Dive | Gauge, scatter plot, heatmap, treemap, area chart |
| Predictive Analytics | Risk gauge, risk matrix, high risk treemap, scatter |
| Attendance and Training | Absenteeism trend, overtime heatmap, training ROI |

### Dashboard Features
- Basic/Advance bookmark toggle on every page
- Page navigation buttons
- 4 cross-page slicers (Year, Country, Department, JobLevel)
- Conditional formatting heatmaps
- 20+ DAX measures
- Star schema data model

## 🔍 SQL Analytics

10 analytical queries covering:
- Executive KPI summary
- Attrition by department, age group, country
- Attrition reasons breakdown
- Salary analysis by job level
- Manager effect on attrition
- Training impact on performance
- High risk employee identification
- Diversity ratio by country

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.13 | Data generation, cleaning, ML |
| PostgreSQL 18 | Data warehouse |
| pandas, numpy | Data manipulation |
| scikit-learn | ML preprocessing |
| XGBoost | Attrition prediction |
| SQLAlchemy | Database connection |
| Power BI Desktop | Dashboards |
| VS Code | Development environment |

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Power BI Desktop

### Setup

1. Clone the repository

2. Create virtual environment
python -m venv hr_env

hr_env\Scripts\activate

3. Install dependencies
pip install numpy pandas faker openpyxl sqlalchemy psycopg2-binary scikit-learn xgboost matplotlib seaborn plotly jupyter

4. Set up PostgreSQL database
CREATE DATABASE hr_warehouse;

5. Load data into PostgreSQL
python load_to_postgres.py

6. Run data cleaning
python notebooks/data_cleaning.py

7. Train ML model
python ml/models/attrition_model.py

8. Open Power BI dashboard
Open dashboards/HR_Analytics_Dashboard.pbix in Power BI Desktop

## 📊 Key Business Insights

- Cost of Attrition: $87.96M annual cost of employee turnover
- Attrition Rate: 15.6% within healthy enterprise benchmark
- Burnout is #1 driver — employees with burnout above 70 are 2x more likely to leave
- Manager quality matters — teams with low manager ratings have 25% higher attrition
- Training works — employees with 60+ training hours show 20% lower attrition
- Internal L&D beats external — scores 81.87 vs 79.85 for external trainers

## 📂 Project Structure
hr-people-analytics-warehouse/

├── notebooks/

│   └── data_cleaning.py

├── sql/

│   └── analytics/

│       └── hr_analytics.sql

├── ml/

│   └── models/

│       └── attrition_model.py

├── dashboards/

│   └── screenshots/

├── load_to_postgres.py

└── README.md

## 👨‍💻 Author

**Jaikishan**
GitHub: https://github.com/jaikishanc007-lgtm

## ⭐ If you found this project useful please give it a star!
