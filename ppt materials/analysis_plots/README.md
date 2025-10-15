# Placement Data Analysis - Visualization Summary

## 📁 Generated Files

This folder contains comprehensive visualizations analyzing the 2023-24 placement season data.

### File Formats
- **HTML files**: Interactive visualizations (hover for details, zoom, pan)
- **PNG files**: Static images for presentations and reports

---

## 📊 Available Visualizations

### 1. **plot_1_departmental_performance** 
**The Landscape: Departmental Performance**
- **Type**: Grouped Bar Chart
- **Shows**: Total students vs. Placed students by department
- **Key Metric**: Placement Rate (%) for each department
- **Use Case**: Identify high-performing and struggling departments

### 2. **plot_2_cgpa_distribution**
**CGPA Distribution Analysis**
- **Type**: Multi-panel (Histogram, Box Plots, Bar Charts)
- **Shows**: 
  - Overall CGPA distribution (truncated normal)
  - CGPA distribution by department
  - Students with CGPA ≥ 9.0 by department
  - Average CGPA by department
- **Key Insight**: Which departments have most high performers (9+ CGPA)
- **Use Case**: Understanding academic excellence patterns

### 3. **plot_3_department_domain_heatmap**
**Department × Domain Matrix**
- **Type**: Heatmap
- **Shows**: Distribution of domain preferences across departments
- **Key Insight**: Cross-domain transitions and career preferences
- **Use Case**: Understanding which departments feed into which job domains

### 4. **plot_4_companies_per_day**
**Placement Timeline: Company Arrivals**
- **Type**: Bar Chart with Trend Line
- **Shows**: Number of companies arriving each day (Day 1-4)
- **Key Insight**: Placement activity intensity across days
- **Use Case**: Strategic planning for placement week

### 5. **plot_5_kpi_cards**
**Key Performance Indicators Dashboard**
- **Type**: KPI Cards/Indicators
- **Shows**: 
  - Total Students Participating
  - Total Students Placed
  - Overall Placement Rate (%)
- **Key Insight**: At-a-glance placement success metrics
- **Use Case**: Executive summary and stakeholder reporting

### 6. **plot_6_placement_comparison**
**Departmental Placement Analysis**
- **Type**: Dual visualization (Horizontal Bar + Grouped Bar)
- **Shows**:
  - Placement Rate % by department (horizontal bars)
  - Placed vs. Unplaced students by department (grouped bars)
- **Key Insight**: Both relative success (%) and absolute impact (numbers)
- **Use Case**: Comprehensive departmental comparison

### 7. **plot_7_cgpa_boxplot**
**CGPA Distribution Across All Departments**
- **Type**: Box Plots
- **Shows**: Statistical distribution (median, quartiles, outliers) for each department
- **Key Insight**: CGPA variance and consistency across departments
- **Use Case**: Understanding grade distributions and departmental academic patterns

---

## 📈 Key Findings

### Overall Metrics
- **Total Students Analyzed**: 1,235
- **Overall Placement Rate**: 21.62%
- **Total Departments**: 22
- **Total Companies**: 79
- **Placement Days**: 4 (Day 1-4)

### Quick Insights
1. **Top Performing Departments**: Computer Science, Mathematics, Electronics typically show highest placement rates
2. **CGPA Distribution**: Follows truncated normal distribution with most students in 7.0-8.5 range
3. **Domain Preferences**: Strong migration from non-CS departments to SDE roles
4. **Company Clustering**: Day 1 sees maximum company arrivals (premium companies)
5. **High Performers**: CS and MA departments dominate the 9+ CGPA bracket

---

## 🔍 How to Use These Visualizations

### For Presentations
1. Use **PNG files** for PowerPoint/PDF presentations
2. Files are high-resolution (1400-1600px wide) for clear projection
3. Each plot has descriptive titles and annotations

### For Interactive Analysis
1. Open **HTML files** in any web browser
2. Hover over data points for detailed information
3. Zoom and pan for detailed exploration
4. Download customized views directly from the plot

### For Reports
1. Reference plots by number and name
2. See `PLACEMENT_ANALYSIS_REPORT.md` for detailed interpretation
3. Combine multiple plots for comprehensive storytelling

---

## 📖 Detailed Analysis

For in-depth interpretation of each visualization, including:
- Statistical methodology
- Key patterns and trends
- Strategic recommendations
- Stakeholder-specific insights

**👉 See: `PLACEMENT_ANALYSIS_REPORT.md`** in the parent directory

---

## 🛠️ Technical Details

### Libraries Used
- **Plotly**: Interactive visualizations
- **Pandas**: Data processing and analysis
- **NumPy**: Numerical computations

### Data Sources
- `analysis_data.csv` - Student profiles and academic data
- `outcomes_4_year.csv` - Placement results (Day 1-4)
- `companies.csv` - Company recruitment information
- `dep_names.csv` - Department mappings
- `domain.csv` - Domain and skill definitions

### Generation Script
- **Script**: `generate_analysis_plots.py`
- **Language**: Python 3.x
- **Reproducible**: Run script to regenerate all plots

---

## 📝 Notes

### Color Coding
- 🟢 **Green**: Placed students, high performance, success metrics
- 🔴 **Red**: Unplaced students, areas needing improvement
- 🔵 **Blue**: Information, neutral metrics
- 🟡 **Yellow/Orange**: Warning zones, moderate performance

### Best Practices
1. **Always cite the data source** when using these visualizations
2. **Check timestamps** - data represents placement through Day 4 only
3. **Consider context** - placement rates can vary by year and market conditions
4. **Holistic interpretation** - combine multiple plots for complete understanding

---

## 🔄 Updates and Maintenance

To regenerate plots with updated data:
```bash
cd "c:\Users\nigam\Desktop\Simulation 2nd Presentation\ppt materials"
python generate_analysis_plots.py
```

Ensure all CSV data files are up-to-date before regeneration.

---

## 📞 Questions or Issues?

For questions about:
- **Data interpretation**: Refer to `PLACEMENT_ANALYSIS_REPORT.md`
- **Technical issues**: Check script comments in `generate_analysis_plots.py`
- **Custom visualizations**: Modify the generation script as needed

---

*Generated: October 2025*  
*Analysis Period: 2023-24 Placement Season (Day 1-4)*
