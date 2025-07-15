#!/usr/bin/env python3
"""
Test script to verify export functionality
"""
import requests

# Test export with filters but without format parameter
url = 'http://127.0.0.1:8000/api/export/?start_date=2025-01-01&end_date=2025-01-31&type=Credit&category=CSR'
response = requests.get(url)

print(f'Status: {response.status_code}')
print(f'Content-Type: {response.headers.get("content-type", "N/A")}')
print(f'Content-Length: {len(response.content)} bytes')
print(f'Content-Disposition: {response.headers.get("content-disposition", "N/A")}')

if response.status_code == 200:
    print("✅ Export successful!")
else:
    print(f"❌ Export failed: {response.text}") 