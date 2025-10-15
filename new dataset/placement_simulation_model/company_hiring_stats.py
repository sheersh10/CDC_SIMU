import pandas as pd

# Load results
df = pd.read_csv('day1_placement_results.csv')
placed = df[df['status'] == 'Placed']

# Get company-wise statistics
company_stats = placed.groupby('placed_company').size().reset_index(name='students_hired')
company_stats = company_stats.sort_values('students_hired', ascending=False)

print("="*80)
print("COMPANY-WISE HIRING STATISTICS (DAY 1)")
print("="*80)
print(f"\nTotal Companies That Hired: {len(company_stats)}")
print(f"Total Students Placed: {len(placed)}\n")

print(f"{'Rank':<6} {'Company':<50} {'Students Hired':>15}")
print("-"*80)

for idx, (_, row) in enumerate(company_stats.iterrows(), 1):
    print(f"{idx:<6} {row['placed_company']:<50} {row['students_hired']:>15}")

print("="*80)

# Additional statistics
print(f"\n{'SUMMARY STATISTICS':^80}")
print("="*80)
print(f"Average hires per company: {company_stats['students_hired'].mean():.2f}")
print(f"Median hires per company: {company_stats['students_hired'].median():.0f}")
print(f"Maximum hires by one company: {company_stats['students_hired'].max()}")
print(f"Minimum hires by companies that hired: {company_stats['students_hired'].min()}")

# Top 10
print(f"\n{'TOP 10 COMPANIES BY HIRING':^80}")
print("="*80)
top10 = company_stats.head(10)
for idx, (_, row) in enumerate(top10.iterrows(), 1):
    print(f"{idx:2}. {row['placed_company']:<45} → {row['students_hired']:>3} students")

# Companies that made 0 hires
companies_with_0_hires = df[df['status'] != 'Placed'].groupby('placed_company').size()
if 'nan' not in str(companies_with_0_hires.index):
    print(f"\n{'COMPANIES WITH 0 HIRES':^80}")
    print("="*80)
    # From simulation output, we know these companies visited but didn't hire
    zero_hire_companies = [
        'Adobe_Software (MDSR)',
        'HUL_Supply Chain',
        'ITC_KITES Intern',
        'JPMC_CCB',
        'JPMC_MRGR',
        'JPMC_QR'
    ]
    for company in zero_hire_companies:
        print(f"  - {company}")

print("\n" + "="*80)
