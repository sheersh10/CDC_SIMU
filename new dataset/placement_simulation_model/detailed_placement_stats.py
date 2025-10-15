import pandas as pd
from pathlib import Path

# Load the placement results from the parent directory
results_path = Path(__file__).parent.parent / 'day1_placement_results.csv'
df = pd.read_csv(results_path)

# Filter only placed students
placed = df[df['status'] == 'Placed']

print('=' * 80)
print('COMPANY-WISE HIRING DATA (All 211 Placed Students)')
print('=' * 80)
print()

# Get company-wise counts sorted alphabetically
company_counts = placed['placed_company'].value_counts().sort_index()

for company, count in company_counts.items():
    print(f'{company:<45} : {count:>3} students')

print()
print('=' * 80)
print(f'Total Companies that Hired        : {len(company_counts)}')
print(f'Total Students Placed             : {len(placed)}')
print('=' * 80)
print()
print()

# Department-wise analysis
print('=' * 80)
print('DEPARTMENT-WISE PLACEMENT DATA (All 211 Placed Students)')
print('=' * 80)
print()

dept_counts = placed['department'].value_counts().sort_index()

for dept, count in dept_counts.items():
    # Get total students in that department
    total_in_dept = len(df[df['department'] == dept])
    percentage = (count / total_in_dept) * 100
    print(f'{dept:<10} : {count:>3} placed out of {total_in_dept:>4} students ({percentage:>5.2f}%)')

print()
print('=' * 80)
print(f'Total Students Placed             : {len(placed)}')
print(f'Total Students in Dataset         : {len(df)}')
print(f'Overall Placement Rate            : {(len(placed)/len(df))*100:.2f}%')
print('=' * 80)
print()
print()

# Department-wise breakdown by company
print('=' * 80)
print('DEPARTMENT-WISE BREAKDOWN FOR EACH COMPANY')
print('=' * 80)
print()

for company in sorted(company_counts.index):
    company_students = placed[placed['placed_company'] == company]
    dept_breakdown = company_students['department'].value_counts().sort_index()
    
    print(f'\n{company} (Total: {len(company_students)} students)')
    print('-' * 60)
    for dept, count in dept_breakdown.items():
        print(f'  {dept:<10} : {count:>2} students')

print()
print('=' * 80)
