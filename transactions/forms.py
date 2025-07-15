from django import forms
from .models import Transaction

class TransactionManualInputForm(forms.ModelForm):
    """Form for manual input of Purpose and Payee/Recipient Name"""
    
    class Meta:
        model = Transaction
        fields = ['purpose', 'payee_recipient_name', 'category']
        widgets = {
            'purpose': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select purpose...'
            }),
            'payee_recipient_name': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select payee/recipient...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class BulkTransactionForm(forms.Form):
    """Form for bulk editing multiple transactions"""
    
    def __init__(self, transactions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for transaction in transactions:
            # Purpose field - dropdown
            self.fields[f'purpose_{transaction.id}'] = forms.ChoiceField(
                choices=Transaction.PURPOSE_CHOICES,
                required=False,
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'placeholder': 'Select purpose...'
                }),
                initial=transaction.purpose
            )
            
            # Payee/Recipient field - dropdown
            self.fields[f'payee_{transaction.id}'] = forms.ChoiceField(
                choices=Transaction.PAYEE_RECIPIENT_CHOICES,
                required=False,
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'placeholder': 'Select payee/recipient...'
                }),
                initial=transaction.payee_recipient_name
            )
            
            # Category field
            if transaction.type == 'Credit':
                choices = Transaction.CREDIT_CATEGORIES
            else:
                choices = Transaction.DEBIT_CATEGORIES
                
            self.fields[f'category_{transaction.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.Select(attrs={
                    'class': 'form-control'
                }),
                initial=transaction.category
            ) 