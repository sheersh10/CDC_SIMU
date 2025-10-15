"""
Placement Simulation Model
Multi-stage placement process simulation with test shortlisting and interviews
"""

import pandas as pd
import numpy as np
import random
from typing import List, Dict, Set, Tuple
import os
from pathlib import Path

# Set random seed for reproducibility (can be overridden)
RANDOM_SEED = int(os.environ.get('RANDOM_SEED', 42))
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

# Score weights (UPDATED FORMULA)
W1_CGPA_PROFILE = 0.3  # Weight for CGPA in ProfileScore
W2_SKILL_PROFILE = 0.2  # Weight for Skill Match in ProfileScore
W3_RANDOM_PROFILE = 0.2  # Weight for Random factor in ProfileScore
W4_DEP_SCORE_PROFILE = 0.3  # Weight for Department Score in ProfileScore

W5_PROFILE_INTERVIEW = 0.3  # Weight for ProfileScore in InterviewScore
W6_CGPA_INTERVIEW = 0.5  # Weight for CGPA in InterviewScore
W7_RANDOM_INTERVIEW = 0.2  # Weight for Random factor in InterviewScore

P_OPT_OUT = 0.05  # Probability of student opting out

# Load department scores
DEP_SCORES = {}
def load_dep_scores():
    """Load department scores from dep_score.csv"""
    global DEP_SCORES
    dep_score_file = Path(__file__).parent.parent / 'dep_score.csv'
    if dep_score_file.exists():
        df = pd.read_csv(dep_score_file)
        DEP_SCORES = dict(zip(df['department_code'], df['score']))
    else:
        print(f"Warning: dep_score.csv not found at {dep_score_file}")
        DEP_SCORES = {}

# Load department scores at module initialization
load_dep_scores()

# Department mappings
DEPT_MAPPINGS = {
    'CSE': 'CS',
    'MNC': 'MA',
    'MnC': 'MA',
    'ECE': 'EC',
    'E&ECE': ['EE', 'EC'],
    'CIRCUITAL': ['CS', 'MA', 'IM', 'EE', 'EC', 'IE'],
    'Circuital': ['CS', 'MA', 'IM', 'EE', 'EC', 'IE'],
    'Circuitals': ['CS', 'MA', 'IM', 'EE', 'EC', 'IE'],
}

