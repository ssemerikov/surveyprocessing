#!/usr/bin/env python3
"""
Generate comprehensive analysis report with proper column identification.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

print("=" * 80)
print("COMPREHENSIVE ANALYSIS - UKRAINIAN EDUCATION SURVEY")
print("=" * 80)
print()

# Load data
df = pd.read_csv('data/raw/answers.csv')
cols = df.columns

# Identify key columns by their question numbers
timestamp_col = cols[0]  # Timestamp
age_col = cols[1]  # Q1: Age
gender_col = cols[2]  # Q2: Gender
grade_col = cols[3]  # Q3: Grade
region_col = cols[4]  # Q4: Region
settlement_col = cols[5]  # Q5: Settlement type
school_type_col = cols[6]  # Q6: School type
ownership_col = cols[7]  # Q7: Ownership
format_col = cols[8]  # Q8: Educational format
shifts_col = cols[9]  # Q9: Shifts
platform_col = cols[10]  # Q10: Platform
platform_other_col = cols[11]  # Q10: Platform (other)
services_col = cols[12]  # Q11: Services used
services_other_col = cols[13]  # Q11: Services (other)
tech_support_col = cols[14]  # Q12: Tech support satisfaction
journal_access_col = cols[15]  # Q13: Journal access
website_quality_col = cols[16]  # Q14: Website quality
website_features_col = cols[17]  # Q15: Website features
communication_col = cols[18]  # Q16: Communication channels
communication_other_col = cols[19]  # Q16: Communication (other)
teacher_feedback_col = cols[20]  # Q17: Teacher feedback
parent_survey_col = cols[21]  # Q18: Parent surveys
child_skills_col = cols[22]  # Q19: Child's digital skills
learning_independence_col = cols[23]  # Q20: Learning independence
device_access_col = cols[24]  # Q21: Device access
suggestions_col = cols[25]  # Q22: Suggestions

# Create comprehensive analysis
output = []

def add_section(title):
    output.append("")
    output.append("=" * 80)
    output.append(title)
    output.append("=" * 80)
    output.append("")

def add_subsection(title):
    output.append("")
    output.append("-" * 80)
    output.append(title)
    output.append("-" * 80)

def add_frequency(df, col, title, top_n=None):
    add_subsection(title)
    counts = df[col].value_counts()
    if top_n:
        counts = counts.head(top_n)
    total = len(df)
    for value, count in counts.items():
        pct = (count / total) * 100
        value_str = str(value)[:60] if pd.notna(value) else "Missing"
        output.append(f"  {value_str:<60} {count:>5} ({pct:>5.2f}%)")

# Header
add_section("UKRAINIAN EDUCATION SURVEY - COMPREHENSIVE ANALYSIS")
output.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
output.append(f"Total Responses: {len(df):,}")
output.append(f"Data Quality: {df.notna().all(axis=1).sum()} complete rows ({(df.notna().all(axis=1).sum() / len(df) * 100):.1f}%)")

# 1. DEMOGRAPHICS
add_section("1. RESPONDENT DEMOGRAPHICS")

add_frequency(df, age_col, "1.1 Age Distribution")
add_frequency(df, gender_col, "1.2 Gender Distribution")
add_frequency(df, region_col, "1.3 Regional Distribution (Top 15)", top_n=15)
add_frequency(df, settlement_col, "1.4 Settlement Type")

# 2. SCHOOL CHARACTERISTICS
add_section("2. SCHOOL CHARACTERISTICS")

add_frequency(df, school_type_col, "2.1 School Type")
add_frequency(df, ownership_col, "2.2 School Ownership")
add_frequency(df, format_col, "2.3 Educational Format")
add_frequency(df, shifts_col, "2.4 School Shifts")

# 3. DIGITAL PLATFORMS & INFRASTRUCTURE
add_section("3. DIGITAL PLATFORMS & INFRASTRUCTURE")

add_frequency(df, platform_col, "3.1 Educational Platforms Used (Top 20)", top_n=20)
add_frequency(df, services_col, "3.2 Digital Services Used (Top 20)", top_n=20)
add_frequency(df, communication_col, "3.3 Communication Channels (Top 20)", top_n=20)

# 4. ACCESS & SATISFACTION
add_section("4. ACCESS & SATISFACTION")

add_frequency(df, tech_support_col, "4.1 Technical Support Satisfaction")
add_frequency(df, journal_access_col, "4.2 Electronic Journal Access")
add_frequency(df, website_quality_col, "4.3 Website Quality Assessment")
add_frequency(df, device_access_col, "4.4 Device Access for Learning")

# 5. STUDENT DIGITAL COMPETENCIES
add_section("5. STUDENT DIGITAL COMPETENCIES")

add_frequency(df, child_skills_col, "5.1 Child's Digital Skills")
add_frequency(df, learning_independence_col, "5.2 Learning Independence")

# 6. PARENT ENGAGEMENT
add_section("6. PARENT ENGAGEMENT")

add_frequency(df, teacher_feedback_col, "6.1 Teacher Feedback Availability")
add_frequency(df, parent_survey_col, "6.2 School Parent Surveys")

# 7. TEXT ANALYSIS - SUGGESTIONS
add_section("7. IMPROVEMENT SUGGESTIONS (Question 22)")

suggestions = df[suggestions_col].dropna()
output.append(f"Total Responses with Suggestions: {len(suggestions):,} ({(len(suggestions) / len(df) * 100):.1f}%)")
output.append(f"Empty Responses: {df[suggestions_col].isna().sum():,}")
output.append("")

# Sample suggestions
output.append("Sample Suggestions (first 10):")
for i, suggestion in enumerate(suggestions.head(10), 1):
    suggestion_text = str(suggestion)[:100]
    output.append(f"  {i}. {suggestion_text}...")

# 8. GRADE DISTRIBUTION
add_section("8. GRADE/CLASS DISTRIBUTION")

# Parse grade information (Question 3)
grades_raw = df[grade_col].dropna()
output.append(f"Responses with grade information: {len(grades_raw):,}")
output.append("")

# Count grade mentions
grade_counts = {}
for grades_str in grades_raw:
    # Split by common delimiters
    for delimiter in [',', ';']:
        if delimiter in str(grades_str):
            individual_grades = [g.strip() for g in str(grades_str).split(delimiter)]
            for grade in individual_grades:
                if grade and any(char.isdigit() for char in grade):
                    grade_counts[grade] = grade_counts.get(grade, 0) + 1

if grade_counts:
    add_subsection("Grade Mentions (from Question 3)")
    for grade in sorted(grade_counts.keys()):
        count = grade_counts[grade]
        output.append(f"  {grade:<30} {count:>5}")

# Save report
report_path = "reports/comprehensive_analysis.txt"
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"✓ Comprehensive report generated: {report_path}")
print(f"  Total sections: 8")
print(f"  Total lines: {len(output)}")

# Generate summary statistics for Excel
excel_path = "reports/detailed_statistics.xlsx"
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    # Sheet 1: Overview
    overview = pd.DataFrame({
        'Metric': [
            'Total Responses',
            'Complete Responses',
            'Responses with Suggestions',
            'Unique Regions',
            'Analysis Date'
        ],
        'Value': [
            len(df),
            df.notna().all(axis=1).sum(),
            len(suggestions),
            df[region_col].nunique(),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
    })
    overview.to_excel(writer, sheet_name='Overview', index=False)

    # Sheet 2-10: Frequency tables for key variables
    def write_frequency_sheet(df, col, sheet_name):
        freq = df[col].value_counts().reset_index()
        freq.columns = ['Value', 'Count']
        freq['Percentage'] = (freq['Count'] / len(df) * 100).round(2)
        freq.to_excel(writer, sheet_name=sheet_name[:31], index=False)

    write_frequency_sheet(df, age_col, 'Age')
    write_frequency_sheet(df, gender_col, 'Gender')
    write_frequency_sheet(df, region_col, 'Region')
    write_frequency_sheet(df, format_col, 'Educational_Format')
    write_frequency_sheet(df, tech_support_col, 'Tech_Support')
    write_frequency_sheet(df, journal_access_col, 'Journal_Access')
    write_frequency_sheet(df, child_skills_col, 'Digital_Skills')
    write_frequency_sheet(df, device_access_col, 'Device_Access')

print(f"✓ Detailed statistics Excel: {excel_path}")

print()
print("=" * 80)
print("COMPREHENSIVE ANALYSIS COMPLETE")
print("=" * 80)
