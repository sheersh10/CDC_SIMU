# 📊 PLACEMENT SIMULATION DASHBOARD - COMPLETE PLAN

## 1. ARCHITECTURE

```
Frontend (HTML/CSS/JS)
    ↓
FastAPI Backend (Python)
    ↓
Simulation Engine (placement_simulation.py)
    ↓
Data (CSV files)
```

---

## 2. DASHBOARD SECTIONS & VISUALIZATIONS

#### SECTION A: DATA OVERVIEW
1.  **Summary Cards (Top of Dashboard)**
    *   Total Students
    *   Total Companies
    *   Current Placement Rate
    *   Total Opted Out
    *   Average CGPA (All Students)
    *   Average CGPA (Placed Students)

2.  **Student Data Table**
    *   Filterable by: Department, CGPA range, Domain, Placement Status
    *   Columns: Roll No, Name, Department, CGPA, Domain 1, Domain 2, Status, Company
    *   Pagination
    *   Export to CSV option

3.  **Company Data Table**
    *   Filterable by: Role Type, Day, Min/Max Hires
    *   Columns: Company, Role, Day, Min Hires, Max Hires, Domain, Eligibility
    *   Pagination
    *   Export to CSV option

#### SECTION B: STUDENT ANALYTICS

4.  **Department Distribution**
    *   **Pie Chart**: Student count by department
    *   **Bar Chart**: Department-wise student count (sorted)
    *   Interactive tooltips with percentages

5.  **CGPA Distribution**
    *   **Histogram**: CGPA distribution across all students
    *   **Box Plot**: CGPA distribution by department
    *   **Line Chart**: Cumulative CGPA distribution
    *   Filters: Department, Placement Status

6.  **Domain Preference Analysis**
    *   **Stacked Bar Chart**: Domain 1 vs Domain 2 preferences
    *   **Pie Chart**: Most popular domains
    *   **Heatmap**: Department × Domain matrix

7.  **Placement Status Overview**
    *   **Donut Chart**: Placed vs Unplaced vs Opted Out
    *   **Bar Chart**: Status by department
    *   Color-coded (Green: Placed, Red: Unplaced, Orange: Opted Out)

#### SECTION C: COMPANY ANALYTICS

8.  **Company Distribution**
    *   **Bar Chart**: Companies by hiring capacity (max_hires)
    *   **Pie Chart**: Companies by role type (SDE, Quant, Data, etc.)
    *   **Tree Map**: Company hierarchy by role

9.  **Role Type Analysis**
    *   **Stacked Bar Chart**: Min vs Max hires by role type
    *   **Donut Chart**: Role type distribution
    *   Filter by Day (Serial 1, Serial 2)

10. **Day-wise Company Distribution**
    *   **Grouped Bar Chart**: Serial 1 vs Serial 2 companies
    *   **Timeline View**: Company visit schedule

#### SECTION D: PLACEMENT RESULTS (After Simulation)

11. **Overall Placement Statistics**
    *   **KPI Cards**: 
        *   Total Placed
        *   Placement Rate %
        *   Companies that Hired
        *   Average Offers per Company
    *   **Gauge Chart**: Placement rate visualization

12. **Department-wise Placement Analysis**
    *   **Bar Chart**: Placement count by department
    *   **Horizontal Bar Chart**: Placement rate % by department
    *   **Grouped Bar Chart**: Placed vs Unplaced by department
    *   Color gradient based on placement rate

13. **Company-wise Hiring Results**
    *   **Bar Chart**: Students hired by each company
    *   **Stacked Bar Chart**: Min Required vs Actual Hires
    *   **Heat Map**: Company vs Department hiring matrix
    *   Filter: Show only companies that hired / all companies

14. **CGPA Analysis (Placed Students)**
    *   **Histogram**: CGPA distribution of placed students
    *   **Comparison Line Chart**: Placed vs Unplaced CGPA distribution
    *   **Box Plot**: CGPA by company
    *   **Scatter Plot**: CGPA vs Company (with department color coding)

15. **Department in Company Analysis**
    *   **Stacked Bar Chart**: For each company, show department breakdown
    *   **Heat Map**: Company × Department (cell value = student count)
    *   Interactive: Click company to see department distribution

16. **Role Type Success Analysis**
    *   **Pie Chart**: Placements by role type (SDE, Quant, Data, Finance, etc.)
    *   **Bar Chart**: Placement rate by role type
    *   **Funnel Chart**: Applications → Shortlists → Offers → Accepted

