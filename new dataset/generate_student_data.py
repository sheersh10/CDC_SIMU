import pandas as pd
import numpy as np
from scipy.stats import truncnorm
import random

# Set random seed for reproducibility (you can change this)
np.random.seed(42)
random.seed(42)

# Load data
print("Loading data...")
students_df = pd.read_csv('analysis_data.csv')
domain_df = pd.read_csv('domain.csv')

# Extract department from roll number
students_df['dept'] = students_df['roll_no'].str[2:4]

print(f"Total students: {len(students_df)}")
print(f"\nDepartment distribution:")
print(students_df['dept'].value_counts().sort_index())

# Define department categories
core_eligible_depts = ['ME', 'MF', 'EE', 'IE', 'EC', 'CH', 'IM', 'EX', 'GG', 'MI', 'MT', 'AE', 'CE']
non_core_depts = ['CS', 'MA', 'CY', 'PH', 'AE', 'NA', 'AG', 'BT', 'HS']
quant_preferred_depts = ['CS', 'MA', 'EC', 'EE', 'IM', 'ME']

# Parse domain data
domain_skills = {}
for _, row in domain_df.iterrows():
    domain = row['domain']
    skills = row['skills_for_domain']
    domain_skills[domain] = skills

print(f"\nAvailable domains: {list(domain_skills.keys())}")

# =============================================================================
# STEP 1: Generate CGPA using truncated normal distribution
# =============================================================================
print("\n" + "="*80)
print("STEP 1: Generating CGPA")
print("="*80)

total_students = len(students_df)
mean_cgpa = 8.1
lower_bound = 6.0
upper_bound = 10.0

# Target: ~35-40 students with CGPA > 9.5 (let's aim for 37)
# For truncated normal, we need to find std that gives us this
# Using approximation: with mean=8.1, to get ~37/1225 (~3%) above 9.5
# We need P(X > 9.5) ≈ 0.03
# For standard normal: P(Z > z) = 0.03 => z ≈ 1.88
# So (9.5 - 8.1) / std ≈ 1.88
# std ≈ 1.4 / 1.88 ≈ 0.745

std_cgpa = 0.75

# Create truncated normal distribution
a = (lower_bound - mean_cgpa) / std_cgpa
b = (upper_bound - mean_cgpa) / std_cgpa
cgpa_dist = truncnorm(a, b, loc=mean_cgpa, scale=std_cgpa)

# Generate base CGPA for all students
base_cgpas = cgpa_dist.rvs(total_students)

# Initialize CGPA array
cgpas = np.zeros(total_students)

# Get indices by department
cs_indices = students_df[students_df['dept'] == 'CS'].index.tolist()
ma_indices = students_df[students_df['dept'] == 'MA'].index.tolist()
other_indices = students_df[~students_df['dept'].isin(['CS', 'MA'])].index.tolist()

print(f"CS students: {len(cs_indices)}")
print(f"MA students: {len(ma_indices)}")
print(f"Other students: {len(other_indices)}")

# Sort base CGPAs to allocate high CGPAs strategically
sorted_cgpas = np.sort(base_cgpas)[::-1]  # Sort in descending order

# Allocate top CGPAs to CS students (40 students with 9+, 16 with 9.5+)
cs_high_cgpa_indices = random.sample(cs_indices, min(40, len(cs_indices)))
# 16 with 9.5+
for i, idx in enumerate(cs_high_cgpa_indices[:16]):
    cgpas[idx] = np.random.uniform(9.5, 10.0)
# Remaining 24 with 9.0-9.5
for idx in cs_high_cgpa_indices[16:40]:
    cgpas[idx] = np.random.uniform(9.0, 9.5)

# Allocate to MA students (18 students with 9+, 6 with 9.5+)
ma_high_cgpa_indices = random.sample(ma_indices, min(18, len(ma_indices)))
# 6 with 9.5+
for idx in ma_high_cgpa_indices[:6]:
    cgpas[idx] = np.random.uniform(9.5, 10.0)
# Remaining 12 with 9.0-9.5
for idx in ma_high_cgpa_indices[6:18]:
    cgpas[idx] = np.random.uniform(9.0, 9.5)

