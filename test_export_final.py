#!/usr/bin/env python3
import requests

def test_export():
    print("Testing export endpoint...")
    
    # Test the export endpoint
    try:
        response = requests.get('http://127.0.0.1:8000/api/export/?format=excel')
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ Export endpoint is working!")
            # Save the file to test
            with open('test_export.xlsx', 'wb') as f:
                f.write(response.content)
            print("✅ File saved as test_export.xlsx")
        else:
            print(f"❌ Export failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_export() 