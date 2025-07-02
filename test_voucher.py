import os
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_backend.settings')
django.setup()

from transactions.models import Transaction

def test_voucher_generation():
    print("Testing voucher number generation...")
    
    # Test for different dates
    test_dates = [
        date(2025, 6, 15),  # June 2025 (FY 2025-26)
        date(2025, 1, 15),  # January 2025 (FY 2024-25)
        date(2024, 8, 15),  # August 2024 (FY 2024-25)
    ]
    
    for test_date in test_dates:
        print(f"\nTesting date: {test_date}")
        
        # Create a test transaction
        transaction = Transaction(
            date=test_date,
            type='Credit',
            amount=1000.00,
            category='Test',
            remarks='Test transaction',
            voucher_number=''  # Will be auto-generated
        )
        
        # Generate voucher number
        voucher_number = transaction.generate_voucher_number()
        print(f"Generated voucher number: {voucher_number}")
        
        # Verify format
        parts = voucher_number.split('/')
        if len(parts) == 3 and parts[0] == 'V':
            print(f"✓ Format is correct: V/YY-YY/NN")
            print(f"  Financial year: {parts[1]}")
            print(f"  Serial number: {parts[2]}")
        else:
            print(f"✗ Format is incorrect: {voucher_number}")

if __name__ == "__main__":
    test_voucher_generation() 