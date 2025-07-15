#!/usr/bin/env python3
"""
Test script to check URL patterns
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_backend.settings')
django.setup()

from django.urls import reverse
from transactions.urls import urlpatterns

print("=== URL PATTERNS TEST ===")
print(f"Total patterns in transactions.urls: {len(urlpatterns)}")

for i, pattern in enumerate(urlpatterns):
    print(f"{i}: {pattern}")

print("\n=== TESTING SPECIFIC URLS ===")

# Test if we can reverse the export URL
try:
    url = reverse('transactions:export_transactions')
    print(f"✅ export_transactions URL: {url}")
except Exception as e:
    print(f"❌ export_transactions URL error: {e}")

try:
    url = reverse('transactions:export_transactions_alt')
    print(f"✅ export_transactions_alt URL: {url}")
except Exception as e:
    print(f"❌ export_transactions_alt URL error: {e}")

print("\n=== TESTING DIRECT ACCESS ===")
import requests

# Test the working URL
try:
    r = requests.get('http://127.0.0.1:8000/api/transactions/')
    print(f"✅ /api/transactions/ status: {r.status_code}")
except Exception as e:
    print(f"❌ /api/transactions/ error: {e}")

# Test the export URL
try:
    r = requests.get('http://127.0.0.1:8000/api/transactions/export/')
    print(f"✅ /api/transactions/export/ status: {r.status_code}")
except Exception as e:
    print(f"❌ /api/transactions/export/ error: {e}")

# Test the export URL with format
try:
    r = requests.get('http://127.0.0.1:8000/api/transactions/export/?format=excel')
    print(f"✅ /api/transactions/export/?format=excel status: {r.status_code}")
except Exception as e:
    print(f"❌ /api/transactions/export/?format=excel error: {e}") 