# 🔍 Issues Identified and Fixes Required

## Issue #1: Companies Hiring 0 Students (min_hires not enforced)

### Problem:
Companies like Adobe (MDSR), HUL, ITC, JPMC roles hired 0 students even though they have `min_offers` requirements.

**Root Cause:**
In `run_simulation.py` line 143:
```python
offer_count = min(actual_openings, len(interview_scores))
```

This allows `offer_count = 0` if `len(interview_scores) = 0` (no shortlisted students).

### Examples from Day 1:
- **Adobe (MDSR)**: min_offers=7, max_offers=10 → Hired 0 ❌
- **HUL Supply Chain**: min_offers=4, max_offers=8 → Hired 0 ❌  
- **ITC KITES**: min_offers=4, max_offers=8 → Hired 0 ❌
- **JPMC CCB/MRGR/QR**: min_offers=3 each → All hired 0 ❌
- **Proctor & Gamble**: min_offers=3, max_offers=5 → Not even loaded ❌

### Why They Got 0 Students:

1. **Adobe (MDSR)**: Has shortlist file, but no domain match
   - Job requires: ML, DL, NLP skills
   - Most students have SDE/Quant domains
   
2. **HUL Supply Chain**: Domain mismatch
   - Job doesn't map to any student domain (Core_Supply Chain)
   - 0 applicants because of domain filtering
   
3. **ITC, JPMC roles**: Similar domain/department mismatch
   - 0 eligible students after filtering

### Fix Required:
```python
# In run_simulation.py, step5_interview_hiring()
# BEFORE:
offer_count = min(actual_openings, len(interview_scores))

# AFTER: Ensure minimum hiring if students available
if len(interview_scores) >= company.min_hires:
    # Have enough candidates, hire between min and max
    offer_count = min(actual_openings, len(interview_scores))
else:
    # Not enough candidates
    offer_count = len(interview_scores)  # Hire all available
    if offer_count > 0:
        print(f"  WARNING: {company.company_name} couldn't meet min_hires ({company.min_hires}), hiring {offer_count}")
```

---

## Issue #2: Missing Day 1 Companies

### Companies in companies.csv (Day 1) but NOT in simulation:

| Company | Role | Min/Max | Shortlist File | Why Missing? |
|---------|------|---------|----------------|--------------|
| **Goldman Sachs** | SDE | 11/15 | ✅ `goldman_sachs(sde).csv` | Not in mapping! |
| **Natwest** | SDE | 7/10 | ✅ `natwest.csv` | Not in mapping! |
| **LEK** | Consulting | 3/5 | ✅ bcg.csv (similar) | Not in companies.csv! |
| **Wells Fargo** | Tech | 4/6 | ✅ `wells_fargo(technology).csv` | Not in mapping! |
| **NVIDIA** | System Software | 7/10 | ✅ `nvidia.csv` | In mapping but not loading? |
| **AWL Inc** | AI Engineer | 1/3 | ✅ `awl.csv` | In mapping ✅ |
| **Rippling** | AI/SDE | 2/5 | ✅ `rippling.csv` | In mapping ✅ |
| **Proctor & Gamble** | Consulting | 3/5 | ❌ No file | Mapping shows None |

**Lost Capacity from missing companies:** ~40-50 positions!

### Fix Required:
Add to `COMPANY_SHORTLIST_MAPPING` in `placement_simulation.py`:

```python
# Add these missing entries:
'Goldman Sachs_SDE': 'goldman_sachs(sde).csv',
'Natwest_SDE': 'natwest.csv',
'LEK_Consulting': 'bcg.csv',
'Wells Fargo_Tech': 'wells_fargo(technology).csv',
'NVIDIA_System Software Engineer': 'nvidia.csv',
'Proctor and Gamble_Consultinig': None,  # No shortlist available
```

---

## Issue #3: Multiple Roles for Same Company

### Problem:
Some companies visit with multiple roles but only one is tracked.

### Examples:

**American Express:**
- In companies.csv: Only "Analyst" role (Data-focused)
- Expected: Should also have "SDE" role
- Check: Look for `amex(sde).csv` file

**Goldman Sachs:**
- Available files: `goldman_sachs(quant).csv` AND `goldman_sachs(sde).csv`
- In companies.csv: Only one entry visible
- Need: Check if both roles are in CSV

**Natwest:**
- Available files: `natwest.csv` AND `natwest(data).csv`  
- Should have 2 roles: SDE and Data

**LEK:**
- Has shortlist file but not in companies.csv at all!

### Investigation Needed:
Let me check if companies.csv has multiple rows for these companies...

---

## Issue #4: Company Name Variations

### Problem:
Typo in mapping: `'Natweest_SDE'` (extra 'e')
Should be: `'Natwest_SDE'`

---

## Summary of Required Fixes

### Priority 1: Fix min_hires Enforcement
**Impact:** Companies can't hire 0 if they have min_hires > 0
**Files:** `run_simulation.py` (step5_interview_hiring)

### Priority 2: Add Missing Company Mappings
**Impact:** +6-8 companies, ~40-50 additional positions
**Files:** `placement_simulation.py` (COMPANY_SHORTLIST_MAPPING)
Companies to add:
- Goldman Sachs SDE
- Natwest SDE (fix typo)
- Wells Fargo Tech
- NVIDIA (already mapped but not loading?)

### Priority 3: Investigate Multiple Roles
**Impact:** Potentially double capacity for some companies
**Action:** Check companies.csv for all company entries

### Priority 4: Fix Domain Matching
**Impact:** Companies like HUL, ITC, JPMC getting 0 applicants
**Files:** `placement_simulation.py` (DOMAIN_JOB_ROLE_MAPPING)
**Action:** Broaden domain mappings for edge cases

---

## Next Steps

1. ✅ List all shortlist files available
2. ✅ Identify which companies are missing from mapping
3. ⏳ Check if companies.csv has multiple entries per company
4. ⏳ Implement min_hires enforcement
5. ⏳ Add missing company mappings
6. ⏳ Fix domain matching issues
7. ⏳ Re-run simulation

Would you like me to implement these fixes now?