# Calculate remaining high CGPA slots
# Target: ~37 total with 9.5+, we've assigned 16+6=22, need ~15 more
remaining_95plus_needed = 15
# Target: ensure we have enough 9+ students for quant (need ~98 total with 9+)
# We have 40+18=58 from CS and MA, need ~40 more from others

# Allocate remaining high CGPAs to other departments
high_cgpa_other = random.sample(other_indices, min(50, len(other_indices)))
for idx in high_cgpa_other[:remaining_95plus_needed]:
    cgpas[idx] = np.random.uniform(9.5, 10.0)
for idx in high_cgpa_other[remaining_95plus_needed:40]:
    cgpas[idx] = np.random.uniform(9.0, 9.5)

# Fill remaining students with base distribution
unassigned_indices = [i for i in range(total_students) if cgpas[i] == 0]
remaining_cgpas = [c for c in base_cgpas if c < 9.0]
random.shuffle(remaining_cgpas)

for i, idx in enumerate(unassigned_indices):
    if i < len(remaining_cgpas):
        cgpas[idx] = remaining_cgpas[i]
    else:
        # Generate new CGPA if needed
        cgpas[idx] = cgpa_dist.rvs(1)[0]
        while cgpas[idx] >= 9.0:  # Ensure it's below 9
            cgpas[idx] = cgpa_dist.rvs(1)[0]

# Round to 2 decimal places
cgpas = np.round(cgpas, 2)

# Assign to dataframe
students_df['cgpa'] = cgpas

# Verify distribution
print(f"\nCGPA Statistics:")
print(f"Mean: {cgpas.mean():.2f}")
print(f"Std: {cgpas.std():.2f}")
print(f"Min: {cgpas.min():.2f}")
print(f"Max: {cgpas.max():.2f}")
print(f"\nStudents with CGPA > 9.5: {(cgpas > 9.5).sum()}")
print(f"Students with CGPA > 9.0: {(cgpas > 9.0).sum()}")
print(f"Students with CGPA < 8.0: {(cgpas < 8.0).sum()}")
print(f"\nCS students with CGPA > 9.0: {students_df[students_df['dept'] == 'CS']['cgpa'].gt(9.0).sum()}")
print(f"CS students with CGPA > 9.5: {students_df[students_df['dept'] == 'CS']['cgpa'].gt(9.5).sum()}")
print(f"MA students with CGPA > 9.0: {students_df[students_df['dept'] == 'MA']['cgpa'].gt(9.0).sum()}")
print(f"MA students with CGPA > 9.5: {students_df[students_df['dept'] == 'MA']['cgpa'].gt(9.5).sum()}")

# =============================================================================
# STEP 2: Assign Domains and Skills
# =============================================================================
print("\n" + "="*80)
print("STEP 2: Assigning Domains and Skills")
print("="*80)

# Initialize columns
students_df['domain_1'] = ''
students_df['skills_for_domain_1'] = ''
students_df['domain_2'] = ''
students_df['skills_for_domain_2'] = ''

# Track assignments
domain_stats = {'SDE': 0, 'Quant': 0, 'Data': 0, 'Finance': 0, 'CONSULTING': 0, 'Core': 0}
students_with_one_domain = 0

# Get students with 9+ CGPA (eligible for Quant)
high_cgpa_students = students_df[students_df['cgpa'] >= 9.0].index.tolist()
print(f"\nTotal students with CGPA >= 9.0: {len(high_cgpa_students)}")

# Get students with 9+ CGPA (eligible for Quant)
high_cgpa_students = students_df[students_df['cgpa'] >= 9.0].index.tolist()
print(f"\nTotal students with CGPA >= 9.0: {len(high_cgpa_students)}")

# For quant, we need ~98 students, so ensure we have enough high CGPA students
# If not enough from preferred depts, we'll also consider other students with 9+ CGPA
target_quant = int(0.08 * total_students)
print(f"Target quant students: {target_quant}")

# Prioritize quant candidates from preferred departments
quant_preferred_candidates = []
for idx in high_cgpa_students:
    dept = students_df.loc[idx, 'dept']
    if dept in quant_preferred_depts:
        quant_preferred_candidates.append(idx)

