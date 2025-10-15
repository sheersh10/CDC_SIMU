# SIMULATION RESULTS WITH UPDATED PROFILE SCORE FORMULA

## Updated Formula
```
ProfileScore = w1*CGPA + w2*Skill_Match + w3*R1 + w4*Dep_Score
where:
  w1 = 0.3 (CGPA weight)
  w2 = 0.2 (Skill Match weight) 
  w3 = 0.2 (Random factor weight)
  w4 = 0.3 (Department Score weight)
```

## Department Scores Used (from dep_score.csv)
- CS: 10, MA: 10, EC: 10, EE: 8, IE: 8, CH: 7, IM: 7, ME: 7, MF: 7, HS: 5, AE: 5, MT: 4, AG: 3, BT: 3, CE: 3, MI: 3, GG: 3, EX: 3, CY: 2, PH: 2

---

## OVERALL STATISTICS

| Metric | Value |
|--------|-------|
| **Total Students** | 1,223 |
| **Total Placed** | **120** (9.81%) |
| **Total Unplaced** | 1,006 (82.3%) |
| **Total Opted Out** | 97 (7.9%) |
| **Companies Hired** | 36 |

---

## COMPANY-WISE HIRING (All 36 Companies)

| Rank | Company | Students Hired |
|------|---------|----------------|
| 1 | Graviton Research Capital_SDE | **8** |
| 2 | Alphagrep_SDE | **7** |
| 3 | Google_Core | **7** |
| 4 | Adobe_Data | **6** |
| 5 | Microsoft_Software Development | **6** |
| 6 | HUL_DATA | **6** |
| 7 | Databricks_SDE | **5** |
| 8 | Rubrik_SDE | **5** |
| 9 | Amazon_SDE | **5** |
| 10 | BAIN_Consulting | **5** |
| 11 | JPMC_Finance | **5** |
| 12 | Adobe_SDE | **4** |
| 13 | Morgan Stanley_Data | **4** |
| 14 | Google_SDE | **4** |
| 15 | Stripe_Data | **4** |
| 16 | Optiver_Quant | **3** |
| 17 | ITC_CORE_ME/IM | **3** |
| 18 | Blackrock_Finance | **3** |
| 19-36 | 18 companies with 1-2 hires each | 1-2 |

---

## DEPARTMENT-WISE PLACEMENT DATA

| Rank | Department | Placed | Total | Placement Rate |
|------|------------|--------|-------|----------------|
| 1 | **CS** (Computer Science) | **49** | 90 | **54.44%** ⬆️ |
| 2 | **MA** (Mathematics) | **24** | 74 | **32.43%** |
| 3 | **EC** (Electronics) | **21** | 95 | **22.11%** ⬆️ |
| 4 | **HS** (Humanities) | **7** | 65 | **10.77%** |
| 5 | **IM** (Industrial Mgmt) | **3** | 41 | **7.32%** |
| 6 | **ME** (Mechanical) | **6** | 105 | **5.71%** |
| 7 | **EE** (Electrical) | **5** | 89 | **5.62%** ⬇️ |
| 8 | **MF** (Manufacturing) | **1** | 35 | **2.86%** |
| 9 | **CH** (Chemical) | **2** | 87 | **2.30%** |
| 10 | **GG** (Geology) | **1** | 47 | **2.13%** |
| 11 | **IE** (Industrial Eng) | **1** | 48 | **2.08%** |

**Note:** Only 11 departments got placements (vs 20+ in previous runs)

---

## COMPARISON WITH PREVIOUS FORMULA

### Previous Formula (W1=0.3, W2=0.3, W3=0.4, NO Dep_Score):
- **Average Placements:** 157.2 ± 5.9 students
- **Placement Rate:** 12.85% ± 0.48%
- **Opted Out:** 108.9 ± 10.0

### New Formula (W1=0.3, W2=0.2, W3=0.2, W4=0.3 with Dep_Score):
- **Placements:** **120 students** (-37 placements, **-23.5%** ⚠️)
- **Placement Rate:** **9.81%** (-3.04% ⚠️)
- **Opted Out:** 97 (-11.9)

---

## KEY INSIGHTS

### 1. **Overall Impact: NEGATIVE**
   - **37 fewer placements** compared to average (157.2 → 120)
   - **3% drop** in placement rate
   - This is the **worst result** across all formula variations tested

### 2. **Department Score Impact:**
   - **High-scoring departments benefited:**
     - CS (score 10): 54.44% placement rate ⬆️ (+8.88%)
     - EC (score 10): 22.11% placement rate ⬆️ (+8.22%)
     - MA (score 10): 32.43% placement rate ⬆️ (+5.40%)
   
   - **Low-scoring departments severely affected:**
     - CY (score 2): 0% placement ⬇️ (was 10.70%)
     - AG (score 3): 0% placement ⬇️ (was 17.25%)
     - MT (score 4): 0% placement ⬇️ (was 6.89%)
     - AE (score 5): 0% placement ⬇️ (was 7.91%)
     - SD, BT, CE, EX, MI, PH: All 0% ⬇️

### 3. **Concentration Effect:**
   - Placements became **highly concentrated** in top 3 departments (CS, MA, EC)
   - These 3 departments account for **94 out of 120** placements (78.3%)
   - **10 departments got ZERO placements** (vs all departments getting some in previous formula)

### 4. **Company Hiring Patterns:**
   - Top companies still hired, but overall numbers reduced
   - More companies unable to meet minimum requirements
   - Graviton SDE became top hirer (8 students)

---

## RECOMMENDATION

❌ **DO NOT USE this formula** - It creates severe bias favoring high-scoring departments

**Reasons:**
1. **23.5% drop in total placements** is unacceptable
2. **Unfair disadvantage** to students from lower-scoring departments
3. **10 departments completely shut out** from placements
4. Does not reflect real-world placement patterns
5. Creates artificial hierarchy based on department scores

**Alternative Suggestions:**
1. **Revert to original formula** (W1=0.3, W2=0.3, W3=0.4) which gave ~157 placements
2. If department score must be included, use **much lower weight** (e.g., W4=0.1) and adjust others
3. Consider department score as a **tie-breaker** rather than weighted component

---

## STATISTICAL SUMMARY

**Profile Score Components (New Formula):**
- CGPA: 30% weight
- Skill Match: 20% weight
- Random Factor: 20% weight  
- **Department Score: 30% weight** ⚠️ (Too high!)

**Result:** Department score dominates profile, reducing diversity and overall placements.

