from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
    ]
    
    # Credit categories
    CREDIT_CATEGORIES = [
        ('Corpus', 'Corpus'),
        ('CSR', 'CSR'),
        ('Grants', 'Grants'),
        ('Membership fees', 'Membership fees'),
        ('Loans', 'Loans'),
        ('Donation', 'Donation'),
        ('Others', 'Others'),
    ]
    
    # Debit categories
    DEBIT_CATEGORIES = [
        # Programmatic
        ('Education', 'Education'),
        ('Empowerment', 'Empowerment'),
        ('Environment', 'Environment'),
        ('Innovation', 'Innovation'),
        # Administrative
        ('Salaries to Employees', 'Salaries to Employees'),
        ('Stipends to apprentice', 'Stipends to apprentice'),
        ('Honorarium to tutors', 'Honorarium to tutors'),
        ('Rent', 'Rent'),
        ('Travel', 'Travel'),
        ('Maintenance', 'Maintenance'),
        ('Other operational expenses', 'Other operational expenses'),
        ('Educational aid', 'Educational aid'),
        ('Digital gadgets', 'Digital gadgets'),
        ('Consumables', 'Consumables'),
        ('Training expenses', 'Training expenses'),
        ('Bank charges', 'Bank charges'),
        ('Audit expenses', 'Audit expenses'),
        ('Outsourcing', 'Outsourcing'),
    ]
    
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)
    voucher_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    from_party = models.CharField(max_length=100, blank=True, null=True)
    to_party = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.voucher_number} - {self.type} - {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.voucher_number or self.voucher_number == '':
            self.voucher_number = self.generate_voucher_number()
        super().save(*args, **kwargs)
    
    def generate_voucher_number(self):
        """Generate voucher number in format V/YY-YY/NN"""
        from datetime import datetime
        
        # Get current financial year (April to March)
        current_date = self.date or datetime.now().date()
        year = current_date.year
        month = current_date.month
        
        if month >= 4:  # April onwards
            fy_start = year
            fy_end = year + 1
        else:  # January to March
            fy_start = year - 1
            fy_end = year
        
        # Format as YY-YY (e.g., 25-26 for 2025-2026)
        fy_string = f"{str(fy_start)[-2:]}-{str(fy_end)[-2:]}"
        
        # Find the next number for this financial year
        last_transaction = Transaction.objects.filter(
            voucher_number__startswith=f"V/{fy_string}/"
        ).order_by('-voucher_number').first()
        
        if last_transaction:
            try:
                # Extract the serial number from the last voucher
                last_number = int(last_transaction.voucher_number.split('/')[-1])
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Format as V/YY-YY/NN (e.g., V/25-26/01)
        return f"V/{fy_string}/{str(next_number).zfill(2)}"