# Add other high CGPA students if needed
quant_other_candidates = []
for idx in high_cgpa_students:
    dept = students_df.loc[idx, 'dept']
    if dept not in quant_preferred_depts and idx not in quant_preferred_candidates:
        quant_other_candidates.append(idx)

print(f"Quant candidates from preferred depts (CS,MA,EC,EE,IM,ME): {len(quant_preferred_candidates)}")
print(f"Quant candidates from other depts: {len(quant_other_candidates)}")

# Select quant students
# Try to get as many as possible from preferred depts, fill rest from others
quant_students = []

# Distribute among preferred departments
cs_quant_candidates = [idx for idx in quant_preferred_candidates if students_df.loc[idx, 'dept'] == 'CS']
ma_quant_candidates = [idx for idx in quant_preferred_candidates if students_df.loc[idx, 'dept'] == 'MA']
other_pref_quant_candidates = [idx for idx in quant_preferred_candidates if students_df.loc[idx, 'dept'] in ['EC', 'EE', 'IM', 'ME']]

# Calculate target distribution
cs_quant_count = min(int(target_quant * 0.35), len(cs_quant_candidates))
ma_quant_count = min(int(target_quant * 0.25), len(ma_quant_candidates))
other_quant_count = min(target_quant - cs_quant_count - ma_quant_count, len(other_pref_quant_candidates))

quant_students.extend(random.sample(cs_quant_candidates, cs_quant_count))
quant_students.extend(random.sample(ma_quant_candidates, ma_quant_count))
quant_students.extend(random.sample(other_pref_quant_candidates, other_quant_count))

# If still short, add from other departments
if len(quant_students) < target_quant and len(quant_other_candidates) > 0:
    remaining_needed = target_quant - len(quant_students)
    quant_students.extend(random.sample(quant_other_candidates, min(remaining_needed, len(quant_other_candidates))))

print(f"Actual quant students selected: {len(quant_students)}")

# Assign Quant as domain_1, SDE as domain_2 for quant students
for idx in quant_students:
    students_df.loc[idx, 'domain_1'] = 'Quant'
    students_df.loc[idx, 'skills_for_domain_1'] = domain_skills['Quant']
    students_df.loc[idx, 'domain_2'] = 'SDE'
    students_df.loc[idx, 'skills_for_domain_2'] = domain_skills['SDE']
    domain_stats['Quant'] += 1
    domain_stats['SDE'] += 1

# Remaining students
remaining_students = [idx for idx in students_df.index if idx not in quant_students]
print(f"Remaining students to assign: {len(remaining_students)}")

# Select ~100 students for Finance domain (70% from HS)
target_finance = 100
hs_students = students_df[students_df['dept'] == 'HS'].index.tolist()
hs_finance_count = int(target_finance * 0.7)
non_hs_finance_count = target_finance - hs_finance_count

hs_finance_candidates = [idx for idx in hs_students if idx in remaining_students]
non_hs_finance_candidates = [idx for idx in remaining_students if idx not in hs_students]

finance_students = []
finance_students.extend(random.sample(hs_finance_candidates, min(hs_finance_count, len(hs_finance_candidates))))
finance_students.extend(random.sample(non_hs_finance_candidates, min(non_hs_finance_count, len(non_hs_finance_candidates))))

print(f"Finance students: {len(finance_students)}")

