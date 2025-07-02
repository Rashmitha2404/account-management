import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_backend.settings')
django.setup()

from transactions.models import Transaction
from django.db import models

def update_categories():
    print("Updating transaction categories...")
    
    # Define comprehensive category mappings (old -> new)
    category_mappings = {
        # Fix capitalization and naming issues
        'Training Expenses': 'Training expenses',
        'Bank Charges': 'Bank charges',
        'SP Tutor Salary': 'Salaries to Employees',
        'Membership': 'Membership fees',
        'Loan': 'Loans',
        'Salary': 'Salaries to Employees',
        'Honorarium': 'Honorarium to tutors',
        'Rent office space': 'Rent',
        'Audit Fees': 'Audit expenses',
        'Donation for SP': 'Donation',
        'Sahaaj Poshan': 'Donation',
        'Car Insurance, petrol, maintenance': 'Travel',
        'Lea Associates Project Expenses': 'Other operational expenses',
    }
    
    # Get all unique categories currently in the database
    existing_categories = Transaction.objects.values_list('category', flat=True).distinct()
    print(f"Current categories in database: {list(existing_categories)}")
    
    # Update categories according to mappings
    updated_count = 0
    for old_category, new_category in category_mappings.items():
        count = Transaction.objects.filter(category=old_category).count()
        if count > 0:
            Transaction.objects.filter(category=old_category).update(category=new_category)
            print(f"Updated {count} transactions from '{old_category}' to '{new_category}'")
            updated_count += count
    
    # Check for any categories that don't match the current model definitions
    current_credit_categories = [
        'Corpus', 'CSR', 'Grants', 'Membership fees', 'Loans', 'Donation', 'Others'
    ]
    
    current_debit_categories = [
        'Education', 'Empowerment', 'Environment', 'Innovation',
        'Salaries to Employees', 'Stipends to apprentice', 'Honorarium to tutors',
        'Rent', 'Travel', 'Maintenance', 'Other operational expenses',
        'Educational aid', 'Digital gadgets', 'Consumables', 'Training expenses',
        'Bank charges', 'Audit expenses', 'Outsourcing'
    ]
    
    all_valid_categories = current_credit_categories + current_debit_categories
    
    # Find invalid categories
    invalid_categories = []
    for category in existing_categories:
        if category not in all_valid_categories:
            invalid_categories.append(category)
    
    if invalid_categories:
        print(f"\nWARNING: Found categories that don't match current model definitions:")
        for cat in invalid_categories:
            count = Transaction.objects.filter(category=cat).count()
            print(f"  - '{cat}' ({count} transactions)")
        print("\nYou may want to update these categories manually or add them to the model.")
    
    print(f"\nCategory update completed. Updated {updated_count} transactions.")
    
    # Show final category distribution
    print("\nFinal category distribution:")
    final_categories = Transaction.objects.values('category').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    for item in final_categories:
        print(f"  {item['category']}: {item['count']} transactions")

if __name__ == "__main__":
    update_categories() 