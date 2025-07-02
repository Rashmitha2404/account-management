from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Max
from django.http import JsonResponse
import pandas as pd
import io
from .models import Transaction
from .serializers import TransactionSerializer, TransactionListSerializer
from datetime import datetime
import re

# Create your views here.

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
        """Handle file upload and process transactions"""
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
            
            # Normalize column names (remove extra spaces, convert to lowercase)
            df.columns = df.columns.str.strip().str.lower()
            print("Normalized columns:", df.columns.tolist())
            
            # More flexible column mapping including user's specific format
            column_mapping = {
                # Date variations
                'date': 'date',
                'transaction date': 'date',
                'txn date': 'date',
                'txn date': 'date',
                
                # Type variations
                'type': 'type',
                'transaction type': 'type',
                'txn type': 'type',
                'credit/debit': 'type',
                'credit or debit': 'type',
                
                # Amount variations
                'amount': 'amount',
                'transaction amount': 'amount',
                'txn amount': 'amount',
                'value': 'amount',
                'sum': 'amount',
                
                # Category variations
                'category': 'category',
                'transaction category': 'category',
                'txn category': 'category',
                'classification': 'category',
                
                # Remarks variations
                'purpose/remarks': 'remarks',
                'remarks': 'remarks',
                'purpose': 'remarks',
                'description': 'remarks',
                'note': 'remarks',
                'comments': 'remarks',
                'details': 'remarks',
                
                # Voucher variations
                'voucher number': 'voucher_number',
                'vouchernumber': 'voucher_number',
                'voucher': 'voucher_number',
                'voucher no': 'voucher_number',
                'voucher no.': 'voucher_number',
                'vou no': 'voucher_number',
            }
            
            # Rename columns if they exist
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})
            
            print("After mapping columns:", df.columns.tolist())
            
            # Process each row
            created_count = 0
            errors = []
            skipped_count = 0
            
            # --- Prepare to continue serial numbers from DB for each FY ---
            existing_max_serial = {}
            fy_counters = {}

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
                        date_val = row.get('txn date', '')
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
                    
                    # Parse category and remarks
                    category = str(row.get('category', '')).strip()
                    if pd.isna(category) or category == '':
                        # Try alternative category column
                        category = str(row.get('description.1', '')).strip()
                        if pd.isna(category):
                            category = 'Others'
                    
                    remarks = str(row.get('remarks', '')).strip()
                    if pd.isna(remarks) or remarks == '':
                        # Try alternative remarks column
                        remarks = str(row.get('description', '')).strip()
                        if pd.isna(remarks):
                            remarks = ''
                    
                    # Map 'Person received/paid' and 'Ref No./Cheque No.'
                    person = str(row.get('person received/paid', '')).strip()
                    ref_no = str(row.get('ref no./cheque no.', '')).strip()
                    from_party = ''
                    to_party = ''
                    if transaction_type == 'Credit':
                        from_party = person
                    elif transaction_type == 'Debit':
                        to_party = person
                    reference_number = ref_no
                    
                    # --- Check for duplicate transaction before creating ---
                    # Look for existing transaction with same date, amount, and description
                    existing_transaction = Transaction.objects.filter(
                        date=date,
                        amount=amount,
                        remarks=remarks
                    ).first()
                    
                    if existing_transaction:
                        # Skip this transaction as it already exists
                        skipped_count += 1
                        continue
                    
                    # --- Generate voucher number with DB-aware serial ---
                    # Determine financial year
                    year = date.year
                    month = date.month
                    if month >= 4:
                        fy_start = year
                        fy_end = year + 1
                    else:
                        fy_start = year - 1
                        fy_end = year
                    fy_string = f"{str(fy_start)[-2:]}-{str(fy_end)[-2:]}"

                    # Get max serial for this FY from DB if not already cached
                    if fy_string not in existing_max_serial:
                        last_voucher = (
                            Transaction.objects
                            .filter(voucher_number__startswith=f"V/{fy_string}/")
                            .order_by('-voucher_number')
                            .first()
                        )
                        if last_voucher:
                            m = re.match(r"V/\d{2}-\d{2}/(\d+)", last_voucher.voucher_number)
                            if m:
                                last_serial = int(m.group(1))
                            else:
                                last_serial = 0
                        else:
                            last_serial = 0
                        existing_max_serial[fy_string] = last_serial
                    # Increment for this upload
                    if fy_string not in fy_counters:
                        fy_counters[fy_string] = existing_max_serial[fy_string]
                    fy_counters[fy_string] += 1
                    serial = fy_counters[fy_string]
                    voucher_number = f"V/{fy_string}/{str(serial).zfill(2)}"
                    
                    # Create transaction
                    transaction = Transaction.objects.create(
                        date=date,
                        type=transaction_type,
                        amount=amount,
                        category=category,
                        remarks=remarks,
                        voucher_number=voucher_number,
                        from_party=from_party,
                        to_party=to_party,
                        reference_number=reference_number
                    )
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            return Response({
                'message': f'Success! {created_count} transactions uploaded. {skipped_count} duplicates skipped. Errors: {", ".join(errors)}' if errors else f'Success! {created_count} transactions uploaded. {skipped_count} duplicates skipped.',
                'created_count': created_count,
                'skipped_count': skipped_count,
                'errors': errors
            }, status=201)
            
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
