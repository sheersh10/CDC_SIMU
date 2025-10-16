"""
Unit Tests for Placement Simulation Dashboard API
Tests all endpoints to ensure data is returned correctly and no NaN values are present
"""

import pytest
from fastapi.testclient import TestClient
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from main import app, simulation_state, load_initial_data

# Create test client
client = TestClient(app)


class TestHealthAndSetup:
    """Test basic health checks and data loading"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_load_data(self):
        """Test data loading endpoint"""
        response = client.get("/api/data/load")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data


class TestStudentsAPI:
    """Test student-related endpoints"""
    
    def test_get_students_basic(self):
        """Test basic students retrieval"""
        response = client.get("/api/students")
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "data" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        
        # Check data validity
        assert isinstance(data["data"], list)
        assert data["total"] >= 0
        assert data["limit"] == 100  # Default limit
        
        # Verify no NaN values in JSON
        json_str = json.dumps(data)
        assert "NaN" not in json_str
        assert "nan" not in json_str.lower()
    
    def test_get_students_with_filters(self):
        """Test students with filters"""
        # Test with department filter
        response = client.get("/api/students?department=CS&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) <= 10
        
        # Test with CGPA filters
        response = client.get("/api/students?cgpa_min=8.0&cgpa_max=9.0")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all students match CGPA criteria
        for student in data["data"]:
            if student.get("cgpa") is not None:
                assert 8.0 <= student["cgpa"] <= 9.0
    
    def test_get_students_pagination(self):
        """Test students pagination"""
        # First page
        response1 = client.get("/api/students?limit=50&offset=0")
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second page
        response2 = client.get("/api/students?limit=50&offset=50")
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Ensure different students
        if len(data1["data"]) > 0 and len(data2["data"]) > 0:
            assert data1["data"][0] != data2["data"][0]
    
    def test_students_no_nan_values(self):
        """Verify no NaN values in student data"""
        response = client.get("/api/students?limit=200")
        assert response.status_code == 200
        data = response.json()
        
        # Check each student record
        for student in data["data"]:
            for key, value in student.items():
                # None is acceptable, but not NaN
                if value is not None:
                    assert value == value  # NaN != NaN, so this fails for NaN
                    assert not (isinstance(value, float) and str(value) == "nan")


class TestCompaniesAPI:
    """Test company-related endpoints"""
    
    def test_get_companies_basic(self):
        """Test basic companies retrieval"""
        response = client.get("/api/companies")
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert "total" in data
        assert isinstance(data["data"], list)
        
        # Verify no NaN values
        json_str = json.dumps(data)
        assert "NaN" not in json_str
        assert "nan" not in json_str.lower()
    
    def test_get_companies_with_filters(self):
        """Test companies with filters"""
        # Test with role filter
        response = client.get("/api/companies?role=SDE")
        assert response.status_code == 200
        data = response.json()
        
        # Test with day filter
        response = client.get("/api/companies?day=1")
        assert response.status_code == 200
        data = response.json()
        
        # Verify day filter works
        for company in data["data"]:
            if "arrival_day" in company:
                assert company["arrival_day"] == 1
    
    def test_companies_no_nan_values(self):
        """Verify no NaN values in company data"""
        response = client.get("/api/companies?limit=200")
        assert response.status_code == 200
        data = response.json()
        
        for company in data["data"]:
            for key, value in company.items():
                if value is not None:
                    assert value == value  # Fails for NaN
                    assert not (isinstance(value, float) and str(value) == "nan")


class TestStatisticsAPI:
    """Test statistics endpoints"""
    
    def test_summary_stats(self):
        """Test summary statistics endpoint"""
        response = client.get("/api/stats/summary")
        assert response.status_code == 200
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
            # Check it's a valid number
            assert isinstance(data[field], (int, float))
            assert data[field] == data[field]  # Not NaN
        
        # Logical checks
        assert data["total_students"] >= 0
        assert data["placed_students"] + data["unplaced_students"] <= data["total_students"]
        assert 0 <= data["placement_rate"] <= 100
        assert 0 <= data["avg_cgpa_all"] <= 10
        assert 0 <= data["avg_cgpa_placed"] <= 10
    
    def test_department_stats(self):
        """Test department statistics endpoint"""
        response = client.get("/api/stats/department")
        assert response.status_code == 200
        data = response.json()
        
        assert "departments" in data
        assert isinstance(data["departments"], list)
        
        # Check each department
        for dept in data["departments"]:
            assert "department" in dept
            assert "total" in dept
            assert "placed" in dept
            assert "unplaced" in dept
            assert "avg_cgpa" in dept
            assert "placement_rate" in dept
            
            # Verify all values are valid numbers
            assert dept["total"] >= 0
            assert dept["placed"] >= 0
            assert dept["unplaced"] >= 0
            assert 0 <= dept["avg_cgpa"] <= 10
            assert 0 <= dept["placement_rate"] <= 100
            
            # Check no NaN
            assert dept["avg_cgpa"] == dept["avg_cgpa"]
            assert dept["placement_rate"] == dept["placement_rate"]
    
    def test_cgpa_stats(self):
        """Test CGPA distribution statistics"""
        response = client.get("/api/stats/cgpa")
        assert response.status_code == 200
        data = response.json()
        
        assert "bins" in data
        assert "overall" in data
        assert "placed" in data
        assert "unplaced" in data
        
        # Check arrays have same length
        assert len(data["bins"]) == len(data["overall"])
        assert len(data["bins"]) == len(data["placed"])
        assert len(data["bins"]) == len(data["unplaced"])
        
        # All values should be non-negative integers
        for val in data["overall"] + data["placed"] + data["unplaced"]:
            assert isinstance(val, (int, float))
            assert val >= 0
            assert val == val  # Not NaN
    
    def test_company_stats(self):
        """Test company statistics endpoint"""
        response = client.get("/api/stats/companies")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = [
            "role_types", "day_distribution",
            "total_min_capacity", "total_max_capacity",
            "avg_min_capacity", "avg_max_capacity"
        ]
        
        for field in required_fields:
            assert field in data
        
        # Check numeric values
        assert data["total_min_capacity"] >= 0
        assert data["total_max_capacity"] >= data["total_min_capacity"]
        assert data["avg_min_capacity"] >= 0
        assert data["avg_max_capacity"] >= 0
        
        # Check no NaN
        assert data["avg_min_capacity"] == data["avg_min_capacity"]
        assert data["avg_max_capacity"] == data["avg_max_capacity"]
    
    def test_domain_stats(self):
        """Test domain statistics endpoint"""
        response = client.get("/api/stats/domain")
        assert response.status_code == 200
        data = response.json()
        
        assert "domain1_distribution" in data
        assert "domain2_distribution" in data
        assert "all_domains" in data
        assert "dept_domain_matrix" in data
        
        # Check distributions are dictionaries
        assert isinstance(data["domain1_distribution"], dict)
        assert isinstance(data["domain2_distribution"], dict)
        assert isinstance(data["all_domains"], dict)
        
        # All counts should be positive integers
        for domain, count in data["all_domains"].items():
            assert isinstance(count, (int, float))
            assert count > 0


class TestMetadataEndpoints:
    """Test metadata endpoints"""
    
    def test_get_departments(self):
        """Test departments list endpoint"""
        response = client.get("/api/departments")
        assert response.status_code == 200
        data = response.json()
        
        assert "departments" in data
        assert isinstance(data["departments"], list)
        assert len(data["departments"]) > 0
        
        # All should be strings
        for dept in data["departments"]:
            assert isinstance(dept, str)
            assert len(dept) > 0
    
    def test_get_domains(self):
        """Test domains list endpoint"""
        response = client.get("/api/domains")
        assert response.status_code == 200
        data = response.json()
        
        assert "domains" in data
        assert isinstance(data["domains"], list)
        assert len(data["domains"]) > 0
        
        # All should be strings
        for domain in data["domains"]:
            assert isinstance(domain, str)
            assert len(domain) > 0


class TestSimulationEndpoints:
    """Test simulation-related endpoints"""
    
    def test_get_simulation_status(self):
        """Test simulation status endpoint"""
        response = client.get("/api/simulation/status")
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "progress" in data
        assert "message" in data
        
        # Status should be valid
        assert data["status"] in ["idle", "running", "completed", "error"]
        assert 0 <= data["progress"] <= 100


class TestJSONCompliance:
    """Test JSON compliance across all endpoints"""
    
    def test_all_responses_json_serializable(self):
        """Ensure all endpoint responses are JSON serializable without NaN"""
        endpoints = [
            "/api/health",
            "/api/data/load",
            "/api/students?limit=50",
            "/api/companies?limit=50",
            "/api/departments",
            "/api/domains",
            "/api/stats/summary",
            "/api/stats/department",
            "/api/stats/cgpa",
            "/api/stats/companies",
            "/api/stats/domain",
            "/api/simulation/status"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200, f"Failed for {endpoint}"
            
            # Should be valid JSON
            data = response.json()
            
            # Re-serialize to ensure no NaN values
            json_str = json.dumps(data)
            assert "NaN" not in json_str, f"Found NaN in {endpoint}"
            assert "nan" not in json_str.lower(), f"Found nan in {endpoint}"
            
            # Should be able to parse it back
            reparsed = json.loads(json_str)
            assert reparsed is not None


# Run the tests
if __name__ == "__main__":
    print("="*80)
    print("PLACEMENT SIMULATION DASHBOARD - API UNIT TESTS")
    print("="*80)
    
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short", "--color=yes"])
