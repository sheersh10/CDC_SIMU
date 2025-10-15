import pandas as pd
from pathlib import Path

# Load results
results_df = pd.read_csv('day1_placement_results.csv')
placed = results_df[results_df['status'] == 'Placed']
company_stats = placed.groupby('placed_company').size().reset_index(name='hired')

# Load companies data
base_dir = Path(__file__).parent.parent
companies_df = pd.read_csv(base_dir / 'companies.csv')
companies_df['company_id'] = companies_df['company_name'] + '_' + companies_df['job_role']

# Filter Day 1 companies
day1 = companies_df[companies_df['arrival_day'] == 1][['company_id', 'min_offers', 'max_offers']]

# Merge with actual hires
merged = pd.merge(day1, company_stats, left_on='company_id', right_on='placed_company', how='left')
merged['hired'] = merged['hired'].fillna(0).astype(int)
merged['meets_min'] = merged['hired'] >= merged['min_offers']

print("="*90)
print("VERIFICATION: Companies Meeting Minimum Hiring Requirements")
print("="*90)
print(f"\n{'Company':<50} {'Min':>5} {'Hired':>7} {'Max':>5} {'Status':>15}")
print("-"*90)

for _, row in merged.iterrows():
    status = '✓ MEETS MIN' if row['meets_min'] else '✗ BELOW MIN'
    print(f"{row['company_id']:<50} {row['min_offers']:>5} {row['hired']:>7} {row['max_offers']:>5} {status:>15}")

print("="*90)

# Summary
total_companies = len(merged)
meeting_min = merged['meets_min'].sum()
failing = merged[~merged['meets_min']]

print(f"\nSUMMARY:")
print(f"  Total Day 1 Companies: {total_companies}")
print(f"  Meeting Minimum: {meeting_min} ({meeting_min/total_companies*100:.1f}%)")
print(f"  Below Minimum: {len(failing)} ({len(failing)/total_companies*100:.1f}%)")

if len(failing) > 0:
    print(f"\n{'❌ COMPANIES NOT MEETING MINIMUM:':^90}")
    print("="*90)
    for _, row in failing.iterrows():
        shortage = row['min_offers'] - row['hired']
        print(f"  • {row['company_id']:<45} Need: {row['min_offers']:>2}, Got: {row['hired']:>2}, Short: {shortage:>2}")

# Check companies with 0 hires
zero_hires = merged[merged['hired'] == 0]
if len(zero_hires) > 0:
    print(f"\n{'⚠️  COMPANIES WITH ZERO HIRES:':^90}")
    print("="*90)
    for _, row in zero_hires.iterrows():
        print(f"  • {row['company_id']:<45} Min Required: {row['min_offers']:>2}")

print("\n" + "="*90)
