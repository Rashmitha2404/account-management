#!/usr/bin/env python
import pandas as pd
import os

# Read the Excel file
file_path = "Rashmita test data.xlsx"
print(f"Examining file: {file_path}")

if os.path.exists(file_path):
    # Read all sheets
    excel_file = pd.ExcelFile(file_path)
    print(f"Excel file has {len(excel_file.sheet_names)} sheets: {excel_file.sheet_names}")
    
    # Read the first sheet
    df = pd.read_excel(file_path, sheet_name=0)
    print(f"\nFirst sheet has {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    
    print("\nFirst 10 rows:")
    for i in range(min(10, len(df))):
        print(f"Row {i}: {dict(df.iloc[i])}")
    
    print(f"\nLast 5 rows:")
    for i in range(max(0, len(df)-5), len(df)):
        print(f"Row {i}: {dict(df.iloc[i])}")
    
    # Check for NaN values
    print(f"\nRows with all NaN values: {df.isna().all(axis=1).sum()}")
    print(f"Rows with any NaN values: {df.isna().any(axis=1).sum()}")
    
else:
    print(f"File {file_path} not found!")
    print("Available files:")
    for file in os.listdir('.'):
        if file.endswith('.xlsx'):
            print(f"  - {file}") 