"""
Main Placement Simulation Engine
Implements the multi-stage placement process
"""

from placement_simulation import *
import json
import sys
import os

# Check for seed argument
if len(sys.argv) > 2 and sys.argv[1] == '--seed':
    seed = int(sys.argv[2])
    os.environ['RANDOM_SEED'] = str(seed)
    # Re-import to use new seed
    import importlib
    import placement_simulation
    importlib.reload(placement_simulation)
    from placement_simulation import *

# ============================================================================
# SIMULATION ENGINE
# ============================================================================

class PlacementSimulation:
    """Main simulation engine for placement process"""
    
    def __init__(self, students: List[Student], companies: List[Company], company_order: Dict[int, List[str]]):
        self.students = {s.roll_no: s for s in students}
        self.companies = {c.get_unique_id(): c for c in companies}
        self.company_order = company_order
        self.current_day = 0
        
        # Statistics
        self.stats = {
            'day_wise_placements': {},
            'company_wise_hires': {},
            'unplaced_students': len(students),
            'opted_out_students': 0
        }
    
    def get_unplaced_students(self) -> List[Student]:
        """Get list of unplaced students"""
        return [s for s in self.students.values() if s.status == 'Unplaced']
    
    def get_companies_for_day(self, day: int, serial: int) -> List[Company]:
        """Get companies for a specific day and serial number"""
        if serial not in self.company_order:
            return []
        
        company_names = self.company_order[serial]
        day_companies = []
        
        for c in self.companies.values():
            if c.visit_day == day:
                # Check if company name matches (partial matching)
                for order_name in company_names:
                    if order_name.lower() in c.company_name.lower() or c.company_name.lower() in order_name.lower():
                        day_companies.append(c)
                        break
        
        return day_companies
    
    def step1_initialization(self, day: int, serial: int):
        """Step 1: Initialize for the day/serial"""
        print(f"\n{'='*80}")
        print(f"DAY {day} - SERIAL {serial}")
        print(f"{'='*80}")
        
        companies = self.get_companies_for_day(day, serial)
        unplaced_students = self.get_unplaced_students()
        
        print(f"\nCompanies visiting: {len(companies)}")
        for c in companies:
            print(f"  - {c.company_name} ({c.job_role}) - Slots: {c.interview_slots}")
        print(f"\nUnplaced students: {len(unplaced_students)}")
        
        return companies, unplaced_students
    
    def step2_application(self, companies: List[Company], unplaced_students: List[Student]):
        """Step 2: Students apply to eligible companies"""
        print(f"\n[STEP 2] Application Phase")
        print("-" * 80)
        
        for company in companies:
            company.applicants = []
            
            for student in unplaced_students:
                # Check eligibility
                dept_eligible = is_department_eligible(student.department, company.allowed_departments)
                cgpa_eligible = is_cgpa_eligible(student.cgpa, company.min_cgpa)
                domain_match = is_domain_match(student.domains, company.job_role)
                
                if dept_eligible and cgpa_eligible and domain_match:
                    company.applicants.append(student)
                    student.current_applications.append(company.get_unique_id())
            
            print(f"  {company.company_name} ({company.job_role}): {len(company.applicants)} applicants")
    
    def step3_test_invitation(self, companies: List[Company]):
        """Step 3: All eligible students are invited for test (no pre-screening needed)"""
        print(f"\n[STEP 3] Test Invitation Phase (All eligible students invited)")
        print("-" * 80)
        
        for company in companies:
            # All applicants are invited to test (as per clarification)
            company.test_invited = company.applicants.copy()
            print(f"  {company.company_name}: {len(company.test_invited)} students invited for test")
    
    def step4_interview_shortlist(self, companies: List[Company]):
        """Step 4: Shortlist students for interview based on test performance"""
        print(f"\n[STEP 4] Interview Shortlisting Phase (Post-Test)")
        print("-" * 80)
        
        for company in companies:
            # Calculate profile scores for all test-invited students
            student_scores = []
            
            for student in company.test_invited:
                profile_score = calculate_profile_score(student, company)
                student_scores.append((student, profile_score))
            
            # Sort by profile score (descending)
            student_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Shortlist top N students where N = interview_slots
            shortlist_count = min(company.interview_slots, len(student_scores))
            company.shortlisted = [s[0] for s in student_scores[:shortlist_count]]
            
            # Store profile scores for later use
            company.profile_scores = {s[0].roll_no: s[1] for s in student_scores[:shortlist_count]}
            
            print(f"  {company.company_name}: {len(company.shortlisted)} students shortlisted for interview")
    
    def step5_interview_hiring(self, companies: List[Company]):
        """Step 5: Conduct interviews and make offers"""
        print(f"\n[STEP 5] Interview & Hiring Phase")
        print("-" * 80)
        
        for company in companies:
            # Calculate interview scores
            interview_scores = []
            for student in company.shortlisted:
                profile_score = company.profile_scores.get(student.roll_no, 0)
                interview_score = calculate_interview_score(student, company, profile_score)
                interview_scores.append((student, interview_score))
            
            # Sort by interview score (descending)
            interview_scores.sort(key=lambda x: x[1], reverse=True)
            
            num_candidates = len(interview_scores)
            
            # CRITICAL FIX: Determine actual openings first
            if num_candidates >= company.min_hires:
                # Have enough candidates - determine openings (random between min and max)
                actual_openings = random.randint(company.min_hires, company.max_hires)
                
                # OVER-OFFER to ensure we meet minimum after students choose other companies
                # Offer to 1.5x the target to account for students who will reject
                buffered_offers = min(int(actual_openings * 1.5), num_candidates)
                offer_count = max(buffered_offers, company.min_hires)  # Never less than min
            else:
                # Not enough candidates to meet minimum requirement
                offer_count = num_candidates
                actual_openings = company.min_hires  # Show what we needed
                if num_candidates > 0:
                    print(f"  ⚠️  WARNING: {company.company_name} couldn't meet min_hires ({company.min_hires}), only {num_candidates} candidates available!")
                else:
                    print(f"  ⚠️  WARNING: {company.company_name} has 0 candidates (min_hires: {company.min_hires})!")
            
            company.offered = [s[0] for s in interview_scores[:offer_count]]
            company.target_hires = actual_openings  # Store target for tracking
            
            # Update student status to Offered
            for student in company.offered:
                student.status = 'Offered'
            
            print(f"  {company.company_name}: {offer_count} offers made (target: {actual_openings}, min_required: {company.min_hires})")
    
    def step6_offer_acceptance(self, companies: List[Company]):
        """Step 6: Students accept offers and opt-out check"""
        print(f"\n[STEP 6] Offer Acceptance & Day End")
        print("-" * 80)
        
        # Collect all offers for students who got multiple offers
        student_offers = {}
        for company in companies:
            for student in company.offered:
                if student.roll_no not in student_offers:
                    student_offers[student.roll_no] = []
                student_offers[student.roll_no].append(company)
        
        # Process offers
        for roll_no, offers in student_offers.items():
            student = self.students[roll_no]
            
            # If student already placed (from earlier in same serial), skip
            if student.status == 'Placed':
                continue
            
            # Randomly select one offer if multiple
            selected_company = random.choice(offers)
            
            # Accept offer
            student.status = 'Placed'
            student.placed_company = selected_company.get_unique_id()
            selected_company.hired.append(student)
            
            print(f"  {student.roll_no} accepted offer from {selected_company.company_name}")
        
        # Update statistics
        total_placed = sum(len(c.hired) for c in companies)
        print(f"\nTotal placements in this batch: {total_placed}")
        
        # Reset statuses for non-placed students
        unplaced_count = 0
        opted_out_count = 0
        
        for student in self.students.values():
            if student.status == 'Offered' and student not in [s for c in companies for s in c.hired]:
                student.status = 'Unplaced'
            
            if student.status == 'Unplaced':
                # Opt-out check
                if random.random() < P_OPT_OUT:
                    student.status = 'Opted_Out'
                    opted_out_count += 1
                else:
                    unplaced_count += 1
                    
                # Clear current applications
                student.current_applications = []
        
        print(f"Remaining unplaced students: {unplaced_count}")
        print(f"Students opted out: {opted_out_count}")
        
        self.stats['unplaced_students'] = unplaced_count
        self.stats['opted_out_students'] += opted_out_count
        
        # Update company-wise statistics
        for company in companies:
            company_id = company.get_unique_id()
            self.stats['company_wise_hires'][company_id] = len(company.hired)
    
    def simulate_day(self, day: int):
        """Simulate one complete day"""
        print(f"\n{'#'*80}")
        print(f"# SIMULATING DAY {day}")
        print(f"{'#'*80}")
        
        # Process each serial number in order
        for serial in sorted(self.company_order.keys()):
            companies, unplaced_students = self.step1_initialization(day, serial)
            
            if not companies:
                print(f"\nNo companies for serial {serial}")
                continue
            
            if not unplaced_students:
                print(f"\nNo unplaced students remaining!")
                break
            
            self.step2_application(companies, unplaced_students)
            self.step3_test_invitation(companies)
            self.step4_interview_shortlist(companies)
            self.step5_interview_hiring(companies)
            self.step6_offer_acceptance(companies)
        
        # Day summary
        placed_students = [s for s in self.students.values() if s.status == 'Placed']
        self.stats['day_wise_placements'][day] = len(placed_students)
        
        print(f"\n{'='*80}")
        print(f"DAY {day} SUMMARY")
        print(f"{'='*80}")
        print(f"Total placed students: {len(placed_students)}")
        print(f"Unplaced students: {self.stats['unplaced_students']}")
        print(f"Opted out students: {self.stats['opted_out_students']}")
    
    def print_final_statistics(self):
        """Print final simulation statistics"""
        print(f"\n{'#'*80}")
        print(f"# FINAL SIMULATION STATISTICS")
        print(f"{'#'*80}")
        
        placed_students = [s for s in self.students.values() if s.status == 'Placed']
        unplaced_students = [s for s in self.students.values() if s.status == 'Unplaced']
        opted_out_students = [s for s in self.students.values() if s.status == 'Opted_Out']
        
        print(f"\nOverall Placement Summary:")
        print(f"  Total Students: {len(self.students)}")
        print(f"  Placed: {len(placed_students)} ({len(placed_students)/len(self.students)*100:.1f}%)")
        print(f"  Unplaced: {len(unplaced_students)} ({len(unplaced_students)/len(self.students)*100:.1f}%)")
        print(f"  Opted Out: {len(opted_out_students)} ({len(opted_out_students)/len(self.students)*100:.1f}%)")
        
        print(f"\nCompany-wise Hiring:")
        for company_id, count in sorted(self.stats['company_wise_hires'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {company_id}: {count} students")
    
    def export_results(self, output_file: str):
        """Export results to CSV"""
        results = []
        for student in self.students.values():
            results.append({
                'roll_no': student.roll_no,
                'name': student.name,
                'department': student.department,
                'cgpa': student.cgpa,
                'domain_1': student.domain_1,
                'domain_2': student.domain_2,
                'status': student.status,
                'placed_company': student.placed_company if student.placed_company else 'Not Placed'
            })
        
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        print(f"\nResults exported to: {output_file}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("PLACEMENT SIMULATION - DAY 1")
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
    print(f"  Loaded {len(students)} students")
    
    print("\n[2/3] Loading companies...")
    companies = load_companies(companies_file, shortlist_dir)
    print(f"  Loaded {len(companies)} companies")
    
    print("\n[3/3] Loading company order...")
    company_order = load_company_order(company_order_file)
    print(f"  Loaded {len(company_order)} serial batches")
    
    # Initialize simulation
    print("\n" + "="*80)
    print("INITIALIZING SIMULATION")
    print("="*80)
    
    simulation = PlacementSimulation(students, companies, company_order)
    
    # Run Day 1 simulation
    simulation.simulate_day(day=1)
    
    # Print final statistics
    simulation.print_final_statistics()
    
    # Export results
    output_file = base_dir / "day1_placement_results.csv"
    simulation.export_results(output_file)
    
    print("\n" + "="*80)
    print("SIMULATION COMPLETE!")
    print("="*80)
