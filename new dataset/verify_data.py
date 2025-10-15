import pandas as pd

df = pd.read_csv('analysis_data_updated.csv')
df['dept'] = df['roll_no'].str[2:4]

print("="*80)
print("VERIFICATION REPORT")
print("="*80)

print(f"\nTotal students: {len(df)}")
print(f"Students with only 1 domain: {df['domain_2'].isna().sum()}")
print(f"Students with 2 domains: {df['domain_2'].notna().sum()}")

print("\n" + "="*80)
print("CGPA VERIFICATION")
print("="*80)
print(f"Mean CGPA: {df['cgpa'].mean():.2f}")
print(f"Students with CGPA > 9.5: {(df['cgpa'] > 9.5).sum()}")
print(f"Students with CGPA > 9.0: {(df['cgpa'] > 9.0).sum()}")
print(f"Students with CGPA < 8.0: {(df['cgpa'] < 8.0).sum()}")

print(f"\nCS students with CGPA > 9.0: {df[(df['dept']=='CS') & (df['cgpa']>9.0)].shape[0]}")
print(f"CS students with CGPA > 9.5: {df[(df['dept']=='CS') & (df['cgpa']>9.5)].shape[0]}")
print(f"MA students with CGPA > 9.0: {df[(df['dept']=='MA') & (df['cgpa']>9.0)].shape[0]}")
print(f"MA students with CGPA > 9.5: {df[(df['dept']=='MA') & (df['cgpa']>9.5)].shape[0]}")

print("\n" + "="*80)
print("QUANT DOMAIN VERIFICATION")
print("="*80)
quant_students = df[df['domain_1'] == 'Quant']
print(f"Total quant students: {len(quant_students)}")
print(f"Quant students by department:")
print(quant_students['dept'].value_counts().sort_index())
print(f"\nMin CGPA for quant students: {quant_students['cgpa'].min():.2f}")
print(f"All quant students have CGPA >= 9.0: {(quant_students['cgpa'] >= 9.0).all()}")

print("\n" + "="*80)
print("CORE DOMAIN VERIFICATION")
print("="*80)
non_core_depts = ['CS', 'MA', 'CY', 'PH', 'NA', 'AG', 'BT', 'HS']
print("Checking if non-core departments have core domain...")
for dept in non_core_depts:
    core_count = df[(df['dept']==dept) & (
        (df['domain_1'].str.contains('Core', na=False)) | 
        (df['domain_2'].str.contains('Core', na=False))
    )].shape[0]
    if core_count > 0:
        print(f"  {dept}: {core_count} students with core (SHOULD BE 0!)")
    else:
        print(f"  {dept}: 0 students with core ✓")

print("\n" + "="*80)
print("SDE DOMAIN VERIFICATION")
print("="*80)
sde_students = df[(df['domain_1'] == 'SDE') | (df['domain_2'] == 'SDE')]
print(f"Students with SDE as domain_1 or domain_2: {len(sde_students)} ({len(sde_students)/len(df)*100:.1f}%)")

print("\n" + "="*80)
print("FINANCE DOMAIN VERIFICATION")
print("="*80)
finance_students = df[(df['domain_1'] == 'Finance') | (df['domain_2'] == 'Finance')]
print(f"Total finance students: {len(finance_students)}")
print(f"Finance students from HS dept: {finance_students[finance_students['dept']=='HS'].shape[0]} ({finance_students[finance_students['dept']=='HS'].shape[0]/len(finance_students)*100:.1f}%)")

print("\n" + "="*80)
print("CONSULTING DOMAIN VERIFICATION")
print("="*80)
consulting_students = df[(df['domain_1'] == 'CONSULTING') | (df['domain_2'] == 'CONSULTING')]
print(f"Total consulting students: {len(consulting_students)}")

print("\n" + "="*80)
print("DOMAIN DISTRIBUTION")
print("="*80)
print("\nDomain_1 counts:")
print(df['domain_1'].value_counts())
print("\nDomain_2 counts (excluding NaN):")
print(df['domain_2'].value_counts())

print("\n" + "="*80)
print("SAMPLE DATA")
print("="*80)
print("\nHigh CGPA students (CGPA > 9.5):")
print(df[df['cgpa'] > 9.5][['roll_no', 'name', 'cgpa', 'domain_1', 'domain_2']].head(10))

print("\nQuant students:")
print(df[df['domain_1'] == 'Quant'][['roll_no', 'name', 'cgpa', 'domain_1', 'domain_2']].head(10))

print("\nSingle domain students:")
print(df[df['domain_2'].isna()][['roll_no', 'name', 'cgpa', 'domain_1', 'domain_2']].head(10))
