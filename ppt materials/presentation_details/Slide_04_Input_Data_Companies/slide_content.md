# Slide 4: Input Data Analysis - Companies & Recruitment Timeline

## Slide Title
**Company Recruitment Patterns & Timeline Analysis**

---

## Main Content Structure

### Section 1: Company Dataset Overview (Left Side)

**Visual Reference:** Use `plot_4_companies_per_day.png` from analysis_plots folder

**Key Statistics Box:**
```
📊 COMPANY DATASET
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Companies:        79
Unique Roles:          36
Role Categories:       SDE, Data, Quant, 
                      Consulting, Core
Recruitment Days:      4 days
Serial Scheduling:     Yes
```

### Section 2: Recruitment Timeline Breakdown (Right Side)

**Mermaid Diagram - Daily Distribution:**
```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'fontSize':'16px'}}}%%
graph LR
    A[Day 1<br/>Premium Tier<br/>30-35%] --> B[Day 2<br/>Strong Tier<br/>25-30%]
    B --> C[Day 3<br/>Mid Tier<br/>20-25%]
    C --> D[Day 4<br/>Final Round<br/>10-15%]
    
    style A fill:#2E7D32,color:#fff,stroke:#1B5E20
    style B fill:#1976D2,color:#fff,stroke:#0D47A1
    style C fill:#F57C00,color:#fff,stroke:#E65100
    style D fill:#C62828,color:#fff,stroke:#B71C1C
```

### Section 3: Role Type Distribution

**Data Visualization Table:**
```
┌──────────────────┬──────────┬─────────────┐
│ Domain           │ Companies│ % of Total  │
├──────────────────┼──────────┼─────────────┤
│ SDE (Software)   │    28    │    35.4%    │
│ Data Science     │    18    │    22.8%    │
│ Quant/Finance    │    12    │    15.2%    │
│ Consulting       │     9    │    11.4%    │
│ Core Engineering │     8    │    10.1%    │
│ Other            │     4    │     5.1%    │
└──────────────────┴──────────┴─────────────┘
```

### Section 4: Hiring Capacity Insights

**Key Metrics:**
- **Average Min Requirement:** 3-5 students per company
- **Average Max Capacity:** 8-12 students per company
- **Over-Offering Strategy:** 1.5x multiplier (offer 15 to fill 10 positions)
- **Acceptance Rate Assumption:** ~67% of offers accepted

---

## Visual Design Specifications

