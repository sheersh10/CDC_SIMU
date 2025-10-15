import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('analysis_data.csv')
df['dept'] = df['roll_no'].str[2:4]

print("Generating department-wise profile statistics...")

# Get all unique domains
all_domains = set()
for domain in df['domain_1'].dropna():
    all_domains.add(domain)
for domain in df['domain_2'].dropna():
    all_domains.add(domain)

all_domains = sorted(list(all_domains))
print(f"\nFound {len(all_domains)} unique domains: {all_domains}")

# Get all departments
departments = sorted(df['dept'].unique())
print(f"\nFound {len(departments)} departments: {departments}")

# Create a dictionary to store counts
dept_profile_counts = {}

for dept in departments:
    dept_df = df[df['dept'] == dept]
    dept_profile_counts[dept] = {'Total_Students': len(dept_df)}
    
    for domain in all_domains:
        # Count students who have this domain as either domain_1 or domain_2
        count_domain_1 = (dept_df['domain_1'] == domain).sum()
        count_domain_2 = (dept_df['domain_2'] == domain).sum()
        total_count = count_domain_1 + count_domain_2
        
        dept_profile_counts[dept][domain] = total_count

# Convert to DataFrame
stats_df = pd.DataFrame(dept_profile_counts).T

# Reorder columns to have Total_Students first
cols = ['Total_Students'] + [col for col in stats_df.columns if col != 'Total_Students']
stats_df = stats_df[cols]

# Sort by department
stats_df = stats_df.sort_index()

# Save to CSV
output_file = 'department_profile_statistics.csv'
stats_df.to_csv(output_file, index=True)

print(f"\n{'='*80}")
print(f"Department-wise profile statistics saved to: {output_file}")
print(f"{'='*80}")

print("\nPreview of the data:")
print(stats_df)

# Also create a summary showing top profiles per department
print("\n" + "="*80)
print("TOP 3 PROFILES PER DEPARTMENT")
print("="*80)

for dept in departments:
    dept_data = stats_df.loc[dept]
    # Exclude Total_Students and get top 3
    profile_counts = dept_data.drop('Total_Students').sort_values(ascending=False)
    top_3 = profile_counts.head(3)
    
    print(f"\n{dept} (Total: {dept_data['Total_Students']} students)")
    for profile, count in top_3.items():
        if count > 0:
            percentage = (count / dept_data['Total_Students']) * 100
            print(f"  {profile}: {int(count)} ({percentage:.1f}%)")

# Create a cleaner version with only non-zero counts
print("\n" + "="*80)
print("Creating simplified version with only active profiles...")
print("="*80)

# Create a long format table
rows = []
for dept in departments:
    dept_df = df[df['dept'] == dept]
    total = len(dept_df)
    
    for domain in all_domains:
        count_domain_1 = (dept_df['domain_1'] == domain).sum()
        count_domain_2 = (dept_df['domain_2'] == domain).sum()
        total_count = count_domain_1 + count_domain_2
        
        if total_count > 0:
            rows.append({
                'Department': dept,
                'Profile': domain,
                'Count': int(total_count),
                'Percentage': round((total_count / total) * 100, 1),
                'As_Domain_1': int(count_domain_1),
                'As_Domain_2': int(count_domain_2)
            })

simplified_df = pd.DataFrame(rows)
simplified_file = 'department_profile_detailed.csv'
simplified_df.to_csv(simplified_file, index=False)

print(f"Detailed profile breakdown saved to: {simplified_file}")
print(f"\nSample data:")
print(simplified_df.head(20))

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)
print(f"\nTotal departments: {len(departments)}")
print(f"Total unique profiles: {len(all_domains)}")
print(f"Total student-profile mappings: {len(rows)}")

# Profile popularity across all departments
print("\n" + "="*80)
print("OVERALL PROFILE POPULARITY")
print("="*80)
profile_totals = simplified_df.groupby('Profile')['Count'].sum().sort_values(ascending=False)
for profile, count in profile_totals.items():
    print(f"{profile}: {int(count)} students")
