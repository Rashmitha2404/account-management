import pandas as pd
import os
import requests
import json

def check_excel_file(filename):
    try:
        # Read the Excel file
        df = pd.read_excel(filename)
        
        print(f"File: {filename}")
        print(f"Total rows: {len(df)}")
        print(f"Total columns: {len(df.columns)}")
        print("\nColumn names:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1}. '{col}'")
        
        print("\nFirst 3 rows of data:")
        print(df.head(3).to_string())
        
        print("\nColumn data types:")
        print(df.dtypes)
        
        return df.columns.tolist()
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Check your file
filename = "Rashmita test data.xlsx"
if os.path.exists(filename):
    columns = check_excel_file(filename)
else:
    print(f"File '{filename}' not found in current directory")
    print("Available files:")
    for file in os.listdir('.'):
        if file.endswith(('.xlsx', '.xls', '.csv')):
            print(f"  - {file}")

# Test the API endpoint
url = "http://127.0.0.1:8000/api/transactions/"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Total transactions: {len(data)}")
    
    if len(data) > 0:
        print("\nFirst transaction:")
        print(json.dumps(data[0], indent=2))
        
        print("\nChecking voucher numbers in first 5 transactions:")
        for i, tx in enumerate(data[:5]):
            print(f"Transaction {i+1}: voucher_number = '{tx.get('voucher_number', 'NOT FOUND')}'")
    else:
        print("No transactions found")
else:
    print(f"Error: {response.status_code}")
    print(response.text) 