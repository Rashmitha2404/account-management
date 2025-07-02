import pandas as pd
from datetime import datetime, timedelta

# Create sample data
sample_data = [
    {
        'Date': '2024-01-15',
        'Type': 'Credit',
        'Amount': 50000.00,
        'Category': 'Corpus',
        'Purpose/Remarks': 'Initial corpus fund',
        'From': 'ABC Corp',
        'To': 'Your Org',
        'Reference Number': 'REF12345'
    },
    {
        'Date': '2024-01-20',
        'Type': 'Credit',
        'Amount': 25000.00,
        'Category': 'CSR',
        'Purpose/Remarks': 'CSR contribution from ABC Corp',
        'From': 'ABC Corp',
        'To': 'Your Org',
        'Reference Number': 'REF12346'
    },
    {
        'Date': '2024-01-25',
        'Type': 'Debit',
        'Amount': 15000.00,
        'Category': 'Education',
        'Purpose/Remarks': 'Educational program expenses',
        'From': 'Your Org',
        'To': 'School Name',
        'Reference Number': 'REF12347'
    },
    {
        'Date': '2024-02-01',
        'Type': 'Credit',
        'Amount': 10000.00,
        'Category': 'Donation',
        'Purpose/Remarks': 'Individual donation',
        'From': 'John Doe',
        'To': 'Your Org',
        'Reference Number': 'REF12348'
    },
    {
        'Date': '2024-02-05',
        'Type': 'Debit',
        'Amount': 8000.00,
        'Category': 'Salaries to Employees',
        'Purpose/Remarks': 'Staff salary payment',
        'From': 'Your Org',
        'To': 'Employee Name',
        'Reference Number': 'REF12349'
    }
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Save as Excel file
df.to_excel('sample_transactions.xlsx', index=False)

print("Sample Excel file 'sample_transactions.xlsx' created successfully!")
print("\nExpected column headers:")
print("- Date")
print("- Type (Credit/Debit)")
print("- Amount")
print("- Category")
print("- Purpose/Remarks")
print("- From")
print("- To")
print("- Reference Number")
print("\nYou can now upload this file to test the system.") 