# Company to shortlist file mapping
COMPANY_SHORTLIST_MAPPING = {
    # Adobe
    'Adobe_Software (Product)': 'adobe(product).csv',
    'Adobe_Software (MDSR)': None,  # No shortlist available
    'Adobe_Software (Research Intern)': 'adobe(research).csv',
    
    # Amazon
    'Amazon_SDE': 'amazon(sde).csv',
    
    # American Express (AMEX)
    'American Express_Analyst': 'amex.csv',
    'AMEX_Analyst': 'amex.csv',
    
    # Alphagrep
    'Alphagrep_Software': 'alphagrep(sde).csv',
    
    # Samsung
    'Samsung R&D (Korea)_Software': 'samsung_korea.csv',
    'Samsung_SDE': 'samsung_korea.csv',
    'Samsung R&D Delhi_SDE': 'samsung_korea.csv',
    'Samsung Bengaluru R&D_SDE': 'samsung_bengaluru.csv',
    
    # Microsoft
    'Microsoft_Software Development': 'microsoft.csv',
    
    # Google
    'Google_SWE': 'google(swe).csv',
    'Google_Core': 'google(hardware).csv',
    
    # Goldman Sachs
    'Goldman Sachs_SDE': 'goldman_sachs(sde).csv',
    'GS_SDE': 'goldman_sachs(sde).csv',
    
    # Morgan Stanley
    'Morgan Stanley_Sales and Trading': 'morgan_stanley(sales and trading).csv',
    
    # DE Shaw
    'DE Shaw & Co_Software': 'de_shaw.csv',
    
    # Databricks
    'Databricks_Software': 'databricks.csv',
    
    # Graviton
    'Graviton Research Capital_Software': 'graviton(sde).csv',
    
    # Optiver
    'Optiver_Quant': 'optiver.csv',
    
    # Quadeye
    'Quadeye_Quant': 'quadeye(quant).csv',
    
    # Rubrik
    'Rubrik_SDE': 'rubrik.csv',
    
    # Trexquant
    'Trexquant_Quant': 'trexquant.csv',
    
    # NVIDIA
    'NVIDIA_System Software Engineer': 'nvidia.csv',
    
    # Atlassian
    'Atlassian_SDE': 'atlassian.csv',
    
    # BAIN
    'BAIN_Consulting': 'bcg.csv',  # Assuming similar to BCG
    
    # BCG
    'BCG_Consulting': 'bcg.csv',
    
    # Blackrock
    'Blackrock_Finance': 'blackrock(analytics).csv',
    'Blackrock_Data': 'blackrock(application).csv',
    
    # Glean
    'Glean_SWE': 'glean.csv',
    
    # HUL
    'HUL_Supply Chain': 'hul(supply-chain).csv',
    
    # ITC
    'ITC_KITES Intern': 'itc.csv',
    
    # JPMC
    'JPMC_CCB': 'jpmc(wholesale).csv',
    'JPMC_MRGR': 'jpmc(mrgr).csv',
    'JPMC_QR': 'jpmc(qr).csv',
    
    # Nomura
    'Nomura_Wholesale Strategy': 'nomura(global markets).csv',
    'Nomura_Algo-Quants': 'nomura(global markets).csv',
    
    # P&G
    'Proctor and Gamble_Consultinig': None,
    'P&G_Consultinig': None,
    
    # Salesforce
    'Salesforce_SDE': 'stripe.csv',  # Assuming similar
    
    # Samsara
    'Samsara_SDE': 'samsara.csv',
    
    # Uber
    'UBER_SDE': 'uber.csv',
    
    # Stripe
    'Stripe_Data': 'stripe.csv',
    
    # Natwest
    'Natweest_SDE': 'natwest.csv',
    
    # Neo Wealth
    'Neo Wealth_SDE': 'neo-wealth(sde).csv',
    
    # NK Securities
    'NK Securities_SDE': 'nk_securities(sde).csv',
    
    # Ebulliant
    'Ebulliant Securities_Quant': 'ebulliant.csv',
    
    # LEK
    'LEK_Consulting': 'bcg.csv',  # Assuming similar to BCG
    
    # Millennium
    'Millenium_Quant': 'millenium(quant).csv',
    
    # Rippling
    'Rippling_AI engineer / SDE': 'rippling.csv',
    
    # AWL
    'AWL Inc._AI Engineer': 'awl.csv',
    
    # Wells Fargo
    'Wells Fargo_Quant Analyst': 'wells_fargo(qap).csv',
    'Wells Fargo_Tech': 'wells_fargo(technology).csv',
}

# Domain to job role mapping
DOMAIN_JOB_ROLE_MAPPING = {
    'SDE': ['SDE', 'Software', 'Software Development', 'AI engineer / SDE', 'AI Engineer', 
            'System Software Engineer', 'SWE', 'R&D', 'Core'],
    'Data': ['Data', 'Analyst', 'Data Analyst'],
    'Quant': ['Quant', 'Quant Analyst', 'Algo-Quants', 'Sales and Trading'],
    'Finance': ['Finance', 'Analyst', 'Wholesale Strategy'],
    'CONSULTING': ['Consulting', 'Consultinig', 'Management Trainee', 'Political Consulting'],
    'Core_': ['Core', 'R&D', 'Hardware', 'Signal Processing', 'ANALOG', 'DIGITAL', 
              'Electric Vehicle Software', 'EDA', 'Systems'],  # Handles all Core_XX
}


