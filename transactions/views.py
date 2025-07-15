from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Max
from django.http import JsonResponse, HttpResponse
import pandas as pd
import io
from .models import Transaction
from .serializers import TransactionSerializer, TransactionListSerializer
from datetime import datetime
import re
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import models
import os
from django.conf import settings
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import models
import os
from django.conf import settings
from django.utils import timezone
from .forms import TransactionManualInputForm, BulkTransactionForm

# Create your views here.

def upload_interface(request):
    """Main upload interface view"""
    context = {
        'credit_categories': json.dumps(Transaction.CREDIT_CATEGORIES),
        'debit_categories': json.dumps(Transaction.DEBIT_CATEGORIES),
        'purpose_categories': json.dumps(Transaction.PURPOSE_CHOICES),
        'payee_categories': json.dumps(Transaction.PAYEE_RECIPIENT_CHOICES),
    }
    return render(request, 'transactions/upload.html', context)

class TransactionListView(APIView):
    def get(self, request):
        """Get transactions with optional filtering"""
        transactions = Transaction.objects.all().order_by('date', 'created_at')
        
        # Apply filters
        transaction_type = request.query_params.get('type', None)
        category = request.query_params.get('category', None)
        month = request.query_params.get('month', None)
        year = request.query_params.get('year', None)
        
        if transaction_type:
            transactions = transactions.filter(type=transaction_type)
        if category:
            transactions = transactions.filter(category=category)
        if month:
            transactions = transactions.filter(date__month=month)
        if year:
            transactions = transactions.filter(date__year=year)
        
        serializer = TransactionListSerializer(transactions, many=True)
        return Response(serializer.data)

