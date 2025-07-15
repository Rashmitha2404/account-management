import requests
import time

def test_export():
    base_url = "http://127.0.0.1:8000/api"
    
    print("Testing export endpoints...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/transactions/")
        print(f"✅ Server is running. Transactions endpoint status: {response.status_code}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return
    
    # Test 2: Test export_transactions endpoint (without format)
    try:
        response = requests.get(f"{base_url}/transactions/export/")
        print(f"Export endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Export endpoint working!")
        else:
            print(f"❌ Export endpoint failed: {response.text}")
    except Exception as e:
        print(f"❌ Export endpoint error: {e}")
    
    # Test 3: Test with format parameter
    try:
        response = requests.get(f"{base_url}/transactions/export/?format=excel")
        print(f"Excel export status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Excel export working!")
            print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        else:
            print(f"❌ Excel export failed: {response.text}")
    except Exception as e:
        print(f"❌ Excel export error: {e}")

if __name__ == "__main__":
    test_export() 