# ============================================================================
# STUDENT CLASS
# ============================================================================

class Student:
    """Represents a student in the placement process"""
    
    def __init__(self, roll_no: str, name: str, cgpa: float, 
                 department: str, domain_1: str, skills_1: List[str],
                 domain_2: str = None, skills_2: List[str] = None):
        self.roll_no = roll_no
        self.name = name
        self.cgpa = cgpa
        self.department = department
        self.domain_1 = domain_1
        self.domain_2 = domain_2
        
        # Combine all skills
        self.skills = set(skills_1) if skills_1 else set()
        if skills_2:
            self.skills.update(skills_2)
        
        # All domains
        self.domains = [domain_1]
        if domain_2 and pd.notna(domain_2) and domain_2 != '':
            self.domains.append(domain_2)
        
        # Status tracking
        self.status = 'Unplaced'
        self.current_applications = []  # List of companies applied to
        self.placed_company = None
        
    def __repr__(self):
        return f"Student({self.roll_no}, {self.name}, CGPA:{self.cgpa}, Status:{self.status})"


# ============================================================================
# COMPANY CLASS
# ============================================================================

class Company:
    """Represents a company in the placement process"""
    
    def __init__(self, company_name: str, job_role: str, 
                 allowed_departments: List[str], min_cgpa: float,
                 required_skills: List[str], visit_day: int,
                 min_hires: int, max_hires: int, interview_slots: int):
        self.company_name = company_name
        self.job_role = job_role
        self.allowed_departments = allowed_departments
        self.min_cgpa = min_cgpa
        self.required_skills = required_skills
        self.visit_day = visit_day
        self.min_hires = min_hires
        self.max_hires = max_hires
        self.interview_slots = interview_slots
        
        # Application tracking
        self.applicants = []  # Students who applied
        self.test_invited = []  # Students invited for test
        self.shortlisted = []  # Students shortlisted for interview
        self.offered = []  # Students who received offers
        self.hired = []  # Students who accepted offers
        
    def get_unique_id(self):
        """Returns unique identifier for company"""
        return f"{self.company_name}_{self.job_role}"
    
    def __repr__(self):
        return f"Company({self.company_name}, {self.job_role}, Day:{self.visit_day}, Slots:{self.interview_slots})"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def parse_cgpa_requirement(cgpa_str: str) -> float:
    """Parse CGPA requirement from string"""
    if pd.isna(cgpa_str) or cgpa_str in ['NONE', 'NA', 'None', '', 'NA ']:
        return 0.0
    
    cgpa_str = str(cgpa_str).strip()
    
    # Handle conditional CGPA (take the lower value)
    if 'for' in cgpa_str.lower():
        # "7.5+ for Dev, 8.5+ for Advanced Dev" -> extract first number
        import re
        numbers = re.findall(r'\d+\.?\d*', cgpa_str)
        if numbers:
            return float(numbers[0])
    
    # Handle "preferably"
    if 'preferably' in cgpa_str.lower():
        cgpa_str = cgpa_str.replace('preferably', '').strip()
    
    # Remove "+" sign
    cgpa_str = cgpa_str.replace('+', '').strip()
    
    try:
        return float(cgpa_str)
    except ValueError:
        return 0.0