# Assign Finance domain randomly as domain_1 or domain_2
for idx in finance_students:
    if random.random() < 0.5:  # 50% chance domain_1
        students_df.loc[idx, 'domain_1'] = 'Finance'
        students_df.loc[idx, 'skills_for_domain_1'] = domain_skills['Finance']
        # Assign domain_2 (SDE or Data or Core based on dept)
        dept = students_df.loc[idx, 'dept']
        if dept in core_eligible_depts:
            students_df.loc[idx, 'domain_2'] = f'Core_{dept}'
            students_df.loc[idx, 'skills_for_domain_2'] = domain_skills.get(f'Core_{dept}', domain_skills.get('CORE_' + dept, ''))
            domain_stats['Core'] += 1
        else:
            choice = random.choice(['SDE', 'Data'])
            students_df.loc[idx, 'domain_2'] = choice
            students_df.loc[idx, 'skills_for_domain_2'] = domain_skills[choice]
            domain_stats[choice] += 1
    else:  # domain_2
        # Assign domain_1 first (SDE or Data)
        choice = random.choice(['SDE', 'Data'])
        students_df.loc[idx, 'domain_1'] = choice
        students_df.loc[idx, 'skills_for_domain_1'] = domain_skills[choice]
        students_df.loc[idx, 'domain_2'] = 'Finance'
        students_df.loc[idx, 'skills_for_domain_2'] = domain_skills['Finance']
        domain_stats[choice] += 1
    
    domain_stats['Finance'] += 1

# Select ~125 students for Consulting domain
target_consulting = 125
consulting_candidates = [idx for idx in remaining_students if idx not in finance_students]
consulting_students = random.sample(consulting_candidates, min(target_consulting, len(consulting_candidates)))

print(f"Consulting students: {len(consulting_students)}")

# Assign Consulting domain randomly
for idx in consulting_students:
    if random.random() < 0.5:  # domain_1
        students_df.loc[idx, 'domain_1'] = 'CONSULTING'
        students_df.loc[idx, 'skills_for_domain_1'] = domain_skills['CONSULTING']
        # Assign domain_2
        dept = students_df.loc[idx, 'dept']
        if dept in core_eligible_depts:
            students_df.loc[idx, 'domain_2'] = f'Core_{dept}'
            students_df.loc[idx, 'skills_for_domain_2'] = domain_skills.get(f'Core_{dept}', domain_skills.get('CORE_' + dept, ''))
            domain_stats['Core'] += 1
        else:
            choice = random.choice(['SDE', 'Data'])
            students_df.loc[idx, 'domain_2'] = choice
            students_df.loc[idx, 'skills_for_domain_2'] = domain_skills[choice]
            domain_stats[choice] += 1
    else:  # domain_2
        choice = random.choice(['SDE', 'Data'])
        students_df.loc[idx, 'domain_1'] = choice
        students_df.loc[idx, 'skills_for_domain_1'] = domain_skills[choice]
        students_df.loc[idx, 'domain_2'] = 'CONSULTING'
        students_df.loc[idx, 'skills_for_domain_2'] = domain_skills['CONSULTING']
        domain_stats[choice] += 1
    
    domain_stats['CONSULTING'] += 1

# Process remaining students
assigned_students = set(quant_students + finance_students + consulting_students)
truly_remaining = [idx for idx in remaining_students if idx not in assigned_students]

print(f"Truly remaining students: {len(truly_remaining)}")

# Target: 70% should have SDE as one of their domains
# We already assigned some SDE, need to reach ~857 (70% of 1225)
target_sde_total = int(0.70 * total_students)
current_sde = domain_stats['SDE']
additional_sde_needed = target_sde_total - current_sde

print(f"Target SDE students: {target_sde_total}")
print(f"Current SDE students: {current_sde}")
print(f"Additional SDE needed: {additional_sde_needed}")

# Target: 200-300 students with only 1 domain
target_single_domain = 250

