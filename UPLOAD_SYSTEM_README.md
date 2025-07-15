# Bank Transaction Upload System

## Overview
This Django module allows users to upload Excel or CSV files containing bank transaction data and manually input additional details for each transaction.

## Features

### 1. File Upload
- **Supported Formats**: Excel (`.xlsx`, `.xls`) and CSV (`.csv`)
- **Required Columns**:
  - `Txn Date` (or `Transaction Date`, `Date`)
  - `Value Date`
  - `Description`
  - `Ref No./Cheque No.`
  - `Branch Code`
  - `Debit`
  - `Credit`
  - `Balance`

### 2. Automatic Processing
- **Transaction Type Detection**: Automatically detects Credit (Income) or Debit (Expenditure) based on Credit/Debit columns
- **Category Assignment**: Pre-assigns categories based on transaction type
- **Duplicate Detection**: Prevents duplicate transactions

### 3. Manual Input Interface
- **Purpose Field**: Users can input the purpose of each transaction
- **Payee/Recipient Name**: Users can specify who received or paid the money
- **Category Selection**: Users can change the pre-assigned category if needed

### 4. Voucher Number Generation
- **Format**: `V/YY-YY/MM/XX` (e.g., `V/25-26/Jan/01`)
- **Automatic**: Generated based on financial year and month
- **Unique**: Each transaction gets a unique voucher number

## Usage

### 1. Access the Upload Interface
Navigate to: `http://localhost:8000/api/upload-interface/`

### 2. Upload Process
1. **Step 1**: Upload your Excel/CSV file
   - Drag and drop or click to select file
   - Supported formats: `.xlsx`, `.xls`, `.csv`

2. **Step 2**: Review and Complete Transaction Details
   - Review each parsed transaction
   - Fill in Purpose and Payee/Recipient Name
   - Adjust category if needed
   - Click "Save All Transactions"

### 3. API Endpoints

#### File Upload
```
POST /api/upload/
```
Returns parsed transaction data for manual review.

#### Save Transactions
```
POST /api/save-transactions/
```
Saves transactions after manual input.

#### Get Transactions
```
GET /api/transactions/
```
Retrieve all transactions with optional filtering.

## Database Schema

### Transaction Model Fields
- `date`: Transaction date
- `type`: Credit or Debit
- `amount`: Transaction amount
- `category`: Predefined category
- `remarks`: Description from bank statement
- `purpose`: Manual input - purpose of transaction
- `payee_recipient_name`: Manual input - who received/paid
- `voucher_number`: Auto-generated unique identifier
- `from_party`: For Credit transactions
- `to_party`: For Debit transactions
- `reference_number`: Cheque/Reference number
- `description`: Description from bank statement
- `value_date`: Value date from bank statement
- `cheque_number`: Cheque number
- `branch_code`: Branch code
- `balance`: Account balance after transaction

## Categories

### Credit Categories
- Corpus, CSR, Grants, Membership fees, Registration fees, Loans, Donation, Others

### Debit Categories
- **Programmatic**: Education, Empowerment, Environment, Innovation
- **CAPX**: Equipment/Machine, Computer/Laptop/Printer, Furniture
- **OPX**: Salaries, Stipends, Honorarium, Rent, Maintenance, Transport, etc.

## Installation and Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

4. **Access the Interface**
   - Open: `http://localhost:8000/api/upload-interface/`

## File Format Example

Your Excel/CSV file should have columns like this:

| Txn Date | Value Date | Description | Ref No./Cheque No. | Branch Code | Debit | Credit | Balance |
|----------|------------|-------------|-------------------|-------------|-------|--------|---------|
| 2025-01-15 | 2025-01-15 | Salary Payment | CHQ001 | BR001 | 50000 | | 150000 |
| 2025-01-16 | 2025-01-16 | Grant Received | | BR001 | | 100000 | 250000 |

## Error Handling

The system handles various error scenarios:
- Invalid file formats
- Missing required columns
- Invalid date formats
- Duplicate transactions
- Database errors

## Testing

Run the test script to verify the system:
```bash
python test_upload_system.py
```

## Notes

- The system automatically generates voucher numbers in the format `V/YY-YY/MM/XX`
- Duplicate transactions (same date, amount, and description) are automatically skipped
- All manual inputs (Purpose, Payee/Recipient) are preserved in the database
- The interface supports both Credit and Debit transactions with appropriate category options 