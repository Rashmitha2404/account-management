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

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

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
      return <Pie data={getPieData(data, title)} options={{ plugins: { legend: { position: 'bottom' } } }} />;
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
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '20px'
      }}>
        {/* Credit Categories */}
        <div style={{
          padding: '20px',
          border: '1px solid #dee2e6',
          borderRadius: '8px',
          backgroundColor: '#f8f9fa'
        }}>
          {renderChart(
            analytics?.credit?.by_category || {},
            'Credit Categories',
            chartType
          )}
        </div>

        {/* Debit Categories */}
        <div style={{
          padding: '20px',
          border: '1px solid #dee2e6',
          borderRadius: '8px',
          backgroundColor: '#f8f9fa'
        }}>
          {renderChart(
            analytics?.debit?.by_category || {},
            'Debit Categories',
            chartType
          )}
        </div>

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
        <div style={{ textAlign: 'center' }}>
          <h4 style={{ margin: '0 0 10px 0', color: '#28a745' }}>CAPX</h4>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#28a745' }}>
            ₹{analytics?.debit?.by_category_type?.CAPX?.toLocaleString('en-IN') || '0'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <h4 style={{ margin: '0 0 10px 0', color: '#dc3545' }}>OPX</h4>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#dc3545' }}>
            ₹{analytics?.debit?.by_category_type?.OPX?.toLocaleString('en-IN') || '0'}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChartSection; 