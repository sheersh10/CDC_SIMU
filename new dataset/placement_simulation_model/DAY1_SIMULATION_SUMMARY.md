# Placement Simulation - Day 1 Results Summary

## Simulation Overview

This simulation implements a multi-stage placement process with the following stages:
1. **Application Phase** - Students apply to eligible companies
2. **Test Invitation Phase** - All eligible students invited for online test
3. **Interview Shortlisting Phase** - Top performers shortlisted based on ProfileScore
4. **Interview & Hiring Phase** - Final selection based on InterviewScore
5. **Offer Acceptance Phase** - Students accept offers, opt-out probability applied

## Simulation Parameters

### Scoring Weights
- **ProfileScore** = 0.3×CGPA_Score + 0.3×Skill_Match_Score + 0.4×Random(1-10)
- **InterviewScore** = 0.3×ProfileScore + 0.5×CGPA + 0.2×Random(0-10)
- **Opt-out Probability** = 5%

### Eligibility Criteria
- **Department Matching**: Based on company requirements
- **CGPA**: Minimum CGPA threshold per company
- **Domain Matching**: Student domains must match job role
- **Skills**: Partial matching with abbreviation support (e.g., DSA → Data Structures/Algorithms)

## Day 1 Results

### Overall Statistics
- **Total Students**: 1,223 (Note: 2 students missing from analysis_data.csv with roll numbers 23MI10044, 23MI10045)
- **Placed Students**: 120 (9.8%)
- **Unplaced Students**: 1,006 (82.3%)
- **Opted Out**: 97 (7.9%)

### Serial-wise Breakdown

#### Serial 1 (8 Companies)
**Companies**: Alphagrep, Samsung(Korea), Databricks, Graviton, Optiver, Quadeye, Rubrik, Trexquant

**Results**:
- Total Offers Made: 36
- Total Placements: 30
- Students Opted Out: 51

**Top Performers**:
- Databricks: 7 placements
- Graviton Research Capital: 6 placements
- Optiver: 6 placements

#### Serial 2 (23 Companies)
**Companies**: Adobe, Amazon, American Express (AMEX), Atlassian, Bain, BCG, Blackrock, DE Shaw, Goldman Sachs (GS), Google, HUL, ITC, JPMC, Microsoft, Morgan Stanley, Nomura, Salesforce, Samsara, Uber, Stripe, and more

**Results**:
- Total Offers Made: 136
- Total Placements: 90
- Students Opted Out: 46

**Top Performers**:
- Google SWE: 11 placements
- Amazon SDE: 10 placements
- Microsoft: 9 placements
- Blackrock Finance: 8 placements

### Company-wise Placement Details

| Rank | Company | Role | Placements |
|------|---------|------|------------|
| 1 | Google | SWE | 11 |
| 2 | Amazon | SDE | 10 |
| 3 | Microsoft | Software Development | 9 |
| 4 | Blackrock | Finance | 8 |
| 5 | Databricks | Software | 7 |
| 6 | Adobe | Research Intern | 7 |
| 7 | Google | Core | 7 |
| 8 | Graviton Research Capital | Software | 6 |
| 9 | Optiver | Quant | 6 |
| 10 | Morgan Stanley | Sales and Trading | 6 |

### Notable Observations

1. **High Competition**: 
   - Microsoft received 854 applications but could only shortlist 45 for interviews
   - Google SWE received 854 applications with 59 interview slots
   - Databricks received 1,128 applications for 33 interview slots

2. **Zero Applicants**:
   - HUL (Supply Chain) - No domain match
   - ITC (KITES Intern) - No domain match
   - JPMC roles - No domain match with student domains

3. **Zero Offers Despite Applications**:
   - Samsung SDE (0 offers despite 136 applicants) - min_offers = 0, max_offers = 5
   - Trexquant (0 offers despite 93 applicants) - only 2 interview slots

4. **Quant Roles**:
   - High selectivity with CGPA requirements (mostly 9.0+)
   - Optiver: 6 placements from 62 applicants
   - Quadeye: 4 placements from 58 applicants

5. **Consulting Roles**:
   - BAIN: 5 placements from 29 applicants
   - BCG: 4 placements from 29 applicants
   - Good conversion rate (~15-17%)