def parse_departments(dept_str: str) -> List[str]:
    """Parse allowed departments from string"""
    if pd.isna(dept_str):
        return []
    
    dept_str = str(dept_str).strip()
    
    # Handle "ALL" or "OPEN TO ALL"
    if dept_str.upper() in ['ALL', 'OPEN TO ALL', 'ALL DEPARTMENTS', 'NOT DEPARTMENT SPECIFIC']:
        return ['ALL']
    
    # Handle "ONLY BTech."
    if 'ONLY BTech' in dept_str or 'ONLY BTECH' in dept_str.upper():
        return ['ALL']
    
    # Split by comma, 'and', or '&'
    depts = []
    parts = dept_str.replace(' and ', ',').split(',')
    
    for part in parts:
        part = part.strip()
        
        # Check if part contains '&' (like E&ECE)
        if '&' in part:
            sub_parts = part.split('&')
            for sub_part in sub_parts:
                sub_part = sub_part.strip()
                # Handle common abbreviations
                if sub_part in ['E', 'EE', 'Electrical']:
                    depts.append('EE')
                elif sub_part in ['ECE', 'EC', 'Electronics']:
                    depts.append('EC')
                elif len(sub_part) == 2 and sub_part.upper() in ['CS', 'EC', 'EE', 'ME', 'MA', 'CH', 'IM', 'IE', 
                                                                   'MI', 'MT', 'GG', 'EX', 'AE', 'CE', 'MF', 'HS',
                                                                   'AG', 'BT', 'CY', 'PH', 'NA', 'SD']:
                    depts.append(sub_part.upper())
        # Apply mappings
        elif part in DEPT_MAPPINGS:
            mapped = DEPT_MAPPINGS[part]
            if isinstance(mapped, list):
                depts.extend(mapped)
            else:
                depts.append(mapped)
        else:
            # Try to extract department code (2 letters)
            if len(part) >= 2:
                dept_code = part[:2].upper()
                if dept_code in ['CS', 'EC', 'EE', 'ME', 'MA', 'CH', 'IM', 'IE', 
                                 'MI', 'MT', 'GG', 'EX', 'AE', 'CE', 'MF', 'HS',
                                 'AG', 'BT', 'CY', 'PH', 'NA', 'SD']:
                    depts.append(dept_code)
    
    return list(set(depts)) if depts else ['ALL']


def parse_skills(skill_str: str) -> List[str]:
    """Parse required skills from string"""
    if pd.isna(skill_str) or skill_str == '':
        return []
    
    skill_str = str(skill_str).strip()
    
    # Split by comma
    skills = [s.strip() for s in skill_str.split(',')]
    
    # Clean up skills - remove parentheses content
    cleaned_skills = []
    for skill in skills:
        # Remove text in parentheses
        skill = skill.split('(')[0].strip()
        if skill:
            cleaned_skills.append(skill.lower())
    
    return cleaned_skills


def calculate_skill_match_score(student_skills: Set[str], required_skills: List[str]) -> float:
    """
    Calculate skill match score between student and company
    Returns a score between 0 and 10
    """
    if not required_skills:
        return 10.0  # No skills required, perfect match
    
    # Convert to lowercase for comparison
    student_skills_lower = set(s.lower() for s in student_skills)
    required_skills_lower = [s.lower() for s in required_skills]
    
    matched_count = 0
    
    # Common abbreviations mapping
    skill_mappings = {
        'dsa': ['data structures', 'algorithms', 'data structure'],
        'ml': ['machine learning'],
        'dl': ['deep learning'],
        'oop': ['object-oriented programming', 'object oriented programming'],
        'oops': ['object-oriented programming', 'object oriented programming'],
        'os': ['operating systems', 'operating system'],
        'dbms': ['database management systems', 'database'],
        'cp': ['competitive programming'],
    }
    
    for req_skill in required_skills_lower:
        # Check for partial match
        matched = False
        
        # First check direct partial matching
        for student_skill in student_skills_lower:
            if req_skill in student_skill or student_skill in req_skill:
                matched = True
                break
        
        # If not matched, check abbreviation mappings
        if not matched and req_skill in skill_mappings:
            for expanded in skill_mappings[req_skill]:
                for student_skill in student_skills_lower:
                    if expanded in student_skill or student_skill in expanded:
                        matched = True
                        break
                if matched:
                    break
        
        # Also check reverse mapping (student has abbreviation, company needs full name)
        if not matched:
            for abbrev, expansions in skill_mappings.items():
                if req_skill in expansions:
                    if abbrev in student_skills_lower:
                        matched = True
                        break
        
        if matched:
            matched_count += 1
    
    # Calculate percentage and scale to 0-10
    match_percentage = matched_count / len(required_skills_lower)
    return match_percentage * 10.0


