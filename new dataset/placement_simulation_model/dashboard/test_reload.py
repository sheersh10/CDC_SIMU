"""Test to reload data and check for nan values"""
import httpx
import json

print("Step 1: Forcing data reload...")
response = httpx.get("http://localhost:8000/api/data/load")
print(f"Load response: {response.json()}")

print("\nStep 2: Getting student data...")
response = httpx.get("http://localhost:8000/api/students?limit=5")
print(f"Status: {response.status_code}")

data = response.json()
print(f"Got {len(data['data'])} students")

print("\nStep 3: Checking for 'nan' in response...")
json_str = json.dumps(data)

if "nan" in json_str.lower():
    print("❌ Found 'nan' in response!")
    
    # Show first student
    if data['data']:
        print("\nFirst student data:")
        for key, val in data['data'][0].items():
            if val and isinstance(val, str) and 'nan' in val.lower():
                print(f"  {key}: '{val}' ← CONTAINS NAN!")
            else:
                print(f"  {key}: {val}")
else:
    print("✅ No 'nan' found in response!")
    print("\nFirst student sample:")
    if data['data']:
        student = data['data'][0]
        print(f"  Roll: {student.get('roll_no')}")
        print(f"  Name: {student.get('name')}")
        print(f"  Domain 2: {student.get('domain_2')}")
        print(f"  Skills 2: {student.get('skills_for_domain_2')}")
