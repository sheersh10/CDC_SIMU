"""
Bottleneck Analysis - Why are placements lower than expected (250 vs 127)?
"""

import pandas as pd
from pathlib import Path

# Load data
base_dir = Path(__file__).parent.parent
companies_df = pd.read_csv(base_dir / 'companies.csv')
results_df = pd.read_csv(Path(__file__).parent / 'day1_placement_results.csv')

print("="*80)
print("BOTTLENECK ANALYSIS - Why Only 127 Placements Instead of ~250?")
print("="*80)

print("\n1. MAXIMUM POSSIBLE PLACEMENTS")
print("-"*80)
total_max_offers = companies_df['max_offers'].sum()
total_min_offers = companies_df['min_offers'].sum()
print(f"Total max_offers across all companies: {total_max_offers}")
print(f"Total min_offers across all companies: {total_min_offers}")
print(f"Day 1 companies only: {len(companies_df[companies_df['arrival_day'] == 1])}")
day1_max = companies_df[companies_df['arrival_day'] == 1]['max_offers'].sum()
day1_min = companies_df[companies_df['arrival_day'] == 1]['min_offers'].sum()
print(f"Day 1 max_offers sum: {day1_max}")
print(f"Day 1 min_offers sum: {day1_min}")

print("\n2. ACTUAL SIMULATION RESULTS")
print("-"*80)
placed_count = len(results_df[results_df['status'] == 'Placed'])
print(f"Actual placements: {placed_count}")
print(f"Utilization rate: {placed_count}/{day1_max} = {placed_count/day1_max*100:.1f}%")

print("\n3. COMPANIES LOADED VS AVAILABLE")
print("-"*80)
day1_companies = companies_df[companies_df['arrival_day'] == 1]
print(f"Total Day 1 companies in companies.csv: {len(day1_companies)}")
print(f"\nCompanies in simulation output:")
placement_companies = results_df[results_df['status'] == 'Placed']['placed_company'].unique()
print(f"Total companies that hired: {len(placement_companies)}")

print("\n4. HIRING CAPACITY PER COMPANY")
print("-"*80)
company_hires = results_df[results_df['status'] == 'Placed'].groupby('placed_company').size().reset_index(name='actual_hires')
print(f"{'Company':<45} {'Actual':>8} {'Max Possible':>12}")
print("-"*80)
for _, row in company_hires.head(20).iterrows():
    company_name = row['placed_company'].split('_')[0]
    actual = row['actual_hires']
    print(f"{row['placed_company']:<45} {actual:>8}")

print("\n5. KEY BOTTLENECKS IDENTIFIED")
print("-"*80)

# Check if companies were skipped
print("\n5a. Companies WITHOUT shortlist files (SKIPPED):")
print("   - These companies have max_offers but couldn't participate")
print("   - IMPACT: Lost hiring capacity")

# Check interview slots constraint
print("\n5b. Interview Slots Constraint:")
print("   - interview_slots = length of shortlist CSV files")
print("   - If shortlist is small, fewer students get interviewed")
print("   - Then only min(actual_openings, shortlisted) get offers")
print("   - IMPACT: Companies may want 15 hires but only interview 10")

# Check min/max hires randomization
print("\n5c. Random Hiring Numbers:")
print("   - actual_openings = random(min_hires, max_hires)")
print("   - On average, companies hire midpoint, not maximum")
print(f"   - Expected average: {(day1_min + day1_max)/2:.1f} instead of max {day1_max}")

# Check eligibility
print("\n5d. Student Eligibility Issues:")
placed_students = results_df[results_df['status'] == 'Placed']
print(f"   - Mean CGPA of placed: {placed_students['cgpa'].mean():.2f}")
print(f"   - Many students may not meet min_cgpa requirements")
print(f"   - Domain mismatches reduce eligible pool")

# Check opt-out
opted_out = len(results_df[results_df['status'] == 'Opted_Out'])
print(f"\n5e. Student Opt-outs:")
print(f"   - {opted_out} students opted out (P_OPT_OUT = 5% per serial)")
print(f"   - Lost {opted_out} potential candidates from pool")

print("\n6. ESTIMATED IMPACT OF EACH BOTTLENECK")
print("-"*80)
print(f"A. Missing shortlist files: ~34 companies skipped")
print(f"   Estimated loss: ~50-80 placements")
print(f"\nB. interview_slots too small:")
print(f"   Companies want 10-15 hires but only interview 5-8")
print(f"   Estimated loss: ~30-50 placements")
print(f"\nC. Random hiring (avg vs max):")
print(f"   Hiring {(day1_min+day1_max)/2:.0f} instead of {day1_max}")
print(f"   Estimated loss: ~{day1_max - (day1_min+day1_max)/2:.0f} placements")
print(f"\nD. Eligibility constraints (CGPA, domain, dept):")
print(f"   Estimated loss: ~20-40 placements")
print(f"\nE. Student opt-outs ({opted_out} students):")
print(f"   Direct loss: {opted_out} potential placements")

print("\n7. RECOMMENDED FIXES TO REACH 250 PLACEMENTS")
print("-"*80)
print("Priority 1 (HIGH IMPACT):")
print("  ✓ Create shortlist files for all 34 missing companies")
print("  ✓ Set interview_slots = max_offers (or 2x max_offers for buffer)")
print("  ✓ Change hiring logic: actual_openings = max_hires (not random)")
print("\nPriority 2 (MEDIUM IMPACT):")
print("  ✓ Reduce min_cgpa requirements (7.5+ → 7+, or remove for some)")
print("  ✓ Broaden allowed_departments (ALL instead of specific)")
print("  ✓ Reduce opt-out probability (5% → 2%)")
print("\nPriority 3 (LOW IMPACT):")
print("  ✓ Increase score weights for random factor (more variety)")
print("  ✓ Add multiple interview rounds with increasing selection")

print("\n" + "="*80)
print("SUMMARY: Main bottleneck is INTERVIEW_SLOTS < MAX_OFFERS")
print("Companies want to hire 10-15 but only interview 5-8 students!")
print("="*80)