### Color Scheme
- **Premium Companies (Day 1):** Dark Green (#2E7D32)
- **Strong Companies (Day 2):** Blue (#1976D2)
- **Mid-Tier (Day 3):** Orange (#F57C00)
- **Final Round (Day 4):** Red (#C62828)
- **Background:** White with light gray accents (#F5F5F5)

### Layout Recommendations
```
┌─────────────────────────────────────────────────────┐
│  SLIDE TITLE                                        │
├──────────────────────┬──────────────────────────────┤
│                      │                              │
│  [PLOT 4 IMAGE]      │   Daily Distribution        │
│  Companies Per Day   │   [Mermaid Diagram]         │
│                      │                              │
│  Company Stats Box   │   Role Distribution Table   │
│                      │                              │
├──────────────────────┴──────────────────────────────┤
│  Hiring Capacity Insights (Bottom Banner)          │
└─────────────────────────────────────────────────────┘
```

### Typography
- **Title:** Montserrat Bold, 44pt
- **Section Headers:** Montserrat SemiBold, 28pt
- **Body Text:** Open Sans Regular, 20pt
- **Statistics:** Roboto Mono, 18pt (for numbers)

---

## Speaker Notes (2 minutes)

### Opening (15 seconds)
"Moving to our company data, we have 79 companies participating across 4 recruitment days. This slide shows how companies are strategically distributed across the placement timeline."

### Main Points (1 minute 15 seconds)

**Point 1 - Recruitment Timeline (25 seconds):**
"Notice the concentration on Days 1 and 2 - that's where 55-65% of all companies arrive. These are your premium and strong-tier companies like Google, Microsoft, Goldman Sachs. Day 1 is the most competitive - students face multiple interviews on the same day, creating both opportunity and pressure."

**Point 2 - Role Distribution (25 seconds):**
"The role breakdown reveals the market reality: Software Development dominates with 35% of companies, followed by Data Science at 23% and Quantitative roles at 15%. This explains why students from all departments are pivoting towards these skills - the opportunities are there."

**Point 3 - Hiring Strategy (25 seconds):**
"Companies use an over-offering strategy - they make 1.5 times more offers than positions because historically only 67% of offers are accepted. Students wait for better opportunities or decline for various reasons. This is built into our simulation model."

### Transition (15 seconds)
"Now that we understand the company landscape, let's look at the patterns that emerge when students and companies interact in our dataset."

### Key Talking Points
- ✅ Strategic scheduling creates natural competition tiers
- ✅ Software/tech roles dominate the placement landscape
- ✅ Over-offering is a necessary business strategy
- ✅ Serial scheduling prevents interview conflicts

---

## Backup Information / Q&A Preparation

### Potential Question 1: "Why serial scheduling?"
**Answer:** "Serial scheduling means companies don't interview simultaneously. This prevents students from missing opportunities due to time conflicts. In our model, companies arrive in a sequence, and students can participate in all tests and interviews for which they're eligible without scheduling conflicts."

### Potential Question 2: "How do you model Day 1 vs Day 4 differently?"
**Answer:** "Great question! The model doesn't explicitly treat days differently in terms of selection criteria, but the student behavior changes. Day 1 unplaced students become more flexible in their domain preferences by Day 3-4. Also, our acceptance probability adjusts based on when the offer arrives."

### Potential Question 3: "What about companies that recruit for multiple roles?"
**Answer:** "We handle that with separate company-role combinations. For example, Amazon appears multiple times in our dataset - once for SDE, once for Data Science. Each role has its own requirements and capacity."

### Potential Question 4: "Is the 1.5x over-offering realistic?"
**Answer:** "It's based on historical data from actual placement seasons. Some premium companies use 1.3x, mid-tier might use 1.7x. We use 1.5x as a reasonable average. This is a configurable parameter in our simulation."

---

## Additional Data Points (For Handout/Backup Slides)

### Top 10 Companies by Hiring Capacity
1. Amazon (SDE) - 15 positions
2. Microsoft - 12 positions
3. Google - 10 positions
4. Goldman Sachs (SDE) - 10 positions
5. Accenture (Consulting) - 14 positions
6. Adobe (Product) - 8 positions
7. Oracle - 10 positions
8. Qualcomm - 9 positions
9. DE Shaw (Quant) - 6 positions
10. Databricks - 7 positions

### Company Arrival Pattern
- **Day 1 (Premium):** Google, Microsoft, Adobe, Goldman Sachs, DE Shaw, Optiver
- **Day 2 (Strong):** Amazon, Qualcomm, Oracle, Salesforce, Nvidia
- **Day 3 (Mid-Tier):** Accenture, Infosys, Wipro, TCS, Various core companies
- **Day 4 (Final):** Startups, niche companies, regional players

### Domain-Specific Company Insights
- **Quant/Finance:** Highly selective, typically 2-4 positions, require >8.5 CGPA, Math/CS preference
- **SDE Roles:** Largest pool, 3-15 positions per company, skill-focused evaluation
- **Data Science:** Growing demand, 4-8 positions typical, cross-department recruiting
- **Core Engineering:** Variable demand, geography-dependent, 5-10 positions

---

## Timing Checkpoint
- **Cumulative Time:** 10 minutes (Slides 1-4)
- **Remaining Time:** 0-5 minutes for Slides 5-6
- **Pacing Status:** On track, slight compression needed for final slides

---

## Technical Notes for Slide Design

### Image Placement
1. Import `plot_4_companies_per_day.png` from `analysis_plots` folder
2. Resize to fit left half of slide (maintain aspect ratio)
3. Add subtle shadow for depth (3px blur, 20% opacity)

### Animation Suggestions (if using PowerPoint)
1. **Company Stats Box:** Fade in (0.5s delay)
2. **Mermaid Diagram:** Appear in sequence (Day 1 → Day 2 → Day 3 → Day 4)
3. **Role Distribution Table:** Wipe from left (0.3s per row)
4. **Hiring Insights:** Fade in last (after all other elements)

### Accessibility Notes
- Ensure color contrast ratios meet WCAG AA standards
- Provide alt text for the plot image: "Bar chart showing distribution of companies across 4 recruitment days"
- Use patterns in addition to colors if printing in grayscale

---

## Cross-Reference to Other Slides
- **Links to Slide 3:** Student domain preferences (Slide 3) align with company role distribution (this slide)
- **Links to Slide 5:** Patterns emerge from the mismatch between student aspirations and company availability
- **Links to Slide 6:** This company structure feeds into the simulation model's scheduling and matching algorithms

---

*Slide 4 Content Complete | Estimated Presentation Time: 2 minutes*
