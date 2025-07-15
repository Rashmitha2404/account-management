import React, { useState, useEffect } from "react";
import { getAnalytics } from "../api";
import { Pie, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
} from "chart.js";
import html2canvas from "html2canvas";
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, ChartDataLabels);

function ChartSection() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewType, setViewType] = useState('monthly'); // monthly or yearly
  const [chartType, setChartType] = useState('pie'); // pie or bar
  const [year, setYear] = useState(new Date().getFullYear());
  const [month, setMonth] = useState(new Date().getMonth() + 1);

  useEffect(() => {
    fetchAnalytics();
    // eslint-disable-next-line
  }, [year, month, viewType]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const startDate = viewType === 'monthly' 
        ? `${year}-${month.toString().padStart(2, '0')}-01`
        : `${year}-01-01`;
      const endDate = viewType === 'monthly'
        ? `${year}-${month.toString().padStart(2, '0')}-${new Date(year, month, 0).getDate()}`
        : `${year}-12-31`;

      const data = await getAnalytics({
        start_date: startDate,
        end_date: endDate,
        view_type: viewType
      });
      
      setAnalytics(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Helper to create chart data
  const getPieData = (data, label) => ({
    labels: Object.keys(data),
    datasets: [
      {
        label,
        data: Object.values(data),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#28a745', '#dc3545', '#6f42c1', '#fd7e14', '#20c997', '#e83e8c', '#343a40', '#adb5bd', '#ffc107', '#17a2b8', '#6610f2', '#f8f9fa', '#343a40'
        ],
        borderWidth: 1,
      },
    ],
  });

  const getBarData = (data, label) => ({
    labels: Object.keys(data),
    datasets: [
      {
        label,
        data: Object.values(data),
        backgroundColor: '#36A2EB',
      },
    ],
  });

  // Helper to calculate percentages
  const getPercentages = (data) => {
    const values = Object.values(data);
    const total = values.reduce((a, b) => a + b, 0);
    return values.map(v => total ? ((v / total) * 100).toFixed(1) : '0.0');
  };

  // Export functions
  function exportCreditPieAsImage() {
    const element = document.getElementById('credit-pie-section');
    html2canvas(element, { backgroundColor: null }).then(canvas => {
      const url = canvas.toDataURL('image/png');
      const a = document.createElement('a');
      a.href = url;
      a.download = 'credit_pie_chart.png';
      a.click();
    });
  }
  function exportDebitPieAsImage() {
    const element = document.getElementById('debit-pie-section');
    html2canvas(element, { backgroundColor: null }).then(canvas => {
      const url = canvas.toDataURL('image/png');
      const a = document.createElement('a');
      a.href = url;
      a.download = 'debit_pie_chart.png';
      a.click();
    });
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '20px' }}>
        Loading analytics...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '20px',
        color: '#dc3545'
      }}>
        Error loading analytics: {error}
      </div>
    );
  }

  // Pie/Bar chart rendering
  const renderChart = (data, title, type = 'pie') => {
    // Special case: For CAPX vs OPX (Debit Only), render nothing if no data
    if (title === 'CAPX vs OPX (Debit Only)' && (!data || Object.keys(data).length === 0)) {
      return <div style={{ height: 40 }}></div>; // Empty space, no message
    }
    if (!data || Object.keys(data).length === 0) {
      return (
        <div style={{ 
          textAlign: 'center', 
          padding: '20px',
          color: '#666',
          fontStyle: 'italic'
        }}>
          No data available for {title}
        </div>
      );
    }
    if (type === 'pie') {
      return (
        <div style={{ width: 400, height: 400, margin: '0 auto' }}>
          <Pie
            data={getPieData(data, title)}
            options={{
              plugins: {
                legend: { position: 'bottom' },
                datalabels: { display: false }, // Hide datalabels
                tooltip: {
                  callbacks: {
                    label: function(context) {
                      const value = context.parsed;
                      const total = context.dataset.data.reduce((a, b) => a + b, 0);
                      const percent = ((value / total) * 100).toFixed(1);
                      return `${context.label}: ${value} (${percent}%)`;
                    }
                  }
                }
              },
              maintainAspectRatio: false,
              responsive: false,
            }}
            width={400}
            height={400}
          />
        </div>
      );
    } else {
      return <Bar data={getBarData(data, title)} options={{ plugins: { legend: { display: false } }, responsive: true, scales: { y: { beginAtZero: true } } }} />;
    }
  };

  const creditColors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384'];
  const debitColors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'];
  const capxOpxColors = ['#28a745', '#dc3545']; // Green for CAPX, Red for OPX

  return (
    <div className="chart-section" style={{
      padding: '20px',
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      marginBottom: '20px'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '20px',
        flexWrap: 'wrap',
        gap: '10px'
      }}>
        <h2 style={{ margin: 0, color: '#333' }}>Analytics Dashboard</h2>
        
        <div style={{
          display: 'flex',
          gap: '10px',
          alignItems: 'center',
          flexWrap: 'wrap'
        }}>
          <select 
            value={viewType} 
            onChange={(e) => setViewType(e.target.value)}
            style={{
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              fontSize: '14px'
            }}
          >
            <option value="monthly">Monthly View</option>
            <option value="yearly">Yearly View</option>
          </select>

          <select 
            value={chartType} 
            onChange={(e) => setChartType(e.target.value)}
            style={{
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              fontSize: '14px'
            }}
          >
            <option value="pie">Pie Chart</option>
            <option value="bar">Bar Chart</option>
          </select>

          {viewType === 'monthly' ? (
            <>
              <select 
                value={year} 
                onChange={(e) => setYear(parseInt(e.target.value))}
                style={{
                  padding: '8px',
                  borderRadius: '4px',
                  border: '1px solid #ddd',
                  fontSize: '14px'
                }}
              >
                {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i).map(y => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </select>
              <select 
                value={month} 
                onChange={(e) => setMonth(parseInt(e.target.value))}
                style={{
                  padding: '8px',
                  borderRadius: '4px',
                  border: '1px solid #ddd',
                  fontSize: '14px'
                }}
              >
                {Array.from({ length: 12 }, (_, i) => i + 1).map(m => (
                  <option key={m} value={m}>
                    {new Date(2024, m - 1).toLocaleDateString('en-US', { month: 'long' })}
                  </option>
                ))}
              </select>
            </>
          ) : (
            <select 
              value={year} 
              onChange={(e) => setYear(parseInt(e.target.value))}
              style={{
                padding: '8px',
                borderRadius: '4px',
                border: '1px solid #ddd',
                fontSize: '14px'
              }}
            >
              {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i).map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          )}
        </div>
      </div>

      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'flex-start',
        gap: '40px',
        flexWrap: 'wrap',
        marginBottom: '20px'
      }}>
        {/* Credit Categories */}
        <div id="credit-pie-section" style={{
          background: "#f7f8fa",
          borderRadius: "12px",
          padding: "24px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
          maxWidth: 500,
          margin: "auto"
        }}>
          <h2 style={{ display: "flex", alignItems: "center", fontWeight: 600, fontSize: 22, marginBottom: 12 }}>
            <span style={{ fontSize: 24, marginRight: 8 }}>💰</span>
            Credit Categories
          </h2>
          {renderChart(
            analytics?.credit?.by_category || {},
            'Credit Categories',
            chartType
          )}
          {/* Custom Legend */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 16, margin: "16px 0", maxHeight: 60, overflowY: "auto" }}>
            {(Object.keys(analytics?.credit?.by_category || {})).map((label, i) => (
              <div key={label} style={{ display: "flex", alignItems: "center", gap: 4 }}>
                <span style={{
                  display: "inline-block",
                  width: 14,
                  height: 14,
                  borderRadius: "50%",
                  background: creditColors[i % creditColors.length],
                  marginRight: 6
                }} />
                <span>{label}</span>
              </div>
            ))}
          </div>
          {/* Table */}
          <table style={{ width: "100%", background: "white", borderRadius: 8, marginBottom: 16, borderCollapse: 'collapse', fontSize: 15 }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left", padding: 8 }}>Category</th>
                <th style={{ textAlign: "right", padding: 8 }}>Value (₹)</th>
                <th style={{ textAlign: "right", padding: 8 }}>Percent (%)</th>
              </tr>
            </thead>
            <tbody>
              {(Object.keys(analytics?.credit?.by_category || {})).map((label, i) => (
                <tr key={label}>
                  <td style={{ padding: 8, display: "flex", alignItems: "center" }}>
                    <span style={{
                      display: "inline-block",
                      width: 12,
                      height: 12,
                      borderRadius: "50%",
                      background: creditColors[i % creditColors.length],
                      marginRight: 6
                    }} />
                    {label}
                  </td>
                  <td style={{ textAlign: "right", padding: 8 }}>{(Object.values(analytics?.credit?.by_category || {}))[i]?.toLocaleString("en-IN")}</td>
                  <td style={{ textAlign: "right", padding: 8 }}>{getPercentages(analytics?.credit?.by_category || {})[i]}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={exportCreditPieAsImage}>Export Credit Pie Section as Image</button>
        </div>

        {/* Debit Categories */}
        <div id="debit-pie-section" style={{
          background: "#f7f8fa",
          borderRadius: "12px",
          padding: "24px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
          maxWidth: 500,
          margin: "auto"
        }}>
          <h2 style={{ display: "flex", alignItems: "center", fontWeight: 600, fontSize: 22, marginBottom: 12 }}>
            <span style={{ fontSize: 24, marginRight: 8 }}>💸</span>
            Debit Categories
          </h2>
          {renderChart(
            analytics?.debit?.by_category || {},
            'Debit Categories',
            chartType
          )}
          {/* Custom Legend */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 16, margin: "16px 0", maxHeight: 60, overflowY: "auto" }}>
            {(Object.keys(analytics?.debit?.by_category || {})).map((label, i) => (
              <div key={label} style={{ display: "flex", alignItems: "center", gap: 4 }}>
                <span style={{
                  display: "inline-block",
                  width: 14,
                  height: 14,
                  borderRadius: "50%",
                  background: debitColors[i % debitColors.length],
                  marginRight: 6
                }} />
                <span>{label}</span>
              </div>
            ))}
          </div>
          {/* Table */}
          <table style={{ width: "100%", background: "white", borderRadius: 8, marginBottom: 16, borderCollapse: 'collapse', fontSize: 15 }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left", padding: 8 }}>Category</th>
                <th style={{ textAlign: "right", padding: 8 }}>Value (₹)</th>
                <th style={{ textAlign: "right", padding: 8 }}>Percent (%)</th>
              </tr>
            </thead>
            <tbody>
              {(Object.keys(analytics?.debit?.by_category || {})).map((label, i) => (
                <tr key={label}>
                  <td style={{ padding: 8, display: "flex", alignItems: "center" }}>
                    <span style={{
                      display: "inline-block",
                      width: 12,
                      height: 12,
                      borderRadius: "50%",
                      background: debitColors[i % debitColors.length],
                      marginRight: 6
                    }} />
                    {label}
                  </td>
                  <td style={{ textAlign: "right", padding: 8 }}>{(Object.values(analytics?.debit?.by_category || {}))[i]?.toLocaleString("en-IN")}</td>
                  <td style={{ textAlign: "right", padding: 8 }}>{getPercentages(analytics?.debit?.by_category || {})[i]}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={exportDebitPieAsImage}>Export Debit Pie Section as Image</button>
        </div>
      </div> {/* Close the flex container for Credit and Debit pie charts */}

      {/* CAPX vs OPX */}
      <div style={{
        padding: '20px',
        border: '1px solid #dee2e6',
        borderRadius: '8px',
        backgroundColor: '#f8f9fa'
      }}>
        {renderChart(
          analytics?.debit?.by_category_type || {},
          'CAPX vs OPX (Debit Only)',
          chartType
        )}
      </div>

      {/* Monthly/Yearly Credit Trends */}
      <div style={{
        padding: '20px',
        border: '1px solid #dee2e6',
        borderRadius: '8px',
        backgroundColor: '#f8f9fa'
      }}>
        {renderChart(
          viewType === 'monthly' 
            ? analytics?.credit?.by_month || {}
            : analytics?.credit?.by_year || {},
          `${viewType === 'monthly' ? 'Monthly' : 'Yearly'} Credit Trends`,
          chartType
        )}
      </div>

      {/* Monthly/Yearly Debit Trends */}
      <div style={{
        padding: '20px',
        border: '1px solid #dee2e6',
        borderRadius: '8px',
        backgroundColor: '#f8f9fa'
      }}>
        {renderChart(
          viewType === 'monthly'
            ? analytics?.debit?.by_month || {}
            : analytics?.debit?.by_year || {},
          `${viewType === 'monthly' ? 'Monthly' : 'Yearly'} Debit Trends`,
          chartType
        )}
      </div>

      {/* Summary Statistics */}
      <div style={{
        marginTop: '20px',
        padding: '20px',
        backgroundColor: '#e9ecef',
        borderRadius: '8px',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <h4 style={{ margin: '0 0 10px 0', color: '#28a745' }}>Total Credit</h4>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#28a745' }}>
            ₹{analytics?.credit?.total?.toLocaleString('en-IN') || '0'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <h4 style={{ margin: '0 0 10px 0', color: '#dc3545' }}>Total Debit</h4>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#dc3545' }}>
            ₹{analytics?.debit?.total?.toLocaleString('en-IN') || '0'}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChartSection; 