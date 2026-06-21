import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os

password = quote_plus("yourpassword")
engine = create_engine(f"postgresql://postgres:{password}@localhost/hr_warehouse")

DATA_DIR = r"data\raw"

# Load order matters — dimensions first, then facts
tables = [
    ("dim_locations",           "dim_locations.csv"),
    ("dim_departments",         "dim_departments.csv"),
    ("dim_jobroles",            "dim_jobroles.csv"),
    ("dim_employees",           "dim_employees.csv"),
    ("dim_managers",            "dim_managers.csv"),
    ("fact_employee_history",   "fact_employee_history.csv"),
    ("fact_attendance",         "fact_attendance.csv"),
    ("fact_performance_reviews","fact_performance_reviews.csv"),
    ("fact_training_records",   "fact_training_records.csv"),
]

print("Loading data into PostgreSQL...\n")

for table_name, file_name in tables:
    path = os.path.join(DATA_DIR, file_name)
    print(f"Loading {table_name}...")
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists="replace", index=False, chunksize=5000)
    print(f"  Done — {len(df):,} rows loaded\n")

print("All tables loaded successfully!")

# Quick check
with engine.connect() as conn:
    for table, _ in tables:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()[0]
        print(f"  {table:<35} {count:>10,} rows")
