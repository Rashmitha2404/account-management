# Account Management System

A comprehensive accounting management system with Excel/CSV file upload, transaction management, analytics, and export capabilities. The system supports RELF account data format and enhanced categorization with CAPX/OPX classification.

## Features

### 📊 Data Management
- Upload Excel/CSV files with transaction data (including RELF account format)
- Automatic transaction categorization with enhanced categories
- Duplicate detection and prevention
- Enhanced voucher number generation with financial year and month tracking (V/25-26/Jan/01)
- Support for additional fields: Purpose, Payee/Recipient Name, Value Date, Description, Cheque Number, Branch Code, Balance

### 📈 Analytics & Visualization
- **Credit/Debit Category Analysis**: Pie charts showing distribution of income and expenses
- **CAPX vs OPX Analysis**: Capital vs Operational expenditure breakdown
- **Monthly/Yearly Trends**: Bar and line charts for temporal analysis
- **Interactive Charts**: Switch between bar and line chart types
- **Date Range Filtering**: Filter analytics by year and month
- **Enhanced Category Structure**: Organized categories with CAPX/OPX classification

### 📤 Export Capabilities
- **Excel Export**: Download filtered transaction data as Excel files
- **PDF Export**: Generate professional PDF reports with transaction details
- **Chart Data Export**: Export analytics data as JSON for external analysis

### 🎨 Modern UI
- Responsive design with modern styling
- Interactive buttons with hover effects
- Real-time status updates
- Professional color scheme and typography
- Enhanced transaction table with new fields

## Enhanced Transaction Categories

### Credit Categories (Income)
- Corpus
- CSR (Corporate Social Responsibility)
- Grants
- Membership fees
- **Registration fees** (New)
- Loans
- Donation
- Others

### Debit Categories (Expenditure)

#### Programmatic Domains
- Education
- Empowerment
- Environment
- Innovation

#### CAPX (Capital Expenditure)
- Equipment/Machine
- Computer, Laptop, Printer, scanners, etc
- Furniture

#### OPX (Operational Expenditure)

**Human Resource:**
- Salaries to Employees
- Stipends to apprentice
- Honorarium to tutors
- **Honorarium to others** (New)

**Maintenance:**
- Rent of office space
- Maintenance

**Travel:**
- Transport
- Car hire
- Petrol
- Car maintenance

**Educational aid:**
- Digital gadgets
- Stationary items to students
- Mats, Lights, books, etc

**Consumables:**
- Cartridge
- Paper
- Pen
- Electronic items
- Computer consumables
- Paints, cloths, stitching items
- Raw materials

**Training expenses:**
- Venue hire
- Audio-visual rent
- Refreshment
- Registration kits

**Advertisement & Promotion:**
- Banners and other printing materials
- Gifts

**Other operational expenses:**
- Bank charge
- Audit expenses
- Outsourcing
- **Loan repayment** (New)
- Others

## Input File Formats

### Standard Excel/CSV Format
- Date, Type (Credit/Debit), Amount, Category, Remarks, etc.

### RELF Account Data Format
The system now supports RELF account data format with these columns:
- Txn Date, Value Date, Description, Ref No./Cheque No., Branch Code, Debit, Credit, Balance

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or run the batch file:
   ```bash
   install_dependencies.bat
   ```

2. Run Django migrations:
   ```bash
   python manage.py migrate
   ```

3. Start the backend server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

### Uploading Data
1. Prepare your Excel/CSV file with transaction data
2. Supported formats:
   - Standard format: Date, Type (Credit/Debit), Amount, Category, Remarks, etc.
   - RELF format: Txn Date, Value Date, Description, Ref No./Cheque No., Branch Code, Debit, Credit, Balance
3. Click "Choose File" and select your file
4. Click "Upload File" to process the data

### Viewing Analytics
- Use the year and month dropdowns to filter data
- Switch between "Month-wise" and "Year-wise" views
- Choose between "Bar Chart" and "Line Chart" for trends
- View CAPX vs OPX breakdown for debit transactions
- Hover over charts for detailed information

### Exporting Data
- **Export Excel**: Downloads filtered transactions as Excel file
- **Export PDF**: Generates a professional PDF report
- **Export Charts**: Downloads analytics data as JSON

## API Endpoints

- `POST /api/upload/` - Upload Excel/CSV files (supports RELF format)
- `GET /api/transactions/` - Get transactions with filters
- `GET /api/analytics/` - Get analytics data with CAPX/OPX breakdown
- `GET /api/transactions/export/` - Export transactions (Excel/PDF)
- `GET /api/chart-data/export/` - Export chart data (JSON)

## Technologies Used

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- Pandas 2.1.4 (Data processing)
- OpenPyXL 3.1.2 (Excel handling)
- ReportLab 4.0.7 (PDF generation)

### Frontend
- React 19.1.0
- Chart.js 4.5.0
- React-Chartjs-2 5.3.0
- Modern CSS with inline styles

## Key Enhancements

### New Features
1. **RELF Account Data Support**: Automatic detection and processing of RELF format
2. **Enhanced Voucher Numbers**: Format changed to V/25-26/Month/No
3. **CAPX/OPX Classification**: Automatic categorization of capital vs operational expenses
4. **Additional Fields**: Purpose, Payee/Recipient Name, Value Date, Description, Cheque Number, Branch Code, Balance
5. **Enhanced Analytics**: CAPX vs OPX breakdown in charts and reports
6. **Improved UI**: Better styling and user experience

### Technical Improvements
1. **Better Error Handling**: More detailed error messages and validation
2. **Enhanced Data Processing**: Improved handling of different file formats
3. **Scalable Architecture**: Better separation of concerns and modular design
4. **Performance Optimizations**: Efficient data processing and rendering

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.