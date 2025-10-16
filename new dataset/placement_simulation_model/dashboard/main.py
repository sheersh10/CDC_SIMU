"""
Placement Simulation Dashboard - FastAPI Backend
Provides REST API endpoints for the interactive dashboard
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import pandas as pd
import numpy as np
import json
import sys
import os
from pathlib import Path
from datetime import datetime
import asyncio

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from placement_simulation import *
from run_simulation import PlacementSimulation

# Initialize FastAPI app
app = FastAPI(title="Placement Simulation Dashboard", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Global variables
BASE_DIR = Path(__file__).parent.parent.parent
STUDENTS_FILE = BASE_DIR / "analysis_data.csv"
COMPANIES_FILE = BASE_DIR / "companies.csv"
SHORTLIST_DIR = BASE_DIR / "company shortlists(csv)"
COMPANY_ORDER_FILE = BASE_DIR / "company_order.csv"

# Simulation state
simulation_state = {
    "status": "idle",  # idle, running, completed, error
    "progress": 0,
    "message": "",
    "results": None,
    "students_data": None,
    "companies_data": None,
    "simulation_instance": None
}

# Data models
class SimulationConfig(BaseModel):
    w1_cgpa: float = 0.3
    w2_skill: float = 0.2
    w3_random: float = 0.2
    w4_dep_score: float = 0.3
    w5_profile: float = 0.3
    w6_cgpa_interview: float = 0.5
    w7_random_interview: float = 0.2
    p_opt_out: float = 0.05
    random_seed: int = 42
    over_offer_multiplier: float = 1.5
    use_dep_score: bool = True
    enforce_min_hires: bool = True

class FilterParams(BaseModel):
    departments: Optional[List[str]] = None
    cgpa_min: Optional[float] = None
    cgpa_max: Optional[float] = None
    domains: Optional[List[str]] = None
    status: Optional[str] = None
    role_types: Optional[List[str]] = None
    days: Optional[List[int]] = None

# Helper functions
def load_initial_data():
    """Load all initial data"""
    try:
        students_df = pd.read_csv(STUDENTS_FILE)
        companies_df = pd.read_csv(COMPANIES_FILE)
        
        # Clean string 'nan' values in all string columns
        for col in students_df.columns:
            if students_df[col].dtype == 'object':
                students_df[col] = students_df[col].replace('nan', None)
                students_df[col] = students_df[col].replace('NaN', None)
        
        for col in companies_df.columns:
            if companies_df[col].dtype == 'object':
                companies_df[col] = companies_df[col].replace('nan', None)
                companies_df[col] = companies_df[col].replace('NaN', None)
        
        # Add status column if not exists
        if 'status' not in students_df.columns:
            students_df['status'] = 'Unplaced'
        if 'placed_company' not in students_df.columns:
            students_df['placed_company'] = ''
            
        # Extract department code from roll number
        students_df['department'] = students_df['roll_no'].str[2:4]
        
        simulation_state["students_data"] = students_df
        simulation_state["companies_data"] = companies_df
        
        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def apply_filters(df, filters: FilterParams):
    """Apply filters to dataframe"""
    filtered_df = df.copy()
    
    if filters.departments and len(filters.departments) > 0:
        filtered_df = filtered_df[filtered_df['department'].isin(filters.departments)]
    
    if filters.cgpa_min is not None:
        filtered_df = filtered_df[filtered_df['cgpa'] >= filters.cgpa_min]
    
    if filters.cgpa_max is not None:
        filtered_df = filtered_df[filtered_df['cgpa'] <= filters.cgpa_max]
    
    if filters.domains and len(filters.domains) > 0:
        filtered_df = filtered_df[
            filtered_df['domain_1'].isin(filters.domains) | 
            filtered_df['domain_2'].isin(filters.domains)
        ]
    
    if filters.status:
        filtered_df = filtered_df[filtered_df['status'] == filters.status]
    
    return filtered_df

# API Endpoints

@app.get("/")
async def root():
    """Serve the main dashboard HTML"""
    return FileResponse(Path(__file__).parent / "static" / "index.html")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/data/load")
async def load_data():
    """Load initial data"""
    success = load_initial_data()
    if success:
        return {"status": "success", "message": "Data loaded successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to load data")

@app.get("/api/students")
async def get_students(
    department: Optional[str] = None,
    cgpa_min: Optional[float] = None,
    cgpa_max: Optional[float] = None,
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """Get students with optional filters"""
    if simulation_state["students_data"] is None:
        load_initial_data()
    
    df = simulation_state["students_data"].copy()
    
    # Apply filters
    if department:
        df = df[df['department'] == department]
    if cgpa_min is not None:
        df = df[df['cgpa'] >= cgpa_min]
    if cgpa_max is not None:
        df = df[df['cgpa'] <= cgpa_max]
    if status:
        df = df[df['status'] == status]
    
    # Pagination
    total = len(df)
    df = df.iloc[offset:offset+limit]
    
    # Replace NaN and inf values with None for JSON serialization
    df = df.replace([np.nan, np.inf, -np.inf], None)
    
    # Also replace string 'nan' with None
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].replace('nan', None)
            df[col] = df[col].replace('NaN', None)
    
    return {
        "data": df.to_dict(orient='records'),
        "total": total,
        "limit": limit,
        "offset": offset
    }

@app.get("/api/companies")
async def get_companies(
    role: Optional[str] = None,
    day: Optional[int] = None,
    limit: int = 100,
    offset: int = 0
):
    """Get companies with optional filters"""
    if simulation_state["companies_data"] is None:
        load_initial_data()
    
    df = simulation_state["companies_data"].copy()
    
    # Apply filters
    if role:
        df = df[df['job_role'].str.contains(role, case=False, na=False)]
    if day is not None:
        df = df[df['arrival_day'] == day]
    
    # Pagination
    total = len(df)
    df = df.iloc[offset:offset+limit]
    
    # Replace NaN and inf values with None for JSON serialization
    df = df.replace([np.nan, np.inf, -np.inf], None)
    
    # Also replace string 'nan' with None
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].replace('nan', None)
            df[col] = df[col].replace('NaN', None)
    
    return {
        "data": df.to_dict(orient='records'),
        "total": total,
        "limit": limit,
        "offset": offset
    }

@app.get("/api/departments")
async def get_departments():
    """Get list of all departments"""
    if simulation_state["students_data"] is None:
        load_initial_data()
    
    departments = sorted(simulation_state["students_data"]['department'].unique().tolist())
    return {"departments": departments}

@app.get("/api/domains")
async def get_domains():
    """Get list of all domains"""
    if simulation_state["students_data"] is None:
        load_initial_data()
    
    df = simulation_state["students_data"]
    domains = set()
    domains.update(df['domain_1'].dropna().unique())
    domains.update(df['domain_2'].dropna().unique())
    
    return {"domains": sorted(list(domains))}

@app.get("/api/stats/summary")
async def get_summary_stats():
    """Get overall summary statistics"""
    if simulation_state["students_data"] is None:
        load_initial_data()
    
    students_df = simulation_state["students_data"]
    companies_df = simulation_state["companies_data"]
    
    # Calculate statistics
    total_students = len(students_df)
    total_companies = len(companies_df)
    
    placed_students = len(students_df[students_df['status'] == 'Placed'])
    unplaced_students = len(students_df[students_df['status'] == 'Unplaced'])
    opted_out = len(students_df[students_df['status'] == 'Opted_Out'])
    
    placement_rate = (placed_students / total_students * 100) if total_students > 0 else 0
    
    avg_cgpa_all = students_df['cgpa'].mean()
    avg_cgpa_placed = students_df[students_df['status'] == 'Placed']['cgpa'].mean() if placed_students > 0 else 0
    
    total_positions = companies_df['max_offers'].sum()
    min_positions = companies_df['min_offers'].sum()
    
    # Handle NaN values
    avg_cgpa_all = 0 if pd.isna(avg_cgpa_all) else avg_cgpa_all
    avg_cgpa_placed = 0 if pd.isna(avg_cgpa_placed) else avg_cgpa_placed
    
    return {
        "total_students": int(total_students),
        "total_companies": int(total_companies),
        "placed_students": int(placed_students),
        "unplaced_students": int(unplaced_students),
        "opted_out": int(opted_out),
        "placement_rate": round(placement_rate, 2),
        "avg_cgpa_all": round(avg_cgpa_all, 2),
        "avg_cgpa_placed": round(avg_cgpa_placed, 2),
        "total_positions": int(total_positions),
        "min_positions": int(min_positions)
    }

@app.get("/api/stats/department")
async def get_department_stats():
    """Get department-wise statistics"""
    if simulation_state["students_data"] is None:
        load_initial_data()
    
    df = simulation_state["students_data"]
    
    # Group by department
    dept_stats = []
    for dept in df['department'].unique():
        dept_df = df[df['department'] == dept]
        total = len(dept_df)
        placed = len(dept_df[dept_df['status'] == 'Placed'])
        unplaced = len(dept_df[dept_df['status'] == 'Unplaced'])
        opted_out = len(dept_df[dept_df['status'] == 'Opted_Out'])
        avg_cgpa = dept_df['cgpa'].mean()
        placement_rate = (placed / total * 100) if total > 0 else 0
        
        # Handle NaN values
        avg_cgpa = 0 if pd.isna(avg_cgpa) else avg_cgpa
        
        dept_stats.append({
            "department": dept,
            "total": int(total),
            "placed": int(placed),
            "unplaced": int(unplaced),
            "opted_out": int(opted_out),
            "avg_cgpa": round(avg_cgpa, 2),
            "placement_rate": round(placement_rate, 2)
        })
    
    # Sort by placement rate
    dept_stats.sort(key=lambda x: x['placement_rate'], reverse=True)
    
    return {"departments": dept_stats}

@app.get("/api/stats/cgpa")
async def get_cgpa_stats():
    """Get CGPA distribution statistics"""
    if simulation_state["students_data"] is None:
        load_initial_data()
    
    df = simulation_state["students_data"]
    
    # Create bins
    bins = [0, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
    labels = ['<6', '6-6.5', '6.5-7', '7-7.5', '7.5-8', '8-8.5', '8.5-9', '9-9.5', '9.5-10']
    
    df['cgpa_bin'] = pd.cut(df['cgpa'], bins=bins, labels=labels, include_lowest=True)
    
    # Overall distribution
    overall_dist = df['cgpa_bin'].value_counts().sort_index()
    
    # By status
    placed_dist = df[df['status'] == 'Placed']['cgpa_bin'].value_counts().sort_index()
    unplaced_dist = df[df['status'] == 'Unplaced']['cgpa_bin'].value_counts().sort_index()
    
    return {
        "bins": labels,
        "overall": overall_dist.reindex(labels, fill_value=0).tolist(),
        "placed": placed_dist.reindex(labels, fill_value=0).tolist(),
        "unplaced": unplaced_dist.reindex(labels, fill_value=0).tolist()
    }

@app.get("/api/stats/companies")
async def get_company_stats():
    """Get company statistics"""
    if simulation_state["companies_data"] is None:
        load_initial_data()
    
    df = simulation_state["companies_data"]
    
    # Role type distribution
    role_counts = df['job_role'].value_counts().to_dict()
    
    # Day-wise distribution
    day_counts = df['arrival_day'].value_counts().sort_index().to_dict()
    
    # Hiring capacity stats
    total_min = int(df['min_offers'].sum())
    total_max = int(df['max_offers'].sum())
    avg_min = df['min_offers'].mean()
    avg_max = df['max_offers'].mean()
    
    # Handle NaN values
    avg_min = 0 if pd.isna(avg_min) else round(avg_min, 2)
    avg_max = 0 if pd.isna(avg_max) else round(avg_max, 2)
    
    return {
        "role_types": role_counts,
        "day_distribution": day_counts,
        "total_min_capacity": total_min,
        "total_max_capacity": total_max,
        "avg_min_capacity": avg_min,
        "avg_max_capacity": avg_max
    }

@app.get("/api/stats/domain")
async def get_domain_stats():
    """Get domain preference statistics"""
    if simulation_state["students_data"] is None:
        load_initial_data()
    
    df = simulation_state["students_data"]
    
    # Domain 1 distribution
    domain1_counts = df['domain_1'].value_counts().to_dict()
    
    # Domain 2 distribution
    domain2_counts = df['domain_2'].value_counts().to_dict()
    
    # Combined domain counts
    all_domains = {}
    for domain, count in domain1_counts.items():
        all_domains[domain] = all_domains.get(domain, 0) + count
    for domain, count in domain2_counts.items():
        all_domains[domain] = all_domains.get(domain, 0) + count
    
    # Department x Domain matrix
    dept_domain_matrix = []
    for dept in sorted(df['department'].unique()):
        dept_df = df[df['department'] == dept]
        dept_domains = {}
        for _, row in dept_df.iterrows():
            if pd.notna(row['domain_1']):
                dept_domains[row['domain_1']] = dept_domains.get(row['domain_1'], 0) + 1
            if pd.notna(row['domain_2']):
                dept_domains[row['domain_2']] = dept_domains.get(row['domain_2'], 0) + 1
        
        dept_domain_matrix.append({
            "department": dept,
            "domains": dept_domains
        })
    
    return {
        "domain1_distribution": domain1_counts,
        "domain2_distribution": domain2_counts,
        "all_domains": all_domains,
        "dept_domain_matrix": dept_domain_matrix
    }

@app.post("/api/simulation/run")
async def run_simulation(config: SimulationConfig, background_tasks: BackgroundTasks):
    """Run the placement simulation with given configuration"""
    
    if simulation_state["status"] == "running":
        raise HTTPException(status_code=400, detail="Simulation already running")
    
    # Update simulation state
    simulation_state["status"] = "running"
    simulation_state["progress"] = 0
    simulation_state["message"] = "Initializing simulation..."
    
    # Run simulation in background
    background_tasks.add_task(execute_simulation, config)
    
    return {"status": "started", "message": "Simulation started"}

async def execute_simulation(config: SimulationConfig):
    """Execute the simulation (runs in background)"""
    try:
        # Update configuration
        global W1_CGPA_PROFILE, W2_SKILL_PROFILE, W3_RANDOM_PROFILE, W4_DEP_SCORE_PROFILE
        global W5_PROFILE_INTERVIEW, W6_CGPA_INTERVIEW, W7_RANDOM_INTERVIEW, P_OPT_OUT
        
        import placement_simulation
        placement_simulation.W1_CGPA_PROFILE = config.w1_cgpa
        placement_simulation.W2_SKILL_PROFILE = config.w2_skill
        placement_simulation.W3_RANDOM_PROFILE = config.w3_random
        placement_simulation.W4_DEP_SCORE_PROFILE = config.w4_dep_score
        placement_simulation.W5_PROFILE_INTERVIEW = config.w5_profile
        placement_simulation.W6_CGPA_INTERVIEW = config.w6_cgpa_interview
        placement_simulation.W7_RANDOM_INTERVIEW = config.w7_random_interview
        placement_simulation.P_OPT_OUT = config.p_opt_out
        
        # Set random seed
        random.seed(config.random_seed)
        np.random.seed(config.random_seed)
        
        simulation_state["message"] = "Loading data..."
        simulation_state["progress"] = 10
        
        # Load data
        students = load_students(STUDENTS_FILE)
        companies = load_companies(COMPANIES_FILE, SHORTLIST_DIR)
        company_order = load_company_order(COMPANY_ORDER_FILE)
        
        simulation_state["message"] = "Initializing simulation..."
        simulation_state["progress"] = 20
        
        # Initialize simulation
        sim = PlacementSimulation(students, companies, company_order)
        simulation_state["simulation_instance"] = sim
        
        simulation_state["message"] = "Running Day 1..."
        simulation_state["progress"] = 30
        
        # Run simulation
        sim.simulate_day(day=1)
        
        simulation_state["message"] = "Processing results..."
        simulation_state["progress"] = 90
        
        # Collect results
        results = {
            "students": [],
            "companies": [],
            "statistics": sim.stats
        }
        
        for student in sim.students.values():
            results["students"].append({
                "roll_no": student.roll_no,
                "name": student.name,
                "department": student.department,
                "cgpa": student.cgpa,
                "domain_1": student.domain_1,
                "domain_2": student.domain_2,
                "status": student.status,
                "placed_company": student.placed_company if student.placed_company else ""
            })
        
        for company in sim.companies.values():
            results["companies"].append({
                "company_id": company.get_unique_id(),
                "company_name": company.company_name,
                "job_role": company.job_role,
                "min_hires": company.min_hires,
                "max_hires": company.max_hires,
                "hired": len(company.hired),
                "applicants": len(company.applicants),
                "shortlisted": len(company.shortlisted)
            })
        
        # Update state
        simulation_state["results"] = results
        simulation_state["status"] = "completed"
        simulation_state["progress"] = 100
        simulation_state["message"] = "Simulation completed successfully!"
        
        # Update students data with results
        students_df = pd.DataFrame(results["students"])
        simulation_state["students_data"] = students_df
        
    except Exception as e:
        simulation_state["status"] = "error"
        simulation_state["message"] = f"Error: {str(e)}"
        simulation_state["progress"] = 0
        print(f"Simulation error: {e}")
        import traceback
        traceback.print_exc()

@app.get("/api/simulation/status")
async def get_simulation_status():
    """Get current simulation status"""
    return {
        "status": simulation_state["status"],
        "progress": simulation_state["progress"],
        "message": simulation_state["message"]
    }

@app.get("/api/simulation/results")
async def get_simulation_results():
    """Get simulation results"""
    if simulation_state["results"] is None:
        raise HTTPException(status_code=404, detail="No simulation results available")
    
    return simulation_state["results"]

@app.get("/api/results/placements")
async def get_placement_results():
    """Get detailed placement results"""
    if simulation_state["results"] is None:
        raise HTTPException(status_code=404, detail="No simulation results available")
    
    students = simulation_state["results"]["students"]
    
    # Calculate statistics
    total = len(students)
    placed = len([s for s in students if s["status"] == "Placed"])
    unplaced = len([s for s in students if s["status"] == "Unplaced"])
    opted_out = len([s for s in students if s["status"] == "Opted_Out"])
    
    # Department-wise breakdown
    dept_stats = {}
    for student in students:
        dept = student["department"]
        if dept not in dept_stats:
            dept_stats[dept] = {"total": 0, "placed": 0, "unplaced": 0, "opted_out": 0}
        
        dept_stats[dept]["total"] += 1
        if student["status"] == "Placed":
            dept_stats[dept]["placed"] += 1
        elif student["status"] == "Unplaced":
            dept_stats[dept]["unplaced"] += 1
        elif student["status"] == "Opted_Out":
            dept_stats[dept]["opted_out"] += 1
    
    return {
        "overall": {
            "total": total,
            "placed": placed,
            "unplaced": unplaced,
            "opted_out": opted_out,
            "placement_rate": round(placed / total * 100, 2) if total > 0 else 0
        },
        "by_department": dept_stats
    }

@app.get("/api/results/company-wise")
async def get_company_results():
    """Get company-wise hiring results"""
    if simulation_state["results"] is None:
        raise HTTPException(status_code=404, detail="No simulation results available")
    
    companies = simulation_state["results"]["companies"]
    
    # Sort by hired count
    companies_sorted = sorted(companies, key=lambda x: x["hired"], reverse=True)
    
    # Calculate statistics
    total_hired = sum(c["hired"] for c in companies)
    companies_that_hired = len([c for c in companies if c["hired"] > 0])
    avg_hires = round(total_hired / companies_that_hired, 2) if companies_that_hired > 0 else 0
    
    return {
        "companies": companies_sorted,
        "statistics": {
            "total_hired": total_hired,
            "companies_that_hired": companies_that_hired,
            "avg_hires_per_company": avg_hires
        }
    }

@app.get("/api/export/csv")
async def export_to_csv():
    """Export results to CSV"""
    if simulation_state["results"] is None:
        raise HTTPException(status_code=404, detail="No simulation results available")
    
    students = pd.DataFrame(simulation_state["results"]["students"])
    
    # Save to CSV
    output_file = BASE_DIR / "placement_simulation_model" / "dashboard_results.csv"
    students.to_csv(output_file, index=False)
    
    return FileResponse(output_file, filename="placement_results.csv", media_type="text/csv")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize data on startup"""
    print("Loading initial data...")
    load_initial_data()
    print("Dashboard ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