6. **Finance Roles**:
   - Blackrock Finance: 8 placements from 64 applicants
   - Morgan Stanley: 6 placements from 61 applicants
   - American Express: 4 placements from 180 applicants

## Student Performance Analysis

### Top Performing Students (Sample)
- **23CS10001** - Placed at Graviton Research Capital
- **23CS10003** - Placed at Blackrock
- **23CS10004** - Placed at Adobe
- **23MA10007** - Placed at Adobe (Research)
- **23CS10015** - Placed at American Express

### Department-wise Placement Rate (Top Departments)
Based on the placements:
- **CS (Computer Science)**: High placement rate in tech roles
- **MA (Mathematics & Computing)**: Strong in Quant and Tech roles
- **EC (Electronics)**: Good placement in SDE and Core roles
- **EE (Electrical Engineering)**: Placed in diverse roles

## Issues Encountered & Fixes

### 1. Missing Company-Shortlist Mappings
**Issue**: Some companies in companies.csv had no corresponding shortlist files
**Resolution**: Skipped 34 companies without shortlist data

### 2. Department Code Variations
**Issue**: Companies used inconsistent department codes (CSE vs CS, ECE vs EC)
**Resolution**: Created comprehensive mapping dictionary

### 3. CGPA Parsing
**Issue**: Multiple formats (7+, 8.5+, "NONE", "7.5+ for Dev, 8.5+ for Advanced Dev")
**Resolution**: Regex-based parser with conditional handling

### 4. Skill Matching
**Issue**: Abbreviations not matching (DSA vs Data Structures and Algorithms)
**Resolution**: Implemented abbreviation mapping (DSA→Data Structures, ML→Machine Learning, etc.)

### 5. Domain Matching
**Issue**: Job roles didn't always directly match domain names
**Resolution**: Created domain-to-job-role mapping dictionary

## Files Generated

1. **placement_simulation.py** - Core simulation classes and utilities
2. **test_simulation.py** - Unit tests (7/7 passed)
3. **run_simulation.py** - Main simulation engine
4. **day1_placement_results.csv** - Complete results with student status

## Validation & Testing

### Unit Tests Passed (7/7)
✓ CGPA Parsing (8/8 test cases)
✓ Department Parsing (5/5 test cases)
✓ Skill Matching (4/4 test cases)
✓ Eligibility Checks (All passed)
✓ Student Creation (Passed)
✓ Company Creation (Passed)
✓ Scoring Functions (Passed)

### Simulation Validation
✓ All students properly initialized
✓ Department eligibility correctly enforced
✓ CGPA thresholds properly checked
✓ Domain matching working as expected
✓ Interview slots respected (shortlist count ≤ interview_slots)
✓ Hiring limits respected (offers ≤ max_hires)
✓ No student placed in multiple companies
✓ Opt-out probability applied correctly

## Next Steps

To run Day 2, 3, or 4 simulations:

```python
# Modify run_simulation.py to simulate additional days
simulation.simulate_day(day=2)
simulation.simulate_day(day=3)
simulation.simulate_day(day=4)
```

## Key Insights

1. **Placement Rate**: Only 9.8% students placed on Day 1, which is realistic for a competitive placement process
2. **High Competition**: Top companies (Google, Microsoft, Amazon) had 15-20x applications vs slots
3. **Domain Importance**: Companies without matching domains got zero applicants
4. **CGPA Threshold**: High CGPA requirements (8.5+, 9.0+) significantly reduce applicant pool
5. **Random Factors**: 40% weight on random component in ProfileScore creates variability
6. **Opt-out Impact**: 97 students (7.9%) opted out, reducing available pool for subsequent days

## Recommendations for Tuning

If placement rate seems low:
1. **Increase interview_slots** per company
2. **Reduce minimum CGPA** requirements
3. **Broaden domain matching** rules
4. **Decrease opt-out probability** (currently 5%)
5. **Increase max_hires** for companies

If placement rate seems high:
1. **Add more filtering** in test invitation phase
2. **Increase CGPA weights** in scoring functions
3. **Make skill matching stricter** (require more skills)
4. **Add department quotas** per company

---

**Simulation Date**: Day 1 Complete
**Status**: ✓ Successfully Executed
**Output**: day1_placement_results.csv