class FileUploadView(APIView):
    def post(self, request):
        """Handle file upload and process transactions - returns parsed data for manual review"""
        try:
            file = request.FILES.get('file')
            if not file:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Read the file
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Debug: Print original column names
            print("Original columns:", df.columns.tolist())
            
            # More flexible column mapping including user's specific format
            column_mapping = {
                # Date variations - handle exact case
                'Txn Date': 'date',
                'txn date': 'date',
                'date': 'date',
                'transaction date': 'date',
                
                # Value date
                'Value Date': 'value_date',
                'value date': 'value_date',
                
                # Description
                'Description': 'description',
                'description': 'description',
                
                # Reference/Cheque
                'Ref No./Cheque No.': 'reference_number',
                'ref no./cheque no.': 'reference_number',
                'reference': 'reference_number',
                'cheque': 'reference_number',
                
                # Branch code
                'Branch Code': 'branch_code',
                'branch code': 'branch_code',
                'branch': 'branch_code',
                
                # Debit and Credit
                'Debit': 'debit',
                'debit': 'debit',
                'Credit': 'credit',
                'credit': 'credit',
                
                # Balance
                'Balance': 'balance',
                'balance': 'balance',
                
                # Legacy mappings for backward compatibility
                'type': 'type',
                'transaction type': 'type',
                'txn type': 'type',
                'credit/debit': 'type',
                'credit or debit': 'type',
                'amount': 'amount',
                'transaction amount': 'amount',
                'txn amount': 'amount',
                'value': 'amount',
                'sum': 'amount',
                'category': 'category',
                'transaction category': 'category',
                'txn category': 'category',
                'classification': 'category',
                'purpose/remarks': 'remarks',
                'remarks': 'remarks',
                'purpose': 'remarks',
                'note': 'remarks',
                'comments': 'remarks',
                'details': 'remarks',
                'voucher number': 'voucher_number',
                'vouchernumber': 'voucher_number',
                'voucher': 'voucher_number',
                'voucher no': 'voucher_number',
                'voucher no.': 'voucher_number',
                'vou no': 'voucher_number',
            }
            
            # Rename columns if they exist (preserve original case)
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})
            
            print("After mapping columns:", df.columns.tolist())
            
            # Process each row
            parsed_transactions = []
            errors = []
            person_names = set()  # Collect unique person names from Excel
            
            for index, row in df.iterrows():
                try:
                    # Handle the specific format from user's file
                    # Check if this is a credit or debit transaction
                    debit_amount = row.get('debit', 0)
                    credit_amount = row.get('credit', 0)
                    
                    # Determine transaction type and amount
                    if pd.notna(credit_amount) and credit_amount > 0:
                        transaction_type = 'Credit'
                        amount = float(credit_amount)
                    elif pd.notna(debit_amount) and debit_amount > 0:
                        transaction_type = 'Debit'
                        amount = float(debit_amount)
                    else:
                        errors.append(f"Row {index + 1}: No valid amount found (both debit and credit are empty or zero)")
                        continue
                    
                    # Parse date
                    date_val = row.get('date', '')
                    if pd.isna(date_val) or date_val == '':
                        errors.append(f"Row {index + 1}: Missing date")
                        continue
                    try:
                        if isinstance(date_val, str):
                            date = pd.to_datetime(date_val).date()
                        else:
                            date = date_val.date()
                    except:
                        errors.append(f"Row {index + 1}: Invalid date format '{date_val}'")
                        continue
                    
                    # Parse description and remarks
                    description = str(row.get('description', '')).strip()
                    if pd.isna(description) or description == '':
                        description = 'No description'
                    
                    # Extract person names from description or other relevant fields
                    # Look for patterns like "Payment to John Doe" or "Received from Jane Smith"
                    person_name = ''
                    
                    # Try to extract names from description
                    if description:
                        # Common patterns in bank descriptions
                        patterns = [
                            r'to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # "to John Doe"
                            r'from\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # "from Jane Smith"
                            r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',    # "by Ram Kumar"
                            r'for\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',   # "for Amit Patel"
                        ]
                        
                        for pattern in patterns:
                            match = re.search(pattern, description, re.IGNORECASE)
                            if match:
                                person_name = match.group(1).strip()
                                break
                    
                    # If no name found in description, try to extract from other fields
                    if not person_name:
                        # Check if there's a "Person received/paid" column
                        person_field = row.get('person received/paid', '')
                        if pd.notna(person_field) and str(person_field).strip():
                            person_name = str(person_field).strip()
                    
                    # Add to person names set if found
                    if person_name:
                        person_names.add(person_name)
                    
                    # Parse reference number
                    reference_number = str(row.get('reference_number', '')).strip()
                    if pd.isna(reference_number):
                        reference_number = ''
                    
                    # Parse branch code
                    branch_code = str(row.get('branch_code', '')).strip()
                    if pd.isna(branch_code):
                        branch_code = ''
                    
                    # Parse balance
                    balance = row.get('balance', None)
                    if pd.isna(balance):
                        balance = None
                    else:
                        balance = float(balance)
                    
                    # Parse value date
                    value_date_val = row.get('value_date', date_val)
                    if pd.isna(value_date_val) or value_date_val == '':
                        value_date = date
                    else:
                        try:
                            if isinstance(value_date_val, str):
                                value_date = pd.to_datetime(value_date_val).date()
                            else:
                                value_date = value_date_val.date()
                        except:
                            value_date = date
                    
                    # Set default category based on transaction type
                    if transaction_type == 'Credit':
                        category = 'CSR'  # Default for credits
                    else:
                        category = 'Others'  # Default for debits
                    
                    # Create transaction data for manual review
                    transaction_data = {
                        'date': date.isoformat(),
                        'type': transaction_type,
                        'amount': amount,
                        'category': category,
                        'remarks': description,
                        'from_party': '',  # Will be filled manually
                        'to_party': '',    # Will be filled manually
                        'reference_number': reference_number,
                        'description': description,
                        'purpose': '',  # Will be filled manually
                        'payee_recipient_name': person_name,  # Pre-filled with extracted name
                        'value_date': value_date.isoformat(),
                        'cheque_number': reference_number,
                        'branch_code': branch_code,
                        'balance': balance,
                    }
                    
                    parsed_transactions.append(transaction_data)
                    
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            # Convert person names to list for dropdown
            person_names_list = sorted(list(person_names))
            
            return Response({
                'success': True,
                'transactions': parsed_transactions,
                'errors': errors,
                'total_parsed': len(parsed_transactions),
                'person_names': person_names_list  # Send extracted names for dropdown
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def save_transactions(request):
    """Save transactions after manual review and input"""
    try:
        transactions_data = json.loads(request.POST.get('transactions', '[]'))
        created_count = 0
        skipped_count = 0
        errors = []
        
        for index, transaction_data in enumerate(transactions_data):
            try:
                # Get manual inputs from form
                purpose = request.POST.get(f'purpose_{index}', '')
                payee_recipient = request.POST.get(f'payee_{index}', '')
                manual_payee = request.POST.get(f'payee_manual_{index}', '')
                category = request.POST.get(f'category_{index}', 'Others')
                
                # Use manual input if "Other" was selected
                if payee_recipient == 'Other' and manual_payee:
                    payee_recipient = manual_payee
                
                # Parse date
                date = datetime.strptime(transaction_data['date'], '%Y-%m-%d').date()
                
                # Check for duplicate transaction
                existing_transaction = Transaction.objects.filter(
                    date=date,
                    amount=transaction_data['amount'],
                    remarks=transaction_data['remarks']
                ).first()
                
                if existing_transaction:
                    skipped_count += 1
                    continue
                
                # Create transaction (voucher number will be auto-generated)
                transaction = Transaction.objects.create(
                    date=date,
                    type=transaction_data['type'],
                    amount=transaction_data['amount'],
                    category=category,
                    remarks=transaction_data['remarks'],
                    purpose=purpose,
                    payee_recipient_name=payee_recipient,
                    from_party=transaction_data.get('from_party', ''),
                    to_party=transaction_data.get('to_party', ''),
                    reference_number=transaction_data.get('reference_number', ''),
                    description=transaction_data.get('description', ''),
                    value_date=date,  # Use same date for now
                    cheque_number=transaction_data.get('cheque_number', ''),
                    branch_code=transaction_data.get('branch_code', ''),
                    balance=transaction_data.get('balance'),
                )
                created_count += 1
                
            except Exception as e:
                errors.append(f"Transaction {index + 1}: {str(e)}")
        
        return Response({
            'success': True,
            'created_count': created_count,
            'skipped_count': skipped_count,
            'errors': errors
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def analytics_view(request):
    """Get analytics data for dashboard"""
    try:
        # Get date range filters
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        transactions = Transaction.objects.all()
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        
        # Credit categories
        credit_data = transactions.filter(type='Credit').values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        credit_categories = {
            'labels': [item['category'] for item in credit_data],
            'datasets': [{
                'data': [float(item['total']) for item in credit_data],
                'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384']
            }]
        }
        
        # Debit categories
        debit_data = transactions.filter(type='Debit').values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        debit_categories = {
            'labels': [item['category'] for item in debit_data],
            'datasets': [{
                'data': [float(item['total']) for item in debit_data],
                'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
            }]
        }
        
        # Monthly trends
        monthly_data = transactions.extra(
            select={'month': "EXTRACT(month FROM date)", 'year': "EXTRACT(year FROM date)"}
        ).values('month', 'year', 'type').annotate(
            total=Sum('amount')
        ).order_by('year', 'month')
        
        # Process monthly data for chart
        months = []
        credits = []
        debits = []
        
        for item in monthly_data:
            month_year = f"{int(item['year'])}-{int(item['month']):02d}"
            if month_year not in months:
                months.append(month_year)
                credits.append(0)
                debits.append(0)
            
            idx = months.index(month_year)
            if item['type'] == 'Credit':
                credits[idx] = float(item['total'])
            else:
                debits[idx] = float(item['total'])
        
        monthly_trends = {
            'labels': months,
            'datasets': [
                {
                    'label': 'Credits',
                    'data': credits,
                    'backgroundColor': '#36A2EB'
                },
                {
                    'label': 'Debits', 
                    'data': debits,
                    'backgroundColor': '#FF6384'
                }
            ]
        }
        
        return Response({
            'creditCategories': credit_categories,
            'debitCategories': debit_categories,
            'monthly': monthly_trends
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Keep the existing upload_file function for backward compatibility
@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        file = request.FILES['file']
        # Check file extension
        if not file.name.endswith(('.xlsx', '.xls', '.csv')):
            return JsonResponse({'error': 'Please upload Excel or CSV file'}, status=400)
        # Read the file
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        # Lowercase columns for robust detection
        lower_cols = [str(col).strip().lower() for col in df.columns]
        # RELF/bank format detection: look for any of these columns
        relf_cols = [
            'txn date', 'transaction date', 'value date', 'description', 'ref no./cheque no.',
            'debit', 'credit', 'balance', 'branch code', 'branch'
        ]
        is_relf_format = any(any(relf_col in col for col in lower_cols) for relf_col in relf_cols)
        if is_relf_format:
            print("Detected RELF/bank statement format")
            return process_relf_data(df)
        else:
            return process_standard_data(df)
    except Exception as e:
        return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=500)

def process_relf_data(df):
    """Process RELF account data format with robust column mapping and duplicate prevention"""
    try:
        import re
        # Clean the data - remove rows with all NaN values
        df = df.dropna(how='all')

        # Flexible column mapping
        col_map = {
            'txn_date': ['txn date', 'transaction date', 'date'],
            'value_date': ['value date'],
            'description': ['description', 'narration', 'particulars'],
            'ref_no': ['ref no./cheque no.', 'ref no', 'cheque no', 'reference', 'reference number'],
            'branch_code': ['branch code', 'branch'],
            'debit': ['debit', 'withdrawal', 'withdrawals'],
            'credit': ['credit', 'deposit', 'deposits'],
            'balance': ['balance', 'closing balance', 'running balance'],
        }
        # Lowercase columns for matching
        df.columns = [str(col).strip().lower() for col in df.columns]
        # Build a mapping from standard name to actual column name
        actual_cols = {}
        for std, options in col_map.items():
            for opt in options:
                for col in df.columns:
                    if re.sub(r'[^a-z]', '', col) == re.sub(r'[^a-z]', '', opt):
                        actual_cols[std] = col
                        break
                if std in actual_cols:
                    break

        # Find the actual data rows (skip header rows)
        data_start_idx = None
        for idx, row in df.iterrows():
            if pd.notna(row.get(actual_cols.get('txn_date', 'txn date'))) and pd.notna(row.get(actual_cols.get('description', 'description'))):
                data_start_idx = idx
                break
        if data_start_idx is None:
            return JsonResponse({'error': 'No valid transaction data found'}, status=400)
        # Extract only the data rows
        df = df.iloc[data_start_idx:].reset_index(drop=True)
        print(f"Total rows in DataFrame: {len(df)}")
        print(f"DataFrame columns: {list(df.columns)}")
        print(f"First few rows:")
        for i in range(min(5, len(df))):
            print(f"  Row {i}: {dict(df.iloc[i])}")

        transactions_created = 0
        errors = []
        from transactions.models import Transaction
        
        # Clear existing transactions for clean test
        Transaction.objects.all().delete()
        print(f"Cleared existing transactions. Starting to process {len(df)} rows...")
        
        for index, row in df.iterrows():
            try:
                # Get date - handle different date formats
                date_val = row.get('Txn Date')
                if pd.isna(date_val):
                    print(f"Row {index + 1}: Skipping - no date")
                    continue
                
                try:
                    if isinstance(date_val, str):
                        date = pd.to_datetime(date_val).date()
                    else:
                        date = date_val.date()
                except Exception as e:
                    print(f"Row {index + 1}: Date parsing error - {e}")
                    continue
                
                # Get debit and credit amounts
                debit_amount = row.get('Debit', 0)
                credit_amount = row.get('Credit', 0)
                
                # Convert to float, handle NaN
                try:
                    debit_amount = float(debit_amount) if pd.notna(debit_amount) else 0.0
                except:
                    debit_amount = 0.0
                    
                try:
                    credit_amount = float(credit_amount) if pd.notna(credit_amount) else 0.0
                except:
                    credit_amount = 0.0
                
                print(f"Row {index + 1}: Debit={debit_amount} Credit={credit_amount}")
                
                # Determine transaction type
                if debit_amount > 0:
                    transaction_type = 'Debit'
                    amount = debit_amount
                elif credit_amount > 0:
                    transaction_type = 'Credit'
                    amount = credit_amount
                else:
                    print(f"Row {index + 1}: Skipping - no amount")
                    continue
                
                # Get description and reference
                description = str(row.get('Description', ''))
                ref_no = str(row.get('Ref No./Cheque No.', ''))
                branch_code = str(row.get('Branch Code', ''))
                balance = row.get('Balance', 0)
                
                print(f"Row {index + 1}: Saving {transaction_type} {amount} on {date}")
                
                # Create transaction
                transaction = Transaction(
                    date=date,
                    type=transaction_type,
                    amount=amount,
                    category='Others',
                    remarks=description,
                    description=description,
                    reference_number=ref_no,
                    cheque_number=ref_no,
                    branch_code=branch_code,
                    balance=float(balance) if pd.notna(balance) else None,
                    from_party='',
                    to_party='',
                    purpose=''
                )
                transaction.save()
                transactions_created += 1
                
            except Exception as e:
                print(f"Row {index + 1}: ERROR - {e}")
                errors.append(f"Row {index + 1}: {str(e)}")
        return JsonResponse({
            'message': f'Successfully processed {transactions_created} transactions',
            'transactions_created': transactions_created,
            'errors': errors
        })
    except Exception as e:
        return JsonResponse({'error': f'Error processing RELF data: {str(e)}'}, status=500)

def process_standard_data(df):
    """Process standard Excel/CSV format"""
    try:
        # Standard column mapping
        column_mapping = {
            'date': ['date', 'transaction date', 'txn date'],
            'type': ['type', 'transaction type', 'credit/debit'],
            'amount': ['amount', 'transaction amount', 'value'],
            'category': ['category', 'transaction category', 'classification'],
            'remarks': ['remarks', 'purpose', 'description'],
            'from_party': ['from', 'from party', 'payer'],
            'to_party': ['to', 'to party', 'payee'],
            'reference_number': ['reference', 'ref no', 'reference number']
        }
        
        # Rename columns to standard format
        for standard_col, possible_names in column_mapping.items():
            for old_col in possible_names:
                if old_col in df.columns:
                    df = df.rename(columns={old_col: standard_col})
                    break
        
        # Validate required columns
        required_columns = ['date', 'type', 'amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return JsonResponse({
                'error': f'Missing required columns: {missing_columns}'
            }, status=400)
        
        transactions_created = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Parse date
                if isinstance(row['date'], str):
                    date = pd.to_datetime(row['date']).date()
                else:
                    date = row['date'].date()
                
                # Validate transaction type
                transaction_type = row['type'].strip().title()
                if transaction_type not in ['Credit', 'Debit']:
                    errors.append(f"Row {index + 1}: Invalid transaction type '{transaction_type}'")
                    continue
                
                # Parse amount
                amount = float(row['amount'])
                
                # Get category (default to 'Others' if not provided)
                category = row.get('category', 'Others')
                if pd.isna(category):
                    category = 'Others'
                
                # Create transaction
                transaction = Transaction(
                    date=date,
                    type=transaction_type,
                    amount=amount,
                    category=category,
                    remarks=row.get('remarks', ''),
                    from_party=row.get('from_party', ''),
                    to_party=row.get('to_party', ''),
                    reference_number=row.get('reference_number', '')
                )
                transaction.save()
                transactions_created += 1
                
            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")
        
        return JsonResponse({
            'message': f'Successfully processed {transactions_created} transactions',
            'transactions_created': transactions_created,
            'errors': errors
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Error processing standard data: {str(e)}'}, status=500)

@api_view(['GET'])
def get_transactions(request):
    try:
        # Get filter parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        transaction_type = request.GET.get('type')
        category = request.GET.get('category')
        
        # Build query
        queryset = Transaction.objects.all()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)
        if category:
            queryset = queryset.filter(category=category)
        
        # Serialize data
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_analytics(request):
    try:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        queryset = Transaction.objects.all()
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        credit_data = queryset.filter(type='Credit')
        debit_data = queryset.filter(type='Debit')
        # By category (sum of amount)
        credit_by_category = {}
        for item in credit_data.values('category').annotate(total=Sum('amount')):
            key = str(item['category']) if item['category'] else 'Unknown'
            credit_by_category[key] = float(item['total'] or 0)
        debit_by_category = {}
        for item in debit_data.values('category').annotate(total=Sum('amount')):
            key = str(item['category']) if item['category'] else 'Unknown'
            debit_by_category[key] = float(item['total'] or 0)
        # By month (sum of amount)
        credit_by_month = {}
        for item in credit_data.values('date').annotate(total=Sum('amount')):
            if item['date']:
                month = item['date'].strftime('%Y-%m')
                credit_by_month[month] = credit_by_month.get(month, 0) + float(item['total'] or 0)
        debit_by_month = {}
        for item in debit_data.values('date').annotate(total=Sum('amount')):
            if item['date']:
                month = item['date'].strftime('%Y-%m')
                debit_by_month[month] = debit_by_month.get(month, 0) + float(item['total'] or 0)
        # By year (sum of amount)
        credit_by_year = {}
        for item in credit_data.values('date').annotate(total=Sum('amount')):
            if item['date']:
                year = str(item['date'].year)
                credit_by_year[year] = credit_by_year.get(year, 0) + float(item['total'] or 0)
        debit_by_year = {}
        for item in debit_data.values('date').annotate(total=Sum('amount')):
            if item['date']:
                year = str(item['date'].year)
                debit_by_year[year] = debit_by_year.get(year, 0) + float(item['total'] or 0)
        analytics = {
            'credit': {
                'total': float(credit_data.aggregate(Sum('amount'))['amount__sum'] or 0),
                'count': credit_data.count(),
                'by_category': credit_by_category,
                'by_month': credit_by_month,
                'by_year': credit_by_year
            },
            'debit': {
                'total': float(debit_data.aggregate(Sum('amount'))['amount__sum'] or 0),
                'count': debit_data.count(),
                'by_category': debit_by_category,
                'by_month': debit_by_month,
                'by_year': debit_by_year,
                'by_category_type': {}
            }
        }
        # Remove CAPX/OPX aggregation and restore previous analytics logic
        # (No by_category_type calculation)
        # The rest of the analytics code remains unchanged.
        return Response(analytics)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def export_transactions(request):
    print(f"=== EXPORT TRANSACTIONS CALLED ===")
    print(f"Request path: {request.path}")
    print(f"Request GET params: {request.GET}")
    print(f"Request method: {request.method}")
    print(f"Request URL: {request.build_absolute_uri()}")
    print(f"Request GET dict: {dict(request.GET)}")
    print(f"Query string: {request.META.get('QUERY_STRING', '')}")
    
    try:
        # Get filter parameters - handle both single and multiple values
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        transaction_type = request.GET.get('type')
        category = request.GET.get('category')
        export_format = request.GET.get('format', 'excel')
        
        print(f"Export format: {export_format}")
        print(f"Start date: {start_date}")
        print(f"End date: {end_date}")
        print(f"Transaction type: {transaction_type}")
        print(f"Category: {category}")
        
        # Build query with filters
        query = Transaction.objects.all()
        
        if start_date:
            query = query.filter(date__gte=start_date)
        if end_date:
            query = query.filter(date__lte=end_date)
        if transaction_type:
            query = query.filter(type=transaction_type)
        if category:
            query = query.filter(category=category)
        
        # Convert to list for serialization
        transactions = list(query)
        print(f"Query count: {len(transactions)}")
        
        # Serialize data
        serialized_data = []
        for transaction in transactions:
            serialized_data.append({
                'date': transaction.date.strftime('%Y-%m-%d'),
                'type': transaction.type,
                'amount': float(transaction.amount),
                'category': transaction.category,
                'voucher_number': getattr(transaction, 'voucher_number', ''),
                'reference_number': getattr(transaction, 'reference_number', ''),
                'purpose': getattr(transaction, 'purpose', ''),
                'payee_recipient_name': getattr(transaction, 'payee_recipient_name', ''),
                'value_date': transaction.value_date.strftime('%Y-%m-%d') if getattr(transaction, 'value_date', None) else '',
                'description': transaction.description or '',
                'cheque_number': getattr(transaction, 'cheque_number', ''),
                'branch_code': getattr(transaction, 'branch_code', ''),
                'balance': float(transaction.balance) if getattr(transaction, 'balance', None) is not None else '',
                'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S') if getattr(transaction, 'created_at', None) else '',
                'updated_at': transaction.updated_at.strftime('%Y-%m-%d %H:%M:%S') if getattr(transaction, 'updated_at', None) else '',
            })
        
        print(f"Serialized data count: {len(serialized_data)}")
        
        print(f"About to check export format: {export_format}")
        if export_format.lower() == 'excel':
            print("Generating Excel report...")
            try:
                result = generate_excel_report(serialized_data)
                print("Excel report generated successfully")
                return result
            except Exception as excel_error:
                print(f"Error generating Excel report: {str(excel_error)}")
                import traceback
                traceback.print_exc()
                return Response({'error': f'Excel generation failed: {str(excel_error)}'}, status=500)
        elif export_format.lower() == 'pdf':
            print("Generating PDF report...")
            try:
                result = generate_pdf_report(serialized_data)
                print("PDF report generated successfully")
                return result
            except Exception as pdf_error:
                print(f"Error generating PDF report: {str(pdf_error)}")
                import traceback
                traceback.print_exc()
                return Response({'error': f'PDF generation failed: {str(pdf_error)}'}, status=500)
        else:
            print(f"Invalid export format: {export_format}")
            return Response({'error': 'Invalid export format'}, status=400)
            
    except Exception as e:
        print(f"Error in export_transactions: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': f'Export failed: {str(e)}'}, status=500)

# Simple test export view
@api_view(['GET'])
def test_export(request):
    """Simple test export to verify URL routing works"""
    print("=== TEST EXPORT CALLED ===")
    return Response({'message': 'Export endpoint is working!'}, status=status.HTTP_200_OK)

def generate_excel_report(data):
    """Generate Excel report with only relevant columns (exclude from_party, to_party, id, name, remarks; use only description for details)"""
    try:
        import pytz
        from datetime import datetime
        # Create DataFrame with all available data
        df = pd.DataFrame(data)

        # Remove 'id', 'name', and 'remarks' columns if present
        for col in ['id', 'name', 'remarks']:
            if col in df.columns:
                df = df.drop(columns=[col])

        # Convert created_at and updated_at to IST and format as 'YYYY-MM-DD HH:MM:SS'
        ist = pytz.timezone('Asia/Kolkata')
        for col in ['created_at', 'updated_at']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], utc=True, errors='coerce').dt.tz_convert(ist).dt.strftime('%Y-%m-%d %H:%M:%S')

        # Define the order of columns for better readability (exclude from_party, to_party, id, name, remarks)
        column_order = [
            'date',
            'type',
            'amount',
            'category',
            'voucher_number',
            'reference_number',
            'purpose',
            'payee_recipient_name',
            'value_date',
            'description',
            'cheque_number',
            'branch_code',
            'balance',
            'created_at',
            'updated_at'
        ]

        # Reorder columns to match the defined order, keeping any additional columns at the end
        available_columns = [col for col in column_order if col in df.columns]
        remaining_columns = [col for col in df.columns if col not in column_order and col not in ['from_party', 'to_party', 'id', 'name', 'remarks']]
        final_columns = available_columns + remaining_columns

        # Reorder the DataFrame
        df = df[final_columns]

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Transactions', index=False)
        output.seek(0)

        # Create response
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="transactions.xlsx"'
        return response
    except Exception as e:
        return Response({'error': f'Error generating Excel: {str(e)}'}, status=500)

def generate_pdf_report(data):
    """Generate PDF report with all available columns"""
    try:
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Add title
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        elements.append(Paragraph("Transaction Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Define column headers for all available fields
        headers = [
            'Date', 'Type', 'Amount', 'Category', 'Voucher No.', 'Remarks',
            'From Party', 'To Party', 'Reference No.', 'Purpose', 
            'Payee/Recipient', 'Value Date', 'Description', 'Cheque No.',
            'Branch Code', 'Balance', 'Created At', 'Updated At'
        ]
        
        # Prepare table data with headers
        table_data = [headers]
        
        for item in data:
            row = [
                item.get('date', ''),
                item.get('type', ''),
                str(item.get('amount', '')),
                item.get('category', ''),
                item.get('voucher_number', ''),
                (item.get('remarks', '')[:30] + '...') if item.get('remarks', '') and len(item.get('remarks', '')) > 30 else item.get('remarks', ''),
                item.get('from_party', ''),
                item.get('to_party', ''),
                item.get('reference_number', ''),
                item.get('purpose', ''),
                item.get('payee_recipient_name', ''),
                item.get('value_date', ''),
                (item.get('description', '')[:30] + '...') if item.get('description', '') and len(item.get('description', '')) > 30 else item.get('description', ''),
                item.get('cheque_number', ''),
                item.get('branch_code', ''),
                str(item.get('balance', '')) if item.get('balance') else '',
                item.get('created_at', ''),
                item.get('updated_at', '')
            ]
            table_data.append(row)
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 6),  # Smaller font for data rows
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        
        # Create response
        from django.http import HttpResponse
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'
        return response
    except Exception as e:
        return Response({'error': f'Error generating PDF: {str(e)}'}, status=500)

@api_view(['GET'])
def export_chart_data(request):
    try:
        # Get filter parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Build query
        queryset = Transaction.objects.all()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Prepare chart data
        chart_data = {
            'credit_categories': {},
            'debit_categories': {},
            'monthly_trends': {},
            'yearly_trends': {}
        }
        
        # Process data
        for transaction in queryset:
            month = transaction.date.strftime('%Y-%m')
            year = transaction.date.year
            
            if transaction.type == 'Credit':
                if transaction.category not in chart_data['credit_categories']:
                    chart_data['credit_categories'][transaction.category] = 0
                chart_data['credit_categories'][transaction.category] += float(transaction.amount)
            else:
                if transaction.category not in chart_data['debit_categories']:
                    chart_data['debit_categories'][transaction.category] = 0
                chart_data['debit_categories'][transaction.category] += float(transaction.amount)
            
            # Monthly trends
            if month not in chart_data['monthly_trends']:
                chart_data['monthly_trends'][month] = {'credit': 0, 'debit': 0}
            chart_data['monthly_trends'][month][transaction.type.lower()] += float(transaction.amount)
            
            # Yearly trends
            if year not in chart_data['yearly_trends']:
                chart_data['yearly_trends'][year] = {'credit': 0, 'debit': 0}
            chart_data['yearly_trends'][year][transaction.type.lower()] += float(transaction.amount)
        
        return Response(chart_data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def test_view(request):
    return HttpResponse("Test view is working!")

def export_test(request):
    print("==== export_test view called ====")
    return HttpResponse("Export test endpoint is working!")

@api_view(['GET'])
def debug_export(request):
    """Debug view to test URL resolution and query parameters"""
    print("=== DEBUG EXPORT CALLED ===")
    print(f"Request path: {request.path}")
    print(f"Request GET params: {request.GET}")
    print(f"Request method: {request.method}")
    print(f"Request URL: {request.build_absolute_uri()}")
    print(f"Request GET dict: {dict(request.GET)}")
    
    return Response({
        'message': 'Debug export endpoint working!',
        'path': request.path,
        'get_params': dict(request.GET),
        'method': request.method,
        'url': request.build_absolute_uri()
    })
