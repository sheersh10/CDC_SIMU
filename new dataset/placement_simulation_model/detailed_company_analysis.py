import pandas as pd
import os
from pathlib import Path

# Load data
base_dir = Path(__file__).parent.parent
results_df = pd.read_csv(Path(__file__).parent / 'day1_placement_results.csv')
companies_df = pd.read_csv(base_dir / 'companies.csv')

# Get placed students
placed = results_df[results_df['status'] == 'Placed']
company_hires = placed.groupby('placed_company').size().reset_index(name='actual_hires')

# Create company ID mapping
companies_df['company_id'] = companies_df['company_name'] + '_' + companies_df['job_role']

# Merge with company data
detailed_stats = pd.merge(
    company_hires,
    companies_df[['company_id', 'min_offers', 'max_offers', 'arrival_day']],
    left_on='placed_company',
    right_on='company_id',
    how='left'
)

# Calculate utilization
detailed_stats['utilization_%'] = (detailed_stats['actual_hires'] / detailed_stats['max_offers'] * 100).round(1)
detailed_stats['unused_capacity'] = detailed_stats['max_offers'] - detailed_stats['actual_hires']

# Sort by actual hires
detailed_stats = detailed_stats.sort_values('actual_hires', ascending=False)

print("="*100)
print("DETAILED COMPANY HIRING ANALYSIS")
print("="*100)
print(f"\nTotal Companies That Hired: {len(detailed_stats)}")
print(f"Total Students Placed: {len(placed)}")
print(f"Total Max Capacity: {detailed_stats['max_offers'].sum():.0f}")
print(f"Overall Utilization: {(len(placed) / detailed_stats['max_offers'].sum() * 100):.1f}%\n")

print(f"{'Rank':<5} {'Company':<45} {'Hired':<7} {'Max':<7} {'Util%':<8} {'Unused':<8}")
print("-"*100)

for idx, (_, row) in enumerate(detailed_stats.iterrows(), 1):
    company = row['placed_company']
    hired = row['actual_hires']
    max_cap = row['max_offers']
    util = row['utilization_%']
    unused = row['unused_capacity']
    
    print(f"{idx:<5} {company:<45} {hired:<7} {max_cap:<7.0f} {util:<8.1f} {unused:<8.0f}")

print("="*100)

# Summary by categories
print(f"\n{'CAPACITY UTILIZATION BREAKDOWN':^100}")
print("="*100)

high_util = detailed_stats[detailed_stats['utilization_%'] >= 70]
med_util = detailed_stats[(detailed_stats['utilization_%'] >= 40) & (detailed_stats['utilization_%'] < 70)]
low_util = detailed_stats[detailed_stats['utilization_%'] < 40]

print(f"\nHigh Utilization (≥70%): {len(high_util)} companies")
if len(high_util) > 0:
    for _, row in high_util.iterrows():
        print(f"  • {row['placed_company']:<50} {row['actual_hires']}/{row['max_offers']:.0f} ({row['utilization_%']:.1f}%)")

print(f"\nMedium Utilization (40-70%): {len(med_util)} companies")
if len(med_util) > 0:
    for _, row in med_util.iterrows():
        print(f"  • {row['placed_company']:<50} {row['actual_hires']}/{row['max_offers']:.0f} ({row['utilization_%']:.1f}%)")

print(f"\nLow Utilization (<40%): {len(low_util)} companies")
if len(low_util) > 0:
    for _, row in low_util.iterrows():
        print(f"  • {row['placed_company']:<50} {row['actual_hires']}/{row['max_offers']:.0f} ({row['utilization_%']:.1f}%)")

print(f"\n{'UNUSED CAPACITY ANALYSIS':^100}")
print("="*100)
total_unused = detailed_stats['unused_capacity'].sum()
print(f"\nTotal Unused Capacity: {total_unused:.0f} positions")
print(f"If all companies hired at MAX capacity: {detailed_stats['max_offers'].sum():.0f} placements")
print(f"Current placements: {len(placed)}")
print(f"Lost opportunities: {total_unused:.0f} positions ({total_unused/detailed_stats['max_offers'].sum()*100:.1f}%)")

print(f"\n{'TOP WASTED CAPACITY':^100}")
print("="*100)
top_wasted = detailed_stats.nlargest(10, 'unused_capacity')
for idx, (_, row) in enumerate(top_wasted.iterrows(), 1):
    print(f"{idx:2}. {row['placed_company']:<50} Lost {row['unused_capacity']:.0f} positions")

print("\n" + "="*100)
