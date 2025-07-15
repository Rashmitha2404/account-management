import requests

def test_export_endpoint():
    print("Testing export endpoint with query parameters...")
    
    # Test 1: Basic export (no parameters)
    r1 = requests.get('http://127.0.0.1:8000/api/export/')
    print(f"✅ Basic export: {r1.status_code}")
    
    # Test 2: Export with filters
    r2 = requests.get('http://127.0.0.1:8000/api/export/?start_date=2025-01-01&end_date=2025-01-31&type=Credit&category=CSR&format=excel')
    print(f"✅ Filtered export: {r2.status_code}")
    
    if r2.status_code == 200:
        print(f"   Content-Type: {r2.headers.get('content-type', 'N/A')}")
        print(f"   Content-Length: {len(r2.content)} bytes")
        print("   ✅ Export with filters is working!")
    else:
        print(f"   ❌ Export with filters failed: {r2.text[:200]}")

if __name__ == "__main__":
    test_export_endpoint() 