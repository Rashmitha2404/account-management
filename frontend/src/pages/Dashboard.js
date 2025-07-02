import React, { useState, useEffect } from "react";
import FileUpload from "../components/FileUpload";
import TransactionTable from "../components/TransactionTable";
import ChartSection from "../components/ChartSection";
import ExportButtons from "../components/ExportButtons";
import Filters from "../components/Filters";
import { uploadFile, fetchTransactions, fetchStats, exportExcel, exportPDF } from "../api";

const DUMMY_CATEGORIES = [
  "Corpus", "CSR", "Grants", "Membership fees", "Loans", "Donation", "Others",
  "Programmatic", "Administrative"
];

function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [filters, setFilters] = useState({ type: "", category: "", monthYear: "" });
  const [stats, setStats] = useState({
    creditCategories: { labels: [], datasets: [] },
    debitCategories: { labels: [], datasets: [] },
    monthly: { labels: [], datasets: [] }
  });
  const [uploadStatus, setUploadStatus] = useState("");
  const [loading, setLoading] = useState(false);

  // Load transactions and stats on component mount
  useEffect(() => {
    loadTransactions();
    loadStats();
  }, []);

  // Load transactions when filters change
  useEffect(() => {
    loadTransactions();
  }, [filters]);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const data = await fetchTransactions(filters);
      setTransactions(data);
    } catch (error) {
      console.error('Failed to load transactions:', error);
      setUploadStatus(`Error loading transactions: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const data = await fetchStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to load stats:', error);
      // Use fallback stats if API fails
      setStats({
        creditCategories: { labels: [], datasets: [] },
        debitCategories: { labels: [], datasets: [] },
        monthly: { labels: [], datasets: [] }
      });
    }
  };

  // Handle file upload to Django backend
  const handleUpload = async (file) => {
    setUploadStatus("Uploading file to server...");
    setLoading(true);
    
    try {
      const result = await uploadFile(file);
      setUploadStatus(`Success! ${result.created_count} transactions uploaded. ${result.errors.length > 0 ? `Errors: ${result.errors.join(', ')}` : ''}`);
      
      // Reload transactions and stats after successful upload
      await loadTransactions();
      await loadStats();
      
    } catch (error) {
      console.error('Upload failed:', error);
      setUploadStatus(`Upload failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleExportExcel = async () => {
    try {
      setUploadStatus("Exporting to Excel...");
      await exportExcel(filters);
      setUploadStatus("Excel export completed!");
    } catch (error) {
      setUploadStatus(`Export failed: ${error.message}`);
    }
  };

  const handleExportPDF = async () => {
    try {
      setUploadStatus("Exporting to PDF...");
      await exportPDF(filters);
      setUploadStatus("PDF export completed!");
    } catch (error) {
      setUploadStatus(`Export failed: ${error.message}`);
    }
  };

  const handleExportChart = () => {
    // TODO: Implement chart export
    setUploadStatus("Chart export feature coming soon!");
  };

  return (
    <div className="dashboard">
      <h1>Account Management Dashboard</h1>
      <div className="card">
        <FileUpload onUpload={handleUpload} />
        {uploadStatus && (
          <div style={{ 
            marginTop: '10px', 
            padding: '10px', 
            borderRadius: '5px',
            backgroundColor: uploadStatus.includes('Error') || uploadStatus.includes('failed') ? '#ffebee' : '#e8f5e8',
            color: uploadStatus.includes('Error') || uploadStatus.includes('failed') ? '#c62828' : '#2e7d32'
          }}>
            {uploadStatus}
          </div>
        )}
      </div>
      <div className="card">
        <Filters filters={filters} setFilters={setFilters} />
        <div className="card-table">
          {loading ? (
            <div style={{ textAlign: 'center', padding: '20px' }}>
              Loading transactions...
            </div>
          ) : (
            <TransactionTable transactions={transactions} />
          )}
        </div>
      </div>
      <div className="charts-section">
        <h2>Analytics</h2>
        <ChartSection />
      </div>
      <ExportButtons
        onExportExcel={handleExportExcel}
        onExportPDF={handleExportPDF}
        onExportChart={handleExportChart}
      />
    </div>
  );
}

export default Dashboard; 