def is_department_eligible(student_dept: str, allowed_depts: List[str]) -> bool:
    """Check if student's department is eligible"""
    if 'ALL' in allowed_depts:
        return True
    return student_dept in allowed_depts


def is_cgpa_eligible(student_cgpa: float, min_cgpa: float) -> bool:
    """Check if student meets CGPA requirement"""
    return student_cgpa >= min_cgpa


def is_domain_match(student_domains: List[str], job_role: str) -> bool:
    """Check if student's domain matches the job role"""
    for domain in student_domains:
        # Handle Core_XX domains
        if domain.startswith('Core_'):
            domain_key = 'Core_'
        else:
            domain_key = domain
        
        if domain_key in DOMAIN_JOB_ROLE_MAPPING:
            matching_roles = DOMAIN_JOB_ROLE_MAPPING[domain_key]
            for role in matching_roles:
                if role.lower() in job_role.lower() or job_role.lower() in role.lower():
                    return True
    
    return False


# ============================================================================
# SCORING FUNCTIONS
# ============================================================================

def calculate_profile_score(student: Student, company: Company) -> float:
    """
    Calculate ProfileScore for student at company
    ProfileScore = (w1 × CGPA_Score) + (w2 × Skill_Match_Score) + (w3 × R1) + (w4 × Dep_Score)
    where R1 is random [1, 10]
    """
    # Normalize CGPA to 1-10 scale (assuming CGPA range is 6-10)
    cgpa_score = ((student.cgpa - 6.0) / 4.0) * 10.0
    cgpa_score = max(1.0, min(10.0, cgpa_score))
    
    # Calculate skill match score (already in 1-10 range)
    skill_match_score = calculate_skill_match_score(student.skills, company.required_skills)
    
    # Random factor
    R1 = np.random.uniform(1, 10)
    
    # Get department score (default to 5 if not found)
    dep_score = DEP_SCORES.get(student.department, 5.0)
    
    # Calculate profile score with department score
    profile_score = (W1_CGPA_PROFILE * cgpa_score + 
                    W2_SKILL_PROFILE * skill_match_score + 
                    W3_RANDOM_PROFILE * R1 +
                    W4_DEP_SCORE_PROFILE * dep_score)
    
    return profile_score


def calculate_interview_score(student: Student, company: Company, profile_score: float) -> float:
    """
    Calculate InterviewScore for student
    InterviewScore = (w5 × ProfileScore) + (w6 × CGPA) + (w7 × R2)
    where R2 is random [0, 10]
    """
    # Random factor
    R2 = np.random.uniform(0, 10)
    
    # Calculate interview score
    interview_score = (W5_PROFILE_INTERVIEW * profile_score + 
                      W6_CGPA_INTERVIEW * student.cgpa + 
                      W7_RANDOM_INTERVIEW * R2)
    
    return interview_score


# ============================================================================
# DATA LOADING
# ============================================================================

def load_students(filepath: str) -> List[Student]:
    """Load students from CSV file"""
    df = pd.read_csv(filepath)
    
    students = []
    for _, row in df.iterrows():
        # Extract department from roll number
        roll_no = str(row['roll_no'])
        dept = roll_no[2:4].upper()
        
        # Parse skills
        skills_1 = []
        if pd.notna(row.get('skills_for_domain_1')):
            skills_1 = [s.strip() for s in str(row['skills_for_domain_1']).split(',')]
        
        skills_2 = []
        if pd.notna(row.get('skills_for_domain_2')):
            skills_2 = [s.strip() for s in str(row['skills_for_domain_2']).split(',')]
        
        # Get domain_2
        domain_2 = row.get('domain_2')
        if pd.isna(domain_2) or domain_2 == '':
            domain_2 = None
        
        student = Student(
            roll_no=roll_no,
            name=str(row['name']).strip(),
            cgpa=float(row['cgpa']),
            department=dept,
            domain_1=str(row['domain_1']),
            skills_1=skills_1,
            domain_2=domain_2,
            skills_2=skills_2
        )
        students.append(student)
    
    return students


