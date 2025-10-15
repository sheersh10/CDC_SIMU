"""
Unit Tests for Placement Simulation
"""

import sys
from placement_simulation import *

def test_cgpa_parsing():
    """Test CGPA parsing function"""
    print("\n" + "="*80)
    print("TEST 1: CGPA Parsing")
    print("="*80)
    
    test_cases = [
        ("7+", 7.0),
        ("8.5+", 8.5),
        ("NONE", 0.0),
        ("NA", 0.0),
        ("None", 0.0),
        ("", 0.0),
        ("7.5+ for Dev, 8.5+ for Advanced Dev", 7.5),
        ("8.5+ preferably", 8.5),
    ]
    
    passed = 0
    for input_val, expected in test_cases:
        result = parse_cgpa_requirement(input_val)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{input_val}' -> {result} (expected {expected})")
        if result == expected:
            passed += 1
    
    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_department_parsing():
    """Test department parsing function"""
    print("\n" + "="*80)
    print("TEST 2: Department Parsing")
    print("="*80)
    
    test_cases = [
        ("ALL", ['ALL']),
        ("OPEN TO ALL", ['ALL']),
        ("CSE, MnC, ECE, EE", ['CS', 'MA', 'EC', 'EE']),
        ("Circuital", ['CS', 'MA', 'IM', 'EE', 'EC', 'IE']),
        ("E&ECE", ['EE', 'EC']),
    ]
    
    passed = 0
    for input_val, expected in test_cases:
        result = parse_departments(input_val)
        # Convert to sets for comparison (order doesn't matter)
        result_set = set(result)
        expected_set = set(expected)
        status = "✓" if result_set == expected_set else "✗"
        print(f"  {status} '{input_val}' -> {result}")
        if result_set == expected_set:
            passed += 1
    
    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_skill_matching():
    """Test skill matching function"""
    print("\n" + "="*80)
    print("TEST 3: Skill Matching")
    print("="*80)
    
    student_skills = {'Python', 'C++', 'Data Structures', 'Algorithms', 'Machine Learning', 'Deep Learning'}
    
    test_cases = [
        (['Python', 'C++'], 10.0),  # 100% match
        (['Python', 'Java'], 5.0),   # 50% match
        (['DSA', 'ML'], 10.0),       # Partial match (DSA matches Data Structures/Algorithms, ML matches Machine Learning)
        ([], 10.0),                  # No requirements
    ]
    
    passed = 0
    for required_skills, expected_min in test_cases:
        result = calculate_skill_match_score(student_skills, required_skills)
        status = "✓" if result >= expected_min - 1.0 else "✗"  # Allow small tolerance
        print(f"  {status} Required: {required_skills} -> Score: {result:.2f} (expected >= {expected_min})")
        if result >= expected_min - 1.0:
            passed += 1
    
    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_eligibility_checks():
    """Test eligibility checking functions"""
    print("\n" + "="*80)
    print("TEST 4: Eligibility Checks")
    print("="*80)
    
    # Test department eligibility
    print("\nDepartment Eligibility:")
    assert is_department_eligible('CS', ['ALL']) == True, "CS should be eligible for ALL"
    assert is_department_eligible('CS', ['CS', 'EC', 'EE']) == True, "CS should be eligible"
    assert is_department_eligible('ME', ['CS', 'EC', 'EE']) == False, "ME should not be eligible"
    print("  ✓ All department eligibility tests passed")
    
    # Test CGPA eligibility
    print("\nCGPA Eligibility:")
    assert is_cgpa_eligible(8.5, 7.0) == True, "8.5 >= 7.0"
    assert is_cgpa_eligible(6.5, 7.0) == False, "6.5 < 7.0"
    assert is_cgpa_eligible(7.0, 0.0) == True, "Any CGPA >= 0.0"
    print("  ✓ All CGPA eligibility tests passed")
    
    # Test domain matching
    print("\nDomain Matching:")
    assert is_domain_match(['SDE'], 'Software Development') == True, "SDE matches Software"
    assert is_domain_match(['Data'], 'Data Analyst') == True, "Data matches Data Analyst"
    assert is_domain_match(['Quant'], 'Quant Analyst') == True, "Quant matches Quant Analyst"
    assert is_domain_match(['SDE'], 'Quant') == False, "SDE doesn't match Quant"
    print("  ✓ All domain matching tests passed")
    
    print("\nResult: All eligibility tests passed")
    return True


