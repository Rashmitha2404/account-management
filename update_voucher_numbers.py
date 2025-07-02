import os
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_backend.settings')
django.setup()

from transactions.models import Transaction
from django.db import transaction as db_transaction

def get_financial_year(date):
    year = date.year
    month = date.month
    if month >= 4:
        fy_start = year
        fy_end = year + 1
    else:
        fy_start = year - 1
        fy_end = year
    return f"{str(fy_start)[-2:]}-{str(fy_end)[-2:]}"

def main():
    print("Assigning new voucher numbers for all transactions (two-step process)...")
    transactions = Transaction.objects.all().order_by('date', 'id')
    fy_map = {}
    for tx in transactions:
        fy = get_financial_year(tx.date)
        if fy not in fy_map:
            fy_map[fy] = []
        fy_map[fy].append(tx)

    # Compute new voucher numbers in memory
    new_voucher_map = {}  # tx.id -> new_voucher
    for fy, txs in fy_map.items():
        for idx, tx in enumerate(txs, 1):
            new_voucher = f"V/{fy}/{str(idx).zfill(2)}"
            new_voucher_map[tx.id] = new_voucher

    # Step 1: Assign temporary voucher numbers
    print("Step 1: Assigning temporary voucher numbers...")
    with db_transaction.atomic():
        for tx in transactions:
            tmp_voucher = f"TMP-{tx.id}"
            tx.voucher_number = tmp_voucher
            tx.save(update_fields=['voucher_number'])
    print("Temporary voucher numbers assigned.")

    # Step 2: Assign correct new voucher numbers
    print("Step 2: Assigning correct new voucher numbers...")
    with db_transaction.atomic():
        for tx in transactions:
            new_voucher = new_voucher_map[tx.id]
            print(f"Setting ID {tx.id}: {tx.voucher_number} -> {new_voucher}")
            tx.voucher_number = new_voucher
            tx.save(update_fields=['voucher_number'])
    print(f"Done! Updated {len(transactions)} transactions.")

if __name__ == "__main__":
    main() 