"""
Analyze Day 1 Placement Results
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load results
base_dir = Path(r"c:\Users\nigam\Desktop\Simulation 2nd Presentation\new dataset")
results_file = base_dir / "day1_placement_results.csv"

df = pd.read_csv(results_file)

print("="*80)
print("DAY 1 PLACEMENT RESULTS - DETAILED ANALYSIS")
print("="*80)

# Overall statistics
print("\n1. OVERALL STATISTICS")
print("-"*80)
print(f"Total Students: {len(df)}")
print(f"\nStatus Distribution:")
print(df['status'].value_counts())
print(f"\nPercentages:")
for status, count in df['status'].value_counts().items():
    print(f"  {status}: {count/len(df)*100:.2f}%")

# Department-wise analysis
print("\n2. DEPARTMENT-WISE PLACEMENT RATE")
print("-"*80)
dept_stats = df.groupby('department')['status'].apply(lambda x: (x == 'Placed').sum())
dept_total = df.groupby('department').size()
dept_placement_rate = (dept_stats / dept_total * 100).sort_values(ascending=False)

print("\nTop 10 Departments by Placement Rate:")
for dept, rate in dept_placement_rate.head(10).items():
    placed = dept_stats[dept]
    total = dept_total[dept]
    print(f"  {dept}: {placed}/{total} ({rate:.1f}%)")

# CGPA analysis
print("\n3. CGPA ANALYSIS OF PLACED STUDENTS")
print("-"*80)
placed_students = df[df['status'] == 'Placed']
if len(placed_students) > 0:
    print(f"Mean CGPA of placed students: {placed_students['cgpa'].mean():.2f}")
    print(f"Median CGPA of placed students: {placed_students['cgpa'].median():.2f}")
    print(f"Min CGPA of placed students: {placed_students['cgpa'].min():.2f}")
    print(f"Max CGPA of placed students: {placed_students['cgpa'].max():.2f}")
    
    print(f"\nMean CGPA of unplaced students: {df[df['status']=='Unplaced']['cgpa'].mean():.2f}")

# Domain analysis
print("\n4. DOMAIN-WISE PLACEMENT ANALYSIS")
print("-"*80)
domain1_placed = placed_students['domain_1'].value_counts()
print("\nPlacements by Primary Domain:")
for domain, count in domain1_placed.items():
    print(f"  {domain}: {count}")

# Company-wise placements
print("\n5. COMPANY-WISE PLACEMENTS")
print("-"*80)
company_placements = placed_students['placed_company'].value_counts()
print(f"\nTotal Companies that hired: {len(company_placements)}")
print(f"\nTop 15 Companies by Placements:")
for i, (company, count) in enumerate(company_placements.head(15).items(), 1):
    print(f"  {i}. {company}: {count}")

# Sample placed students
print("\n6. SAMPLE PLACED STUDENTS (First 20)")
print("-"*80)
sample_placed = placed_students[['roll_no', 'name', 'department', 'cgpa', 'domain_1', 'placed_company']].head(20)
for _, row in sample_placed.iterrows():
    print(f"  {row['roll_no']} | {row['department']} | CGPA: {row['cgpa']} | {row['domain_1']} → {row['placed_company']}")

# CGPA distribution
print("\n7. CGPA DISTRIBUTION OF PLACEMENTS")
print("-"*80)
cgpa_bins = [6.0, 7.0, 8.0, 8.5, 9.0, 9.5, 10.0]
placed_students['cgpa_bin'] = pd.cut(placed_students['cgpa'], bins=cgpa_bins)
print(placed_students['cgpa_bin'].value_counts().sort_index())

# High CGPA students analysis
print("\n8. HIGH CGPA STUDENTS (9.5+)")
print("-"*80)
high_cgpa = df[df['cgpa'] >= 9.5]
high_cgpa_placed = high_cgpa[high_cgpa['status'] == 'Placed']
print(f"Total students with CGPA >= 9.5: {len(high_cgpa)}")
print(f"Placed: {len(high_cgpa_placed)} ({len(high_cgpa_placed)/len(high_cgpa)*100:.1f}%)")
print(f"Unplaced: {len(high_cgpa[high_cgpa['status']=='Unplaced'])}")
print(f"Opted Out: {len(high_cgpa[high_cgpa['status']=='Opted_Out'])}")

if len(high_cgpa_placed) > 0:
    print(f"\nCompanies that hired students with CGPA >= 9.5:")
    for company, count in high_cgpa_placed['placed_company'].value_counts().items():
        print(f"  {company}: {count}")

# Save detailed analysis
output_file = base_dir / "day1_detailed_analysis.txt"
with open(output_file, 'w') as f:
    f.write("="*80 + "\n")
    f.write("DAY 1 PLACEMENT RESULTS - DETAILED ANALYSIS\n")
    f.write("="*80 + "\n\n")
    
    f.write("1. OVERALL STATISTICS\n")
    f.write("-"*80 + "\n")
    f.write(f"Total Students: {len(df)}\n\n")
    f.write("Status Distribution:\n")
    f.write(df['status'].value_counts().to_string() + "\n\n")
    
    f.write("2. DEPARTMENT-WISE PLACEMENT RATE\n")
    f.write("-"*80 + "\n")
    for dept, rate in dept_placement_rate.items():
        placed = dept_stats[dept]
        total = dept_total[dept]
        f.write(f"{dept}: {placed}/{total} ({rate:.1f}%)\n")
    
    f.write("\n3. COMPANY-WISE PLACEMENTS\n")
    f.write("-"*80 + "\n")
    for company, count in company_placements.items():
        f.write(f"{company}: {count}\n")

print(f"\n\nDetailed analysis saved to: {output_file}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
