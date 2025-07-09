import React from "react";

const CREDIT_CATEGORIES = [
  "Corpus",
  "CSR",
  "Grants",
  "Membership fees",
  "Registration fees",
  "Loans",
  "Donation",
  "Others"
];

const DEBIT_CATEGORIES = {
  "Programmatic Domains": [
    "Education",
    "Empowerment",
    "Environment",
    "Innovation"
  ],
  "CAPX (Capital Expenditure)": [
    "Equipment/Machine",
    "Computer, Laptop, Printer, scanners, etc",
    "Furniture"
  ],
  "OPX - Human Resource": [
    "Salaries to Employees",
    "Stipends to apprentice",
    "Honorarium to tutors",
    "Honorarium to others"
  ],
  "OPX - Maintenance": [
    "Rent of office space",
    "Maintenance"
  ],
  "OPX - Travel": [
    "Transport",
    "Car hire",
    "Petrol",
    "Car maintenance"
  ],
  "OPX - Educational aid": [
    "Digital gadgets",
    "Stationary items to students",
    "Mats, Lights, books, etc"
  ],
  "OPX - Consumables": [
    "Cartridge",
    "Paper",
    "Pen",
    "Electronic items",
    "Computer consumables",
    "Paints, cloths, stitching items",
    "Raw materials"
  ],
  "OPX - Training expenses": [
    "Venue hire",
    "Audio-visual rent",
    "Refreshment",
    "Registration kits"
  ],
  "OPX - Advertisement & Promotion": [
    "Banners and other printing materials",
    "Gifts"
  ],
  "OPX - Other operational expenses": [
    "Bank charge",
    "Audit expenses",
    "Outsourcing",
    "Loan repayment",
    "Others"
  ]
};

function Filters({ filters, setFilters }) {
  const handleTypeChange = (e) => {
    const type = e.target.value;
    setFilters(f => ({ ...f, type, category: "" })); // Reset category on type change
  };

  let categoryOptions = null;
  if (filters.type === "Credit") {
    categoryOptions = CREDIT_CATEGORIES.map(cat => (
      <option key={cat} value={cat}>{cat}</option>
    ));
  } else if (filters.type === "Debit") {
    categoryOptions = Object.entries(DEBIT_CATEGORIES).map(([group, cats]) => (
      <optgroup key={group} label={group}>
        {cats.map(cat => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </optgroup>
    ));
  }

  return (
    <div className="filters">
      <div className="filter-row">
        <div className="filter-group">
          <label>Transaction Type:</label>
          <select 
            value={filters.type} 
            onChange={handleTypeChange}
            style={{
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              fontSize: '14px',
              minWidth: '120px'
            }}
          >
            <option value="">All Types</option>
            <option value="Credit">Credit</option>
            <option value="Debit">Debit</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Category:</label>
          <select 
            value={filters.category} 
            onChange={(e) => setFilters(f => ({ ...f, category: e.target.value }))}
            style={{
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              fontSize: '14px',
              minWidth: '200px'
            }}
          >
            <option value="">All Categories</option>
            {categoryOptions}
          </select>
        </div>

        <div className="filter-group">
          <label>Start Date:</label>
          <input 
            type="date" 
            value={filters.start_date} 
            onChange={(e) => setFilters(f => ({ ...f, start_date: e.target.value }))}
            style={{
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              fontSize: '14px'
            }}
          />
        </div>

        <div className="filter-group">
          <label>End Date:</label>
          <input 
            type="date" 
            value={filters.end_date} 
            onChange={(e) => setFilters(f => ({ ...f, end_date: e.target.value }))}
            style={{
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              fontSize: '14px'
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default Filters; 