def test_student_creation():
    """Test student object creation"""
    print("\n" + "="*80)
    print("TEST 5: Student Creation")
    print("="*80)
    
    student = Student(
        roll_no='23CS10001',
        name='Test Student',
        cgpa=8.5,
        department='CS',
        domain_1='SDE',
        skills_1=['Python', 'C++', 'DSA'],
        domain_2='Data',
        skills_2=['ML', 'DL']
    )
    
    assert student.roll_no == '23CS10001', "Roll number mismatch"
    assert student.department == 'CS', "Department mismatch"
    assert student.cgpa == 8.5, "CGPA mismatch"
    assert len(student.domains) == 2, "Should have 2 domains"
    assert 'SDE' in student.domains, "Should have SDE domain"
    assert 'Data' in student.domains, "Should have Data domain"
    assert len(student.skills) == 5, "Should have 5 unique skills"
    assert student.status == 'Unplaced', "Initial status should be Unplaced"
    
    print("  ✓ Student object created successfully")
    print(f"  ✓ {student}")
    print("\nResult: Student creation test passed")
    return True


def test_company_creation():
    """Test company object creation"""
    print("\n" + "="*80)
    print("TEST 6: Company Creation")
    print("="*80)
    
    company = Company(
        company_name='Test Company',
        job_role='SDE',
        allowed_departments=['CS', 'EC', 'EE'],
        min_cgpa=7.5,
        required_skills=['Python', 'DSA', 'OOP'],
        visit_day=1,
        min_hires=5,
        max_hires=10,
        interview_slots=30
    )
    
    assert company.company_name == 'Test Company', "Company name mismatch"
    assert company.job_role == 'SDE', "Job role mismatch"
    assert company.min_cgpa == 7.5, "Min CGPA mismatch"
    assert company.visit_day == 1, "Visit day mismatch"
    assert company.interview_slots == 30, "Interview slots mismatch"
    assert len(company.applicants) == 0, "Should have no applicants initially"
    
    print("  ✓ Company object created successfully")
    print(f"  ✓ {company}")
    print("\nResult: Company creation test passed")
    return True


def test_scoring_functions():
    """Test scoring functions"""
    print("\n" + "="*80)
    print("TEST 7: Scoring Functions")
    print("="*80)
    
    # Create test student and company
    student = Student(
        roll_no='23CS10001',
        name='Test Student',
        cgpa=9.0,
        department='CS',
        domain_1='SDE',
        skills_1=['Python', 'C++', 'DSA', 'OOP', 'ML'],
        domain_2=None,
        skills_2=None
    )
    
    company = Company(
        company_name='Test Company',
        job_role='SDE',
        allowed_departments=['CS'],
        min_cgpa=7.0,
        required_skills=['Python', 'DSA', 'OOP'],
        visit_day=1,
        min_hires=1,
        max_hires=5,
        interview_slots=10
    )
    
    # Test profile score
    profile_score = calculate_profile_score(student, company)
    print(f"  ✓ Profile Score: {profile_score:.2f}")
    assert 0 <= profile_score <= 30, "Profile score should be reasonable"
    
    # Test interview score
    interview_score = calculate_interview_score(student, company, profile_score)
    print(f"  ✓ Interview Score: {interview_score:.2f}")
    assert 0 <= interview_score <= 30, "Interview score should be reasonable"
    
    print("\nResult: Scoring functions test passed")
    return True


def run_all_tests():
    """Run all unit tests"""
    print("\n" + "="*80)
    print("RUNNING ALL UNIT TESTS")
    print("="*80)
    
    tests = [
        test_cgpa_parsing,
        test_department_parsing,
        test_skill_matching,
        test_eligibility_checks,
        test_student_creation,
        test_company_creation,
        test_scoring_functions
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("✓ ALL TESTS PASSED!")
        return True
    else:
        print("✗ SOME TESTS FAILED")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
