import React, { useState, useEffect, useMemo } from "react";
import { Bar, Pie } from "react-chartjs-2";
import { fetchStats } from "../api";

function groupByYear(stats) {
  // Group monthly data by year for year-wise chart
  if (!stats.monthly || !stats.monthly.labels || !stats.monthly.datasets) return { labels: [], datasets: [] };
  const yearMap = {};
  stats.monthly.labels.forEach((label, idx) => {
    const year = label.split("-")[0];
    if (!yearMap[year]) yearMap[year] = { Credits: 0, Debits: 0 };
    stats.monthly.datasets.forEach(ds => {
      if (ds.label === "Credits") yearMap[year].Credits += ds.data[idx] || 0;
      if (ds.label === "Debits") yearMap[year].Debits += ds.data[idx] || 0;
    });
  });
  return {
    labels: Object.keys(yearMap),
    datasets: [
      {
        label: "Credits",
        data: Object.values(yearMap).map(y => y.Credits),
        backgroundColor: "#36A2EB"
      },
      {
        label: "Debits",
        data: Object.values(yearMap).map(y => y.Debits),
        backgroundColor: "#FF6384"
      }
    ]
  };
}

const MONTHS = [
  { value: "full", label: "Full Year" },
  { value: "01", label: "January" },
  { value: "02", label: "February" },
  { value: "03", label: "March" },
  { value: "04", label: "April" },
  { value: "05", label: "May" },
  { value: "06", label: "June" },
  { value: "07", label: "July" },
  { value: "08", label: "August" },
  { value: "09", label: "September" },
  { value: "10", label: "October" },
  { value: "11", label: "November" },
  { value: "12", label: "December" },
];

function getMonthRange(year, month) {
  if (month === "full") {
    return {
      start_date: `${year}-01-01`,
      end_date: `${year}-12-31`,
    };
  }
  const start_date = `${year}-${month}-01`;
  // Get last day of month
  const end = new Date(year, parseInt(month), 0).getDate();
  const end_date = `${year}-${month}-${end}`;
  return { start_date, end_date };
}

function ChartSection() {
  const now = new Date();
  const currentYear = now.getFullYear();
  const [selectedMonth, setSelectedMonth] = useState("full");
  const [selectedYear, setSelectedYear] = useState(currentYear);
  const [stats, setStats] = useState({
    creditCategories: { labels: [], datasets: [] },
    debitCategories: { labels: [], datasets: [] },
    monthly: { labels: [], datasets: [] }
  });
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState("month");
  const yearData = useMemo(() => groupByYear(stats), [stats]);

  useEffect(() => {
    async function loadStats() {
      setLoading(true);
      try {
        let filters = {};
        if (selectedMonth !== "full") {
          filters = getMonthRange(selectedYear, selectedMonth);
        } else {
          filters = getMonthRange(selectedYear, "full");
        }
        const data = await fetchStats(filters);
        setStats(data);
      } catch (error) {
        setStats({
          creditCategories: { labels: [], datasets: [] },
          debitCategories: { labels: [], datasets: [] },
          monthly: { labels: [], datasets: [] }
        });
      } finally {
        setLoading(false);
      }
    }
    loadStats();
  }, [selectedMonth, selectedYear]);

  // Generate year options (last 5 years)
  const yearOptions = [];
  for (let y = currentYear; y >= currentYear - 4; y--) {
    yearOptions.push(y);
  }

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "center", gap: 16, marginBottom: 24 }}>
        <select value={selectedYear} onChange={e => setSelectedYear(Number(e.target.value))} style={{ padding: '0.5rem', borderRadius: 6 }}>
          {yearOptions.map(y => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>
        <select value={selectedMonth} onChange={e => setSelectedMonth(e.target.value)} style={{ padding: '0.5rem', borderRadius: 6 }}>
          {MONTHS.map(m => (
            <option key={m.value} value={m.value}>{m.label}</option>
          ))}
        </select>
        <button
          style={{
            background: view === "month" ? "#2563eb" : "#f1f5f9",
            color: view === "month" ? "#fff" : "#222",
            border: "none",
            borderRadius: 8,
            padding: "0.5rem 1.2rem",
            fontWeight: 600,
            cursor: "pointer",
            boxShadow: view === "month" ? "0 2px 6px rgba(37,99,235,0.08)" : "none",
            transition: "background 0.2s"
          }}
          onClick={() => setView("month")}
        >
          Month-wise
        </button>
        <button
          style={{
            background: view === "year" ? "#2563eb" : "#f1f5f9",
            color: view === "year" ? "#fff" : "#222",
            border: "none",
            borderRadius: 8,
            padding: "0.5rem 1.2rem",
            fontWeight: 600,
            cursor: "pointer",
            boxShadow: view === "year" ? "0 2px 6px rgba(37,99,235,0.08)" : "none",
            transition: "background 0.2s"
          }}
          onClick={() => setView("year")}
        >
          Year-wise
        </button>
      </div>
      {loading ? (
        <div style={{ textAlign: 'center', padding: '20px' }}>Loading analytics...</div>
      ) : (
      <div className="charts">
        <div>
          <h3 style={{marginBottom: 8}}>Credit Categories</h3>
          <Pie data={stats.creditCategories} />
        </div>
        <div>
          <h3 style={{marginBottom: 8}}>Debit Categories</h3>
          <Pie data={stats.debitCategories} />
        </div>
        <div style={{width: '100%'}}>
          <h3 style={{marginBottom: 8}}>{view === "month" ? "Month-wise Trends" : "Year-wise Trends"}</h3>
          <Bar data={view === "month" ? stats.monthly : yearData} />
        </div>
      </div>
      )}
    </div>
  );
}

export default ChartSection; 