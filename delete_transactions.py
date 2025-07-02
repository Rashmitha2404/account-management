import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_backend.settings')
django.setup()

from transactions.models import Transaction

def main():
    print("Deleting all transactions from database...")
    
    # Count transactions before deletion
    count = Transaction.objects.count()
    print(f"Found {count} transactions to delete.")
    
    if count == 0:
        print("No transactions to delete.")
        return
    
    # Delete all transactions
    Transaction.objects.all().delete()
    
    print(f"Successfully deleted {count} transactions.")
    print("Database is now empty and ready for new data with correct voucher number format.")

if __name__ == "__main__":
    main() 