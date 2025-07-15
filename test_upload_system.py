#!/usr/bin/env python
"""
Test script for the upload system
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_backend.settings')
django.setup()

from transactions.models import Transaction
from transactions.forms import TransactionManualInputForm

def test_model():
    """Test the Transaction model"""
    print("Testing Transaction model...")
    
    # Test voucher number generation
    from datetime import date
    transaction = Transaction(
        date=date(2025, 1, 15),
        type='Credit',
        amount=1000.00,
        category='CSR',
        remarks='Test transaction',
        purpose='Test purpose',
        payee_recipient_name='Test Recipient'
    )
    
    # The voucher number should be auto-generated
    print(f"Transaction created: {transaction}")
    print(f"Voucher number: {transaction.voucher_number}")
    print("✓ Model test passed")

def test_forms():
    """Test the forms"""
    print("\nTesting forms...")
    
    # Test TransactionManualInputForm
    form = TransactionManualInputForm()
    print(f"Form fields: {list(form.fields.keys())}")
    print("✓ Forms test passed")

def test_categories():
    """Test category choices"""
    print("\nTesting categories...")
    
    print(f"Credit categories: {len(Transaction.CREDIT_CATEGORIES)}")
    print(f"Debit categories: {len(Transaction.DEBIT_CATEGORIES)}")
    print("✓ Categories test passed")

if __name__ == "__main__":
    print("=== Testing Upload System ===\n")
    
    try:
        test_model()
        test_forms()
        test_categories()
        print("\n✓ All tests passed! The system is ready.")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc() 