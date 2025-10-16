"""
Simple API Tests - Direct Testing Without Pytest
Tests all endpoints to ensure data is returned correctly and no NaN values are present
"""

import httpx
import json
import sys
from pathlib import Path
import time

# Test against running server
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("\n[TEST] Health Check")
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200, "Health check failed"
        data = response.json()
        assert data["status"] == "healthy"
        print("✓ Health check passed")

def test_load_data():
    """Test data loading endpoint"""
    print("\n[TEST] Load Data")
    response = client.get("/api/data/load")
    assert response.status_code == 200, "Data load failed"
    data = response.json()
    assert data["status"] == "success"
    print("✓ Data loading passed")

def test_get_students():
    """Test students retrieval"""
    print("\n[TEST] Get Students")
    response = client.get("/api/students?limit=100")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    # Check structure
    assert "data" in data
    assert "total" in data
    assert isinstance(data["data"], list)
    
    # Verify no NaN values
    json_str = json.dumps(data)
    assert "NaN" not in json_str, "Found NaN in response"
    assert "nan" not in json_str.lower(), "Found nan in response"
    
    print(f"✓ Students endpoint passed (returned {len(data['data'])} students)")

def test_get_companies():
    """Test companies retrieval"""
    print("\n[TEST] Get Companies")
    response = client.get("/api/companies?limit=100")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    assert "data" in data
    assert isinstance(data["data"], list)
    
    # Verify no NaN values
    json_str = json.dumps(data)
    assert "NaN" not in json_str, "Found NaN in response"
    
    print(f"✓ Companies endpoint passed (returned {len(data['data'])} companies)")

def test_summary_stats():
    """Test summary statistics"""
    print("\n[TEST] Summary Statistics")
    response = client.get("/api/stats/summary")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    # Check all required fields
    required_fields = [
        "total_students", "total_companies", "placed_students",
        "unplaced_students", "opted_out", "placement_rate",
        "avg_cgpa_all", "avg_cgpa_placed", "total_positions", "min_positions"
    ]
    
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
        assert data[field] is not None
        assert isinstance(data[field], (int, float))
        assert data[field] == data[field], f"NaN found in {field}"
    
    print(f"✓ Summary stats passed")
    print(f"  - Total Students: {data['total_students']}")
    print(f"  - Placed: {data['placed_students']} ({data['placement_rate']}%)")
    print(f"  - Average CGPA: {data['avg_cgpa_all']}")

def test_department_stats():
    """Test department statistics"""
    print("\n[TEST] Department Statistics")
    response = client.get("/api/stats/department")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    assert "departments" in data
    assert isinstance(data["departments"], list)
    
    # Check each department
    for dept in data["departments"]:
        assert "department" in dept
        assert "avg_cgpa" in dept
        assert "placement_rate" in dept
        
        # Verify no NaN
        assert dept["avg_cgpa"] == dept["avg_cgpa"], f"NaN in avg_cgpa for {dept['department']}"
        assert dept["placement_rate"] == dept["placement_rate"], f"NaN in placement_rate for {dept['department']}"
    
    print(f"✓ Department stats passed ({len(data['departments'])} departments)")

def test_cgpa_stats():
    """Test CGPA distribution"""
    print("\n[TEST] CGPA Distribution")
    response = client.get("/api/stats/cgpa")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    assert "bins" in data
    assert "overall" in data
    assert "placed" in data
    
    # All values should be valid
    for val in data["overall"] + data["placed"] + data["unplaced"]:
        assert val == val, "Found NaN in CGPA stats"
    
    print(f"✓ CGPA stats passed")

def test_company_stats():
    """Test company statistics"""
    print("\n[TEST] Company Statistics")
    response = client.get("/api/stats/companies")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    # Check no NaN in averages
    assert data["avg_min_capacity"] == data["avg_min_capacity"], "NaN in avg_min_capacity"
    assert data["avg_max_capacity"] == data["avg_max_capacity"], "NaN in avg_max_capacity"
    
    print(f"✓ Company stats passed")
    print(f"  - Total capacity: {data['total_min_capacity']} - {data['total_max_capacity']}")

def test_domain_stats():
    """Test domain statistics"""
    print("\n[TEST] Domain Statistics")
    response = client.get("/api/stats/domain")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    assert "domain1_distribution" in data
    assert "all_domains" in data
    
    print(f"✓ Domain stats passed")

def test_departments_list():
    """Test departments list"""
    print("\n[TEST] Departments List")
    response = client.get("/api/departments")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    assert "departments" in data
    assert isinstance(data["departments"], list)
    assert len(data["departments"]) > 0
    
    print(f"✓ Departments list passed ({len(data['departments'])} departments)")

def test_domains_list():
    """Test domains list"""
    print("\n[TEST] Domains List")
    response = client.get("/api/domains")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    assert "domains" in data
    assert isinstance(data["domains"], list)
    
    print(f"✓ Domains list passed ({len(data['domains'])} domains)")

def test_simulation_status():
    """Test simulation status"""
    print("\n[TEST] Simulation Status")
    response = client.get("/api/simulation/status")
    assert response.status_code == 200, f"Failed with {response.status_code}"
    data = response.json()
    
    assert "status" in data
    assert data["status"] in ["idle", "running", "completed", "error"]
    
    print(f"✓ Simulation status passed (status: {data['status']})")

def test_json_compliance():
    """Test JSON compliance for all endpoints"""
    print("\n[TEST] JSON Compliance Check")
    endpoints = [
        "/api/students?limit=50",
        "/api/companies?limit=50",
        "/api/stats/summary",
        "/api/stats/department",
        "/api/stats/cgpa",
        "/api/stats/companies",
        "/api/stats/domain",
    ]
    
    passed = 0
    for endpoint in endpoints:
        response = client.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            json_str = json.dumps(data)
            assert "NaN" not in json_str, f"Found NaN in {endpoint}"
            assert "nan" not in json_str.lower(), f"Found nan in {endpoint}"
            passed += 1
    
    print(f"✓ JSON compliance passed for {passed}/{len(endpoints)} endpoints")

def run_all_tests():
    """Run all tests"""
    print("="*80)
    print("PLACEMENT SIMULATION DASHBOARD - API TESTS")
    print("="*80)
    
    tests = [
        test_health_check,
        test_load_data,
        test_get_students,
        test_get_companies,
        test_summary_stats,
        test_department_stats,
        test_cgpa_stats,
        test_company_stats,
        test_domain_stats,
        test_departments_list,
        test_domains_list,
        test_simulation_status,
        test_json_compliance
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} FAILED: {str(e)}")
    
    print("\n" + "="*80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed out of {len(tests)} total")
    print("="*80)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Dashboard is ready to use.")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