def load_companies(filepath: str, shortlist_dir: str) -> List[Company]:
    """Load companies from CSV file and match with shortlist files"""
    df = pd.read_csv(filepath)
    
    companies = []
    for _, row in df.iterrows():
        company_name = str(row['company_name']).strip()
        job_role = str(row['job_role']).strip()
        
        # Parse fields
        allowed_depts = parse_departments(row['allowed_departments'])
        min_cgpa = parse_cgpa_requirement(row['min_cgpa'])
        required_skills = parse_skills(row['required_skills'])
        visit_day = int(row['arrival_day'])
        min_hires = int(row['min_offers'])
        max_hires = int(row['max_offers'])
        
        # Get interview slots from shortlist file
        company_id = f"{company_name}_{job_role}"
        shortlist_file = COMPANY_SHORTLIST_MAPPING.get(company_id)
        
        interview_slots = 0
        if shortlist_file:
            shortlist_path = os.path.join(shortlist_dir, shortlist_file)
            if os.path.exists(shortlist_path):
                shortlist_df = pd.read_csv(shortlist_path)
                interview_slots = len(shortlist_df)
        
        # FIX #1: If no shortlist or small shortlist, use max_hires * 2 as buffer
        # This allows companies to interview more candidates than shortlist size
        if interview_slots == 0:
            interview_slots = max_hires * 2  # Use 2x max_hires as interview capacity
        else:
            # Even with shortlist, ensure minimum interview capacity
            interview_slots = max(interview_slots, int(max_hires * 1.5))
        
        company = Company(
            company_name=company_name,
            job_role=job_role,
            allowed_departments=allowed_depts,
            min_cgpa=min_cgpa,
            required_skills=required_skills,
            visit_day=visit_day,
            min_hires=min_hires,
            max_hires=max_hires,
            interview_slots=interview_slots
        )
        companies.append(company)
    
    return companies


def load_company_order(filepath: str) -> Dict[int, List[str]]:
    """Load company order from CSV file"""
    # Read as text file since it has varying number of columns
    company_order = {}
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Format: "1.Company1,Company2,Company3"
            # Split by first dot to get serial number
            parts = line.split('.', 1)
            if len(parts) == 2:
                serial = int(parts[0])
                companies_str = parts[1]
                # Split by comma
                companies = [c.strip() for c in companies_str.split(',')]
                company_order[serial] = companies
    
    return company_order


# ============================================================================
# MAIN SIMULATION CODE (to be continued)
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("PLACEMENT SIMULATION - INITIALIZATION")
    print("="*80)
    
    # File paths
    base_dir = Path(r"c:\Users\nigam\Desktop\Simulation 2nd Presentation\new dataset")
    students_file = base_dir / "analysis_data.csv"
    companies_file = base_dir / "companies.csv"
    shortlist_dir = base_dir / "company shortlists(csv)"
    company_order_file = base_dir / "company_order.csv"
    
    # Load data
    print("\n[1/3] Loading students...")
    students = load_students(students_file)
    print(f"  ✓ Loaded {len(students)} students")
    
    print("\n[2/3] Loading companies...")
    companies = load_companies(companies_file, shortlist_dir)
    print(f"  ✓ Loaded {len(companies)} companies with shortlist data")
    
    print("\n[3/3] Loading company order...")
    company_order = load_company_order(company_order_file)
    print(f"  ✓ Loaded {len(company_order)} serial batches")
    
    print("\n" + "="*80)
    print("INITIALIZATION COMPLETE")
    print("="*80)
