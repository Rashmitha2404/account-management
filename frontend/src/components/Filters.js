import React from "react";

const CREDIT_CATEGORIES = [
  "Corpus",
  "CSR",
  "Grants",
  "Membership fees",
  "Loans",
  "Donation",
  "Others"
];

const DEBIT_CATEGORIES = {
  Programmatic: [
    "Education",
    "Empowerment",
    "Environment",
    "Innovation"
  ],
  Administrative: [
    "Salaries to Employees",
    "Stipends to apprentice",
    "Honorarium to tutors",
    "Rent",
    "Travel",
    "Maintenance",
    "Other operational expenses",
    "Educational aid",
    "Digital gadgets",
    "Consumables",
    "Training expenses",
    "Bank charges",
    "Audit expenses",
    "Outsourcing"
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
      <select value={filters.type} onChange={handleTypeChange}>
        <option value="">All Types</option>
        <option value="Credit">Credit</option>
        <option value="Debit">Debit</option>
      </select>
      <select
        value={filters.category}
        onChange={e => setFilters(f => ({ ...f, category: e.target.value }))}
        disabled={!filters.type}
      >
        <option value="">All Categories</option>
        {categoryOptions}
      </select>
      <input type="month" value={filters.monthYear} onChange={e => setFilters(f => ({...f, monthYear: e.target.value}))} />
    </div>
  );
}

export default Filters; 