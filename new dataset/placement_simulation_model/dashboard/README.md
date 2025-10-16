# 📊 Placement Simulation Dashboard

A beautiful, interactive web dashboard for visualizing and running placement simulations. Built with FastAPI backend and modern HTML/CSS/JavaScript frontend with Chart.js for data visualizations.

![Dashboard Preview](https://img.shields.io/badge/Status-Ready-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)

## ✨ Features

### 📈 Data Visualization
- **Interactive Charts**: Real-time data visualization using Chart.js
- **Department Analytics**: Department-wise student and placement distribution
- **CGPA Analysis**: CGPA distribution across departments and placement status
- **Company Insights**: Company hiring capacity, role types, and day-wise distribution
- **Domain Preferences**: Student domain preference analysis

### 🎮 Simulation Control
- **Configurable Parameters**: Adjust score weights, opt-out probability, and more
- **Real-time Progress**: Live progress tracking during simulation execution
- **Multiple Configurations**: Save and load different simulation configurations
- **Background Processing**: Simulations run asynchronously without blocking UI

### 📊 Results Analysis
- **Placement Statistics**: Comprehensive placement rate and success metrics
- **Company-wise Hiring**: Top recruiting companies and utilization rates
- **Department Performance**: Department-wise placement success
- **CGPA Correlation**: Analyze CGPA impact on placement success

### 🎨 User Interface
- **Modern Design**: Clean, professional interface with gradient accents
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Interactive Tables**: Sortable, filterable data tables with pagination
- **Toast Notifications**: Real-time feedback on actions

## 📁 Project Structure

```
dashboard/
├── main.py                     # FastAPI backend server
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── static/                     # Frontend files
    ├── index.html              # Main dashboard HTML
    ├── css/
    │   └── styles.css          # Dashboard styling
    └── js/
        └── app.js              # Dashboard JavaScript
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Navigate to the dashboard directory:**
   ```powershell
   cd "a:\Documents\cdc-simu\new dataset\placement_simulation_model\dashboard"
   ```

2. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Dashboard

1. **Start the FastAPI server:**
   ```powershell
   python main.py
   ```

   Or use uvicorn directly:
   ```powershell
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:8000
   ```

3. **The dashboard will load automatically!**

## 📖 Usage Guide

### Overview Section
- **Summary Cards**: View key metrics (students, companies, placement rate, CGPA)
- **Charts**: Visualize department distribution, CGPA, domains, and placement status
- Quick snapshot of the entire dataset

### Students Section
- **Filters**: Filter students by department, CGPA range, and status
- **Data Table**: Browse all students with pagination
- **Analytics**: Department-wise placement and CGPA analysis
- **Export**: Download filtered data as CSV

### Companies Section
- **Company List**: View all companies with their requirements
- **Role Analysis**: See distribution by role types
- **Day Distribution**: Understand company visit schedule
- **Capacity Insights**: Analyze hiring capacity metrics

### Configuration Section
- **Score Weights**: Adjust profile and interview score weights
  - W1-W4: Profile score components (CGPA, Skills, Random, Dept Score)
  - W5-W7: Interview score components (Profile, CGPA, Random)
- **Parameters**: Set opt-out probability and over-offer multiplier
- **Options**: Enable/disable department score and minimum hire enforcement
- **Run Simulation**: Execute simulation with configured parameters

### Results Section
- **Summary Stats**: Total placed, success rate, companies hired
- **Charts**: Visualize placement by department, company, and role
- **Top Performers**: See top recruiting companies with utilization rates
- Only available after running a simulation

## 🔧 Configuration Options

### Score Weights (Profile Score)
- **W1 - CGPA Weight** (default: 0.3): Weight for CGPA in profile evaluation
- **W2 - Skill Weight** (default: 0.2): Weight for skill match
- **W3 - Random Weight** (default: 0.2): Random factor for variability
- **W4 - Dept Score Weight** (default: 0.3): Department reputation weight

### Score Weights (Interview Score)
- **W5 - Profile Weight** (default: 0.3): Weight for profile score in interview
- **W6 - CGPA Weight** (default: 0.5): Weight for CGPA in interview
- **W7 - Random Weight** (default: 0.2): Random factor in interview

### Simulation Parameters
- **Opt-out Probability** (default: 0.05): Chance of student opting out
- **Random Seed** (default: 42): Seed for reproducible results
- **Over-offer Multiplier** (default: 1.5): Factor for over-offering

### Options
- **Use Department Score**: Include department reputation in calculations
- **Enforce Minimum Hires**: Ensure companies meet minimum hiring requirements

## 🎨 Theme Support

The dashboard supports both light and dark modes:
- Click the moon/sun icon in the header to toggle themes
- Theme preference is saved in browser local storage
- Automatic theme persistence across sessions

## 📊 API Endpoints

The FastAPI backend provides the following REST API endpoints:

### Data Endpoints
- `GET /api/students` - Get students with filters
- `GET /api/companies` - Get companies with filters
- `GET /api/departments` - Get list of departments
- `GET /api/domains` - Get list of domains

### Statistics Endpoints
- `GET /api/stats/summary` - Overall summary statistics
- `GET /api/stats/department` - Department-wise statistics
- `GET /api/stats/cgpa` - CGPA distribution
- `GET /api/stats/companies` - Company statistics
- `GET /api/stats/domain` - Domain preference statistics

### Simulation Endpoints
- `POST /api/simulation/run` - Run simulation with config
- `GET /api/simulation/status` - Check simulation status
- `GET /api/simulation/results` - Get simulation results

### Results Endpoints
- `GET /api/results/placements` - Placement results
- `GET /api/results/company-wise` - Company-wise hiring

### Export Endpoints
- `GET /api/export/csv` - Export results to CSV

## 🔍 Troubleshooting

### Port Already in Use
If port 8000 is already in use:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```
Then access at `http://localhost:8080`

### CORS Errors
If you encounter CORS errors, ensure:
- Backend is running on the expected port
- Update `API_BASE` in `static/js/app.js` if using different port
- Browser allows localhost connections

### Module Not Found
If Python modules are not found:
```powershell
pip install -r requirements.txt --upgrade
```

### Data Files Not Found
Ensure the following files exist in the parent directory:
- `analysis_data.csv` (student data)
- `companies.csv` (company data)
- `company_order.csv` (company visit order)
- `company shortlists(csv)/` folder with shortlist files

## 🎯 Features Implemented

### Phase 1 (MVP) ✅
- [x] Basic dashboard layout with navigation
- [x] Summary cards with key metrics
- [x] Student and company data tables
- [x] Department & CGPA distribution charts
- [x] Simulation configuration panel
- [x] Run simulation with progress tracking
- [x] Basic results display

### Phase 2 ✅
- [x] Advanced filters for students
- [x] Company-wise analysis charts
- [x] Domain preference heatmap
- [x] Drill-down features
- [x] CSV export functionality
- [x] Dark mode support

### Phase 3 (Future Enhancements) 🚧
- [ ] Multiple simulation runs comparison
- [ ] PDF export for reports
- [ ] Advanced analytics dashboards
- [ ] Predictive modeling features
- [ ] Mobile app version

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Uvicorn**: ASGI server for FastAPI

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with custom properties
- **JavaScript (ES6+)**: Interactive functionality
- **Chart.js**: Data visualization library
- **Font Awesome**: Icon library

### Architecture
- RESTful API design
- Async/await patterns
- Background task processing
- Responsive grid layout
- Component-based structure

## 📝 Notes

- Simulation runs asynchronously in the background
- Progress is updated in real-time via polling
- Results are cached after simulation completion
- All charts are interactive and responsive
- Dark mode preference persists across sessions

## 🤝 Contributing

This dashboard was built following the specifications in `DASHBOARD_PLAN.md`. For enhancements or bug fixes:

1. Test changes locally
2. Ensure backward compatibility
3. Update documentation
4. Follow existing code style

## 📄 License

Part of the CDC Placement Simulation project.

## 🎓 Credits

Created for: CDC Placement Simulation
Date: October 2025
Version: 1.0.0

---

**Enjoy the Dashboard! 🚀**

For questions or issues, refer to the main simulation README or contact the development team.
