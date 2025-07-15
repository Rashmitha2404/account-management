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
        ('Registration fees', 'Registration fees'),  # New category
        ('Loans', 'Loans'),
        ('Donation', 'Donation'),
        ('Others', 'Others'),
    ]
    
    # Purpose choices for transactions
    PURPOSE_CHOICES = [
        ('Salary Payment', 'Salary Payment'),
        ('Office Rent', 'Office Rent'),
        ('Equipment Purchase', 'Equipment Purchase'),
        ('Transport Expenses', 'Transport Expenses'),
        ('Stationary Purchase', 'Stationary Purchase'),
        ('Training Expenses', 'Training Expenses'),
        ('Maintenance', 'Maintenance'),
        ('Utility Bills', 'Utility Bills'),
        ('Insurance', 'Insurance'),
        ('Legal Fees', 'Legal Fees'),
        ('Audit Fees', 'Audit Fees'),
        ('Marketing Expenses', 'Marketing Expenses'),
        ('Travel Expenses', 'Travel Expenses'),
        ('Food & Refreshments', 'Food & Refreshments'),
        ('Grant Received', 'Grant Received'),
        ('Donation Received', 'Donation Received'),
        ('Membership Fees', 'Membership Fees'),
        ('Loan Repayment', 'Loan Repayment'),
        ('Investment Income', 'Investment Income'),
        ('Other Income', 'Other Income'),
        ('Other Expenses', 'Other Expenses'),
    ]
    
    # Payee/Recipient choices
    PAYEE_RECIPIENT_CHOICES = [
        ('Staff', 'Staff'),
        ('Employees', 'Employees'),
        ('Contractors', 'Contractors'),
        ('Suppliers', 'Suppliers'),
        ('Vendors', 'Vendors'),
        ('Government', 'Government'),
        ('Corporate', 'Corporate'),
        ('Individuals', 'Individuals'),
        ('Banks', 'Banks'),
        ('Insurance Companies', 'Insurance Companies'),
        ('Utility Companies', 'Utility Companies'),
        ('Transport Services', 'Transport Services'),
        ('Training Institutes', 'Training Institutes'),
        ('Audit Firms', 'Audit Firms'),
        ('Legal Firms', 'Legal Firms'),
        ('Marketing Agencies', 'Marketing Agencies'),
        ('Hotels', 'Hotels'),
        ('Restaurants', 'Restaurants'),
        ('Equipment Suppliers', 'Equipment Suppliers'),
        ('Stationary Suppliers', 'Stationary Suppliers'),
        ('Members', 'Members'),
        ('Donors', 'Donors'),
        ('Investors', 'Investors'),
        ('Others', 'Others'),
    ]
    
    # Debit categories - Updated structure
    DEBIT_CATEGORIES = [
        # Programmatic Domains
        ('Education', 'Education'),
        ('Empowerment', 'Empowerment'),
        ('Environment', 'Environment'),
        ('Innovation', 'Innovation'),
        
        # CAPX (Capital Expenditure)
        ('Equipment/Machine', 'Equipment/Machine'),
        ('Computer, Laptop, Printer, scanners, etc', 'Computer, Laptop, Printer, scanners, etc'),
        ('Furniture', 'Furniture'),
        
        # OPX (Operational Expenditure) - Human Resource
        ('Salaries to Employees', 'Salaries to Employees'),
        ('Stipends to apprentice', 'Stipends to apprentice'),
        ('Honorarium to tutors', 'Honorarium to tutors'),
        ('Honorarium to others', 'Honorarium to others'),
        
        # OPX - Maintenance
        ('Rent of office space', 'Rent of office space'),
        ('Maintenance', 'Maintenance'),
        
        # OPX - Travel
        ('Transport', 'Transport'),
        ('Car hire', 'Car hire'),
        ('Petrol', 'Petrol'),
        ('Car maintenance', 'Car maintenance'),
        
        # OPX - Educational aid
        ('Digital gadgets', 'Digital gadgets'),
        ('Stationary items to students', 'Stationary items to students'),
        ('Mats, Lights, books, etc', 'Mats, Lights, books, etc'),
        
        # OPX - Consumables
        ('Cartridge', 'Cartridge'),
        ('Paper', 'Paper'),
        ('Pen', 'Pen'),
        ('Electronic items', 'Electronic items'),
        ('Computer consumables', 'Computer consumables'),
        ('Paints, cloths, stitching items', 'Paints, cloths, stitching items'),
        ('Raw materials', 'Raw materials'),
        
        # OPX - Training expenses
        ('Venue hire', 'Venue hire'),
        ('Audio-visual rent', 'Audio-visual rent'),
        ('Refreshment', 'Refreshment'),
        ('Registration kits', 'Registration kits'),
        
        # OPX - Advertisement & Promotion
        ('Banners and other printing materials', 'Banners and other printing materials'),
        ('Gifts', 'Gifts'),
        
        # OPX - Other operational expenses
        ('Bank charge', 'Bank charge'),
        ('Audit expenses', 'Audit expenses'),
        ('Outsourcing', 'Outsourcing'),
        ('Loan repayment', 'Loan repayment'),
        ('Others', 'Others'),
    ]
    
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.CharField(max_length=100)  # Increased max_length for longer category names
    remarks = models.TextField(blank=True, null=True)
    voucher_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    from_party = models.CharField(max_length=100, blank=True, null=True)
    to_party = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    
    # New fields for enhanced requirements
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES, blank=True, null=True, help_text="Purpose of transaction")
    payee_recipient_name = models.CharField(max_length=200, blank=True, null=True, help_text="Payee/Recipient Name (actual person name)")
    value_date = models.DateField(blank=True, null=True, help_text="Value Date from bank statement")
    description = models.TextField(blank=True, null=True, help_text="Description from bank statement")
    cheque_number = models.CharField(max_length=50, blank=True, null=True, help_text="Cheque/Reference Number")
    branch_code = models.CharField(max_length=20, blank=True, null=True, help_text="Branch Code")
    balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text="Account balance after transaction")
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.voucher_number} - {self.type} - {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.voucher_number or self.voucher_number == '':
            self.voucher_number = self.generate_voucher_number()
        super().save(*args, **kwargs)
    
    def generate_voucher_number(self):
        """Generate voucher number in format V/YY-YY/Month/No"""
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
        
        # Get month name
        month_names = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
        month_name = month_names[month - 1]
        
        # Find the next number for this financial year and month
        last_transaction = Transaction.objects.filter(
            voucher_number__startswith=f"V/{fy_string}/{month_name}/"
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
        
        # Format as V/YY-YY/Month/No (e.g., V/25-26/Jan/01)
        return f"V/{fy_string}/{month_name}/{str(next_number).zfill(2)}"
    
    @property
    def category_type(self):
        """Return whether this is CAPX or OPX for debit transactions"""
        if self.type == 'Debit':
            capx_categories = [
                'Equipment/Machine',
                'Computer, Laptop, Printer, scanners, etc',
                'Furniture'
            ]
            return 'CAPX' if self.category in capx_categories else 'OPX'
        return None
