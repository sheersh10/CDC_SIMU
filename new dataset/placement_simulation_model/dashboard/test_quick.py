"""Quick test to see actual student data response"""
import httpx
import json

response = httpx.get("http://localhost:8000/api/students?limit=5")
data = response.json()

print("Response status:", response.status_code)
print("\nNumber of students:", len(data['data']))

if len(data['data']) > 0:
    print("\nFirst student:")
    student = data['data'][0]
    for key, value in student.items():
        print(f"  {key}: {value} (type: {type(value).__name__})")

print("\nChecking for nan in JSON...")
json_str = json.dumps(data)
if "nan" in json_str.lower():
    print("Found 'nan' in response!")
    # Find where
    import re
    matches = re.finditer(r'\bnan\b', json_str, re.IGNORECASE)
    for i, match in enumerate(matches):
        start = max(0, match.start() - 50)
        end = min(len(json_str), match.end() + 50)
        print(f"\n  Match {i+1}: ...{json_str[start:end]}...")
else:
    print("No 'nan' found!")
