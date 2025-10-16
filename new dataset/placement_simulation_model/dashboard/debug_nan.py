"""
Debug script to find NaN values in student data
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load the data
BASE_DIR = Path(__file__).parent.parent.parent
STUDENTS_FILE = BASE_DIR / "analysis_data.csv"

print("Loading student data...")
df = pd.read_csv(STUDENTS_FILE)

print(f"\nTotal students: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")

# Check for NaN values in each column
print("\n" + "="*80)
print("NaN VALUES BY COLUMN:")
print("="*80)

for col in df.columns:
    nan_count = df[col].isna().sum()
    if nan_count > 0:
        print(f"{col}: {nan_count} NaN values ({nan_count/len(df)*100:.1f}%)")

# Check for inf values
print("\n" + "="*80)
print("INF VALUES BY COLUMN:")
print("="*80)

for col in df.columns:
    if df[col].dtype in ['float64', 'int64']:
        inf_count = np.isinf(df[col]).sum()
        if inf_count > 0:
            print(f"{col}: {inf_count} inf values")

# Sample a few rows to see the data
print("\n" + "="*80)
print("SAMPLE DATA (first 5 rows):")
print("="*80)
print(df.head().to_string())

# Check specific columns that might cause issues
print("\n" + "="*80)
print("CHECKING SPECIFIC COLUMNS:")
print("="*80)

# Check for any string "nan" values
for col in df.columns:
    if df[col].dtype == 'object':
        nan_str_count = (df[col].astype(str).str.lower() == 'nan').sum()
        if nan_str_count > 0:
            print(f"{col}: {nan_str_count} string 'nan' values")

# Replace NaN and convert to dict to see what JSON would look like
print("\n" + "="*80)
print("TESTING JSON SERIALIZATION:")
print("="*80)

test_df = df.head(2).copy()
test_df = test_df.replace([np.nan, np.inf, -np.inf], None)
records = test_df.to_dict(orient='records')

import json
try:
    json_str = json.dumps(records)
    print("✓ JSON serialization successful")
except Exception as e:
    print(f"✗ JSON serialization failed: {e}")
    print("\nProblematic records:")
    for i, record in enumerate(records):
        try:
            json.dumps(record)
        except Exception as e2:
            print(f"Record {i}: {e2}")
            print(f"Data: {record}")