17. **Top Performers**
    *   **Table**: Top 20 companies by hiring
    *   **Table**: Top departments by placement rate
    *   **Table**: CGPA ranges with highest placement rates

18. **Opt-Out Analysis**
    *   **Pie Chart**: Opted out students by department
    *   **Bar Chart**: Opt-out rate by department
    *   **Timeline**: When students opted out (Serial 1 vs 2)

#### SECTION E: COMPARATIVE ANALYTICS

19. **Before vs After Simulation**
    *   **Side-by-side comparison**: Unplaced count before/after
    *   **Delta indicators**: Change in placement status
    *   **Progress bars**: Department-wise improvement

20. **Multiple Runs Comparison** (if multiple simulations run)
    *   **Line Chart**: Placement count across runs
    *   **Box Plot**: Variation in placement rate
    *   **Table**: Min/Max/Avg placements by company

21. **Capacity Utilization**
    *   **Gauge Chart**: For each company, show (Hired / Max Capacity)
    *   **Bar Chart**: Companies sorted by utilization %
    *   **Color coding**: Red (<50%), Yellow (50-80%), Green (>80%)

#### SECTION F: ADVANCED FILTERS & DRILL-DOWN

22. **Multi-dimensional Filters**
    *   Department (multi-select)
    *   CGPA Range (slider: 0-10)
    *   Role Type (multi-select)
    *   Placement Status (Placed/Unplaced/Opted Out)
    *   Company (multi-select)
    *   Domain (multi-select)
    *   Serial (Serial 1 / Serial 2 / Both)

23. **Drill-down Features**
    *   Click on any chart element to filter other charts
    *   Click department → show only that department's data across all charts
    *   Click company → show students placed in that company
    *   Click CGPA range → show students in that range

---

## 3. SIMULATION CONFIGURATION PANEL

#### Configuration Options:
```javascript
{
  // Score Weights (Profile Score)
  w1_cgpa: 0.3,
  w2_skill: 0.2,
  w3_random: 0.2,
  w4_dep_score: 0.3,
  
  // Score Weights (Interview Score)
  w5_profile: 0.3,
  w6_cgpa: 0.5,
  w7_random: 0.2,
  
  // Simulation Parameters
  p_opt_out: 0.05,
  random_seed: 42,
  
  // Over-offering Strategy
  over_offer_multiplier: 1.5,
  
  // Toggle Options
  use_dep_score: true,
  enforce_min_hires: true,
  
  // Run Configuration
  num_runs: 1  // For multiple runs
}
```

#### UI Elements:
*   **Sliders** for weight adjustments (0-1 range)
*   **Number inputs** for precise values
*   **Toggle switches** for boolean options
*   **Dropdown** for preset configurations
*   **Reset to Default** button
*   **Save Configuration** button
*   **Load Configuration** button

#### Run Simulation Button:
*   Large, prominent button
*   Shows loading spinner during execution
*   Progress indicator
*   Estimated time remaining
*   Cancel option for long runs

---

## 4. PAGE LAYOUT STRUCTURE

```
┌─────────────────────────────────────────────────────────┐
│                    HEADER / NAVBAR                      │
│  Logo | Dashboard | Data | Configuration | Results     │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   SUMMARY CARDS (6)                     │
│  [Students] [Companies] [Placement%] [Opted Out] [...] │
└─────────────────────────────────────────────────────────┘
┌──────────────────┬──────────────────────────────────────┐
│                  │                                      │
│    SIDEBAR       │        MAIN CONTENT AREA             │
│    FILTERS       │                                      │
│                  │   ┌──────────────┬──────────────┐   │
│  - Department    │   │   Chart 1    │   Chart 2    │   │
│  - CGPA Range    │   └──────────────┴──────────────┘   │
│  - Role Type     │   ┌──────────────┬──────────────┐   │
│  - Status        │   │   Chart 3    │   Chart 4    │   │
│  - Company       │   └──────────────┴──────────────┘   │
│                  │   ┌────────────────────────────┐   │
│  [Apply Filter]  │   │      Data Table            │   │
│  [Reset]         │   └────────────────────────────┘   │
│                  │                                      │
└──────────────────┴──────────────────────────────────────┘
```

---

## 5. FASTAPI BACKEND ENDPOINTS

