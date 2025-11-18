#!/usr/bin/env python3
"""
Run complete survey analysis and generate reports.
Simplified version that works with available dependencies.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import pandas as pd
import yaml

print("=" * 80)
print("UKRAINIAN EDUCATION SURVEY - DATA ANALYSIS")
print("=" * 80)
print(f"Analysis started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Create output directories
Path("data/processed").mkdir(parents=True, exist_ok=True)
Path("reports").mkdir(parents=True, exist_ok=True)

# Step 1: Load Data
print("Step 1: Loading Data...")
print("-" * 80)

try:
    data_file = "data/raw/answers.csv"
    df = pd.read_csv(data_file, encoding='utf-8')
    print(f"✓ Data loaded successfully")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    print()
except Exception as e:
    print(f"✗ Error loading data: {e}")
    sys.exit(1)

# Step 2: Data Summary
print("Step 2: Generating Data Summary...")
print("-" * 80)

summary = {
    'total_responses': len(df),
    'total_columns': len(df.columns),
    'memory_usage_mb': round(df.memory_usage(deep=True).sum() / 1024**2, 2),
    'column_names': df.columns.tolist()
}

print(f"Total Responses: {summary['total_responses']:,}")
print(f"Total Questions: {summary['total_columns']}")
print(f"Memory Usage: {summary['memory_usage_mb']} MB")
print()

# Step 3: Data Quality Check
print("Step 3: Data Quality Assessment...")
print("-" * 80)

# Missing data analysis
missing_data = df.isna().sum()
missing_pct = (missing_data / len(df)) * 100

print(f"Complete rows: {df.notna().all(axis=1).sum():,} ({(df.notna().all(axis=1).sum() / len(df) * 100):.1f}%)")
print(f"Rows with missing data: {df.isna().any(axis=1).sum():,} ({(df.isna().any(axis=1).sum() / len(df) * 100):.1f}%)")

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"Duplicate responses: {duplicates}")
print()

# Step 4: Descriptive Statistics
print("Step 4: Descriptive Statistics...")
print("-" * 80)

# Find key columns
timestamp_col = df.columns[0]  # First column is timestamp
region_col = None
grade_col = None

for col in df.columns:
    if 'област' in col.lower():
        region_col = col
    if 'клас' in col.lower():
        grade_col = col

# Response distribution by region
if region_col:
    print(f"\nTop 10 Regions by Response Count:")
    region_counts = df[region_col].value_counts().head(10)
    for region, count in region_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {region:<30} {count:>5} ({pct:>5.2f}%)")

# Response distribution by grade
if grade_col:
    print(f"\nGrade Distribution:")
    grade_counts = df[grade_col].value_counts().sort_index()
    for grade, count in grade_counts.items():
        pct = (count / len(df)) * 100
        print(f"  Grade {grade:<20} {count:>5} ({pct:>5.2f}%)")

print()

# Step 5: Generate Reports
print("Step 5: Generating Reports...")
print("-" * 80)

# Export summary to text
summary_path = "reports/analysis_summary.txt"
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("UKRAINIAN EDUCATION SURVEY - ANALYSIS SUMMARY\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Data Source: {data_file}\n\n")

    f.write("DATASET OVERVIEW\n")
    f.write("-" * 80 + "\n")
    f.write(f"Total Responses: {len(df):,}\n")
    f.write(f"Total Questions: {len(df.columns)}\n")
    f.write(f"Memory Usage: {summary['memory_usage_mb']} MB\n")
    f.write(f"Duplicate Responses: {duplicates}\n\n")

    f.write("DATA QUALITY\n")
    f.write("-" * 80 + "\n")
    f.write(f"Complete Rows: {df.notna().all(axis=1).sum():,} ({(df.notna().all(axis=1).sum() / len(df) * 100):.1f}%)\n")
    f.write(f"Rows with Missing Data: {df.isna().any(axis=1).sum():,} ({(df.isna().any(axis=1).sum() / len(df) * 100):.1f}%)\n\n")

    if region_col:
        f.write("TOP 10 REGIONS\n")
        f.write("-" * 80 + "\n")
        for region, count in region_counts.items():
            pct = (count / len(df)) * 100
            f.write(f"{region:<30} {count:>5} ({pct:>5.2f}%)\n")
        f.write("\n")

    if grade_col:
        f.write("GRADE DISTRIBUTION\n")
        f.write("-" * 80 + "\n")
        for grade, count in grade_counts.items():
            pct = (count / len(df)) * 100
            f.write(f"Grade {grade:<20} {count:>5} ({pct:>5.2f}%)\n")

print(f"✓ Text summary exported: {summary_path}")

# Export to Excel
excel_path = "reports/analysis_results.xlsx"
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    # Overview sheet
    overview_data = {
        'Metric': [
            'Total Responses',
            'Total Questions',
            'Complete Rows',
            'Rows with Missing',
            'Duplicate Responses',
            'Analysis Date'
        ],
        'Value': [
            f"{len(df):,}",
            len(df.columns),
            f"{df.notna().all(axis=1).sum():,} ({(df.notna().all(axis=1).sum() / len(df) * 100):.1f}%)",
            f"{df.isna().any(axis=1).sum():,} ({(df.isna().any(axis=1).sum() / len(df) * 100):.1f}%)",
            duplicates,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
    }
    pd.DataFrame(overview_data).to_excel(writer, sheet_name='Overview', index=False)

    # Regional distribution
    if region_col:
        region_df = df[region_col].value_counts().reset_index()
        region_df.columns = ['Region', 'Count']
        region_df['Percentage'] = (region_df['Count'] / len(df) * 100).round(2)
        region_df.to_excel(writer, sheet_name='Regional_Distribution', index=False)

    # Grade distribution
    if grade_col:
        grade_df = df[grade_col].value_counts().reset_index()
        grade_df.columns = ['Grade', 'Count']
        grade_df['Percentage'] = (grade_df['Count'] / len(df) * 100).round(2)
        grade_df.to_excel(writer, sheet_name='Grade_Distribution', index=False)

    # Missing data analysis
    missing_df = pd.DataFrame({
        'Column': missing_data.index,
        'Missing_Count': missing_data.values,
        'Missing_Percentage': missing_pct.values
    }).round(2)
    missing_df.to_excel(writer, sheet_name='Missing_Data', index=False)

    # First 100 responses (sample)
    df.head(100).to_excel(writer, sheet_name='Sample_Data', index=False)

print(f"✓ Excel report exported: {excel_path}")

# Export processed data
processed_path = "data/processed/survey_data_processed.csv"
df.to_csv(processed_path, index=False, encoding='utf-8')
print(f"✓ Processed data exported: {processed_path}")

print()
print("=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print()
print("Generated Files:")
print(f"  1. {summary_path}")
print(f"  2. {excel_path}")
print(f"  3. {processed_path}")
print()
print(f"Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
