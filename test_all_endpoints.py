#!/usr/bin/env python3
import requests

def test_all_endpoints():
    base_url = "http://127.0.0.1:8000/api"
    
    endpoints = [
        "/transactions/",
        "/test-export/",
        "/export/",
        "/export/?format=excel",
        "/chart-data/export/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"✅ {endpoint}: {response.status_code}")
            if response.status_code != 200:
                print(f"   Response: {response.text[:100]}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

if __name__ == "__main__":
    test_all_endpoints() 