```python
# Data Endpoints
GET  /api/students              # Get all students with filters
GET  /api/companies             # Get all companies with filters
GET  /api/departments           # Get department list
GET  /api/domains               # Get domain list

# Analytics Endpoints
GET  /api/stats/summary         # Overall summary statistics
GET  /api/stats/department      # Department-wise stats
GET  /api/stats/cgpa            # CGPA distribution
GET  /api/stats/companies       # Company statistics

# Simulation Endpoints
POST /api/simulation/config     # Save configuration
GET  /api/simulation/config     # Get current configuration
POST /api/simulation/run        # Run simulation
GET  /api/simulation/status     # Check simulation status
GET  /api/simulation/results    # Get simulation results

# Results Endpoints
GET  /api/results/placements    # Placement results
GET  /api/results/company-wise  # Company-wise hiring
GET  /api/results/dept-wise     # Department-wise placements
GET  /api/results/comparison    # Before/after comparison

# Export Endpoints
GET  /api/export/csv            # Export results to CSV
GET  /api/export/pdf            # Export dashboard as PDF
```

---

## 6. TECHNOLOGY STACK

**Frontend:**
*   HTML5, CSS3, JavaScript (ES6+)
*   **Chart Library**: Chart.js (lightweight, versatile)
*   **Alternative**: D3.js (for advanced visualizations)
*   **UI Framework**: Bootstrap 5 or Tailwind CSS
*   **Icons**: Font Awesome
*   **Tables**: DataTables.js (for advanced table features)

**Backend:**
*   FastAPI (Python)
*   Pandas (data processing)
*   NumPy (calculations)
*   Uvicorn (ASGI server)

**Data Storage:**
*   CSV files (current)
*   Optional: SQLite for faster queries

---

## 7. INTERACTIVE FEATURES

1.  **Real-time Updates**: Charts update as filters change
2.  **Responsive Design**: Works on desktop, tablet, mobile
3.  **Dark Mode Toggle**: Switch between light/dark themes
4.  **Export Options**: Download charts as PNG, data as CSV
5.  **Tooltips**: Hover over charts for detailed info
6.  **Drill-down**: Click to filter across all visualizations
7.  **Comparison Mode**: Compare multiple simulation runs
8.  **Search**: Quick search for students/companies
9.  **Bookmarks**: Save favorite filter combinations
10. **Notifications**: Toast messages for simulation completion

---

## 8. COMPLETE VISUALIZATION LIST

| # | Visualization | Type | Section |
|---|---------------|------|---------|
| 1 | Summary KPIs | Cards | Overview |
| 2 | Student Table | DataTable | Data |
| 3 | Company Table | DataTable | Data |
| 4 | Department Distribution | Pie + Bar | Student Analytics |
| 5 | CGPA Distribution | Histogram | Student Analytics |
| 6 | CGPA by Department | Box Plot | Student Analytics |
| 7 | Domain Preferences | Stacked Bar | Student Analytics |
| 8 | Placement Status | Donut | Student Analytics |
| 9 | Company by Capacity | Bar Chart | Company Analytics |
| 10 | Role Type Distribution | Pie Chart | Company Analytics |
| 11 | Day-wise Companies | Grouped Bar | Company Analytics |
| 12 | Placement Rate Gauge | Gauge Chart | Results |
| 13 | Dept-wise Placements | Bar Chart | Results |
| 14 | Company Hiring | Bar Chart | Results |
| 15 | Company × Department | Heat Map | Results |
| 16 | CGPA Comparison | Line Chart | Results |
| 17 | Department Breakdown | Stacked Bar | Results |
| 18 | Role Success Rate | Funnel Chart | Results |
| 19 | Top Performers | Tables | Results |
| 20 | Capacity Utilization | Gauge Array | Results |
| 21 | Multiple Runs Comparison | Line + Box | Comparative |
| 22 | Before/After | Side-by-side | Comparative |

---

## 9. IMPLEMENTATION PRIORITY

**Phase 1 (MVP):**
*   Basic dashboard layout
*   Summary cards
*   Student/Company tables
*   Department & CGPA charts
*   Simulation configuration panel
*   Run simulation button
*   Basic results display

**Phase 2:**
*   Advanced filters
*   Company-wise analysis
*   Heat maps
*   Drill-down features
*   Export functionality

**Phase 3:**
*   Multiple runs comparison
*   Advanced analytics
*   Dark mode
*   PDF export
*   Mobile optimization
