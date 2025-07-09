#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_backend.settings')
django.setup()

# Now import Django models
from transactions.models import Transaction

print("=== DATABASE INSPECTION ===")
print(f"Total transactions: {Transaction.objects.count()}")
print(f"Debit transactions: {Transaction.objects.filter(type='Debit').count()}")
print(f"Credit transactions: {Transaction.objects.filter(type='Credit').count()}")

print("\n=== ALL TRANSACTIONS BY TYPE ===")
debit_transactions = Transaction.objects.filter(type='Debit')
credit_transactions = Transaction.objects.filter(type='Credit')

print(f"\nDEBIT TRANSACTIONS ({debit_transactions.count()}):")
for t in debit_transactions:
    print(f"- Debit: {t.amount} on {t.date} (ID: {t.id})")

print(f"\nCREDIT TRANSACTIONS ({credit_transactions.count()}):")
for t in credit_transactions:
    print(f"- Credit: {t.amount} on {t.date} (ID: {t.id})")

print("\n=== RECENT TRANSACTIONS (Last 10) ===")
for t in Transaction.objects.order_by('-id')[:10]:
    print(f"- {t.type}: {t.amount} on {t.date} (ID: {t.id})")

print("\n=== TRANSACTIONS BY DATE ===")
from django.db.models import Count
date_counts = Transaction.objects.values('date').annotate(count=Count('id')).order_by('date')
for item in date_counts:
    print(f"- {item['date']}: {item['count']} transactions") 