# Assign remaining students
for idx in truly_remaining:
    dept = students_df.loc[idx, 'dept']
    cgpa = students_df.loc[idx, 'cgpa']
    
    # Decide if single domain or dual domain
    if students_with_one_domain < target_single_domain and random.random() < 0.3:
        # Single domain student
        # Prioritize SDE if needed
        if domain_stats['SDE'] < target_sde_total:
            students_df.loc[idx, 'domain_1'] = 'SDE'
            students_df.loc[idx, 'skills_for_domain_1'] = domain_skills['SDE']
            domain_stats['SDE'] += 1
        elif dept in core_eligible_depts:
            students_df.loc[idx, 'domain_1'] = f'Core_{dept}'
            students_df.loc[idx, 'skills_for_domain_1'] = domain_skills.get(f'Core_{dept}', domain_skills.get('CORE_' + dept, ''))
            domain_stats['Core'] += 1
        else:
            choice = random.choice(['SDE', 'Data'])
            students_df.loc[idx, 'domain_1'] = choice
            students_df.loc[idx, 'skills_for_domain_1'] = domain_skills[choice]
            domain_stats[choice] += 1
        
        students_with_one_domain += 1
    
    else:
        # Dual domain student
        # Check if student should have core based on department
        should_have_core = (dept in core_eligible_depts) and (dept not in non_core_depts)
        
        if should_have_core and random.random() < 0.6:  # 60% of core-eligible get core
            # Assign SDE or Data as domain_1, Core as domain_2
            if domain_stats['SDE'] < target_sde_total:
                students_df.loc[idx, 'domain_1'] = 'SDE'
                students_df.loc[idx, 'skills_for_domain_1'] = domain_skills['SDE']
                domain_stats['SDE'] += 1
            else:
                students_df.loc[idx, 'domain_1'] = 'Data'
                students_df.loc[idx, 'skills_for_domain_1'] = domain_skills['Data']
                domain_stats['Data'] += 1
            
            students_df.loc[idx, 'domain_2'] = f'Core_{dept}'
            students_df.loc[idx, 'skills_for_domain_2'] = domain_skills.get(f'Core_{dept}', domain_skills.get('CORE_' + dept, ''))
            domain_stats['Core'] += 1
        
        else:
            # Assign SDE as domain_1, Data/other as domain_2
            if domain_stats['SDE'] < target_sde_total:
                students_df.loc[idx, 'domain_1'] = 'SDE'
                students_df.loc[idx, 'skills_for_domain_1'] = domain_skills['SDE']
                domain_stats['SDE'] += 1
                
                # Domain 2: Data or Core (if eligible)
                if dept in core_eligible_depts and random.random() < 0.3:
                    students_df.loc[idx, 'domain_2'] = f'Core_{dept}'
                    students_df.loc[idx, 'skills_for_domain_2'] = domain_skills.get(f'Core_{dept}', domain_skills.get('CORE_' + dept, ''))
                    domain_stats['Core'] += 1
                else:
                    students_df.loc[idx, 'domain_2'] = 'Data'
                    students_df.loc[idx, 'skills_for_domain_2'] = domain_skills['Data']
                    domain_stats['Data'] += 1
            else:
                # Use Data as domain_1
                students_df.loc[idx, 'domain_1'] = 'Data'
                students_df.loc[idx, 'skills_for_domain_1'] = domain_skills['Data']
                domain_stats['Data'] += 1
                
                if dept in core_eligible_depts:
                    students_df.loc[idx, 'domain_2'] = f'Core_{dept}'
                    students_df.loc[idx, 'skills_for_domain_2'] = domain_skills.get(f'Core_{dept}', domain_skills.get('CORE_' + dept, ''))
                    domain_stats['Core'] += 1
                else:
                    students_df.loc[idx, 'domain_2'] = 'SDE'
                    students_df.loc[idx, 'skills_for_domain_2'] = domain_skills['SDE']
                    domain_stats['SDE'] += 1

# =============================================================================
# STEP 3: Final Statistics and Save
# =============================================================================
print("\n" + "="*80)
print("FINAL STATISTICS")
print("="*80)

print(f"\nDomain Statistics:")
for domain, count in domain_stats.items():
    print(f"{domain}: {count} ({count/total_students*100:.1f}%)")

print(f"\nStudents with only 1 domain: {students_with_one_domain}")
print(f"Students with 2 domains: {total_students - students_with_one_domain}")

# Count domain_1 distribution
print("\nDomain_1 distribution:")
print(students_df['domain_1'].value_counts())

# Count domain_2 distribution (non-empty)
print("\nDomain_2 distribution:")
print(students_df[students_df['domain_2'] != '']['domain_2'].value_counts())

# Save to CSV
output_file = 'analysis_data_updated.csv'
students_df.drop('dept', axis=1, inplace=True)  # Remove helper column
students_df.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print(f"Data saved to: {output_file}")
print(f"{'='*80}")

print("\nFirst 10 rows:")
print(students_df.head(10))
