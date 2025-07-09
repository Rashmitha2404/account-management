import React, { useState, useEffect } from "react";
import FileUpload from "../components/FileUpload";
import TransactionTable from "../components/TransactionTable";
import ChartSection from "../components/ChartSection";
import ExportButtons from "../components/ExportButtons";
import Filters from "../components/Filters";
import { uploadFile, getTransactions, exportTransactions, exportChartData } from "../api";

const DUMMY_CATEGORIES = [
  "Corpus", "CSR", "Grants", "Membership fees", "Loans", "Donation", "Others",
  "Programmatic", "Administrative"
];

function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const [filters, setFilters] = useState({
    type: "",
    category: "",
    start_date: "",
    end_date: ""
  });

  useEffect(() => {
    fetchTransactions();
  }, [filters]);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      // Do NOT include uploaded_at in filters for UI table
      const data = await getTransactions(filters);
      setTransactions(data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      setTransactions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file) => {
    try {
      setUploadStatus("Uploading file...");
      const result = await uploadFile(file);
      setUploadStatus(`Successfully processed ${result.created_count || result.transactions_created} transactions!`);
      // Refresh transactions after upload
      await fetchTransactions();
    } catch (error) {
      setUploadStatus(`Upload failed: ${error.message}`);
    }
  };

  const handleExportExcel = async () => {
    try {
      setUploadStatus("Exporting Excel file...");
      await exportTransactions(filters, "excel");
      setUploadStatus(""); // Clear status after download
    } catch (error) {
      setUploadStatus(`Excel export failed: ${error.message}`);
    }
  };

  const handleExportPDF = async () => {
    try {
      setUploadStatus("Exporting PDF file...");
      await exportTransactions(filters, "pdf");
      setUploadStatus(""); // Clear status after download
    } catch (error) {
      setUploadStatus(`PDF export failed: ${error.message}`);
    }
  };

  const handleExportChart = async () => {
    try {
      setUploadStatus("Exporting chart data...");
      // Get current date range for chart export
      const now = new Date();
      const currentYear = now.getFullYear();
      const filters = {
        start_date: `${currentYear}-01-01`,
        end_date: `${currentYear}-12-31`
      };
      await exportChartData(filters);
      setUploadStatus("Chart data export completed!");
    } catch (error) {
      setUploadStatus(`Chart export failed: ${error.message}`);
    }
  };

  return (
    <div className="dashboard" style={{
      maxWidth: "1400px",
      margin: "0 auto",
      padding: "20px",
      backgroundColor: "#f5f5f5",
      minHeight: "100vh"
    }}>
      <h1 style={{
        textAlign: "center",
        color: "#333",
        marginBottom: "30px",
        fontSize: "2.5rem",
        fontWeight: "bold"
      }}>
        Account Management Dashboard
      </h1>
      
      <div className="card" style={{
        backgroundColor: "white",
        borderRadius: "8px",
        padding: "20px",
        marginBottom: "20px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
      }}>
        <FileUpload onUpload={handleUpload} />
        {uploadStatus && (
          <div style={{ 
            marginTop: "10px", 
            padding: "10px", 
            borderRadius: "5px",
            backgroundColor: uploadStatus.includes("Error") || uploadStatus.includes("failed") ? "#ffebee" : "#e8f5e8",
            color: uploadStatus.includes("Error") || uploadStatus.includes("failed") ? "#c62828" : "#2e7d32"
          }}>
            {uploadStatus}
          </div>
        )}
      </div>
      
      <div className="card" style={{
        backgroundColor: "white",
        borderRadius: "8px",
        padding: "20px",
        marginBottom: "20px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
      }}>
        <Filters filters={filters} setFilters={setFilters} />
        <div className="card-table" style={{ marginTop: "20px" }}>
          {loading ? (
            <div style={{ textAlign: "center", padding: "20px" }}>
              Loading transactions...
            </div>
          ) : (
            <TransactionTable transactions={transactions} />
          )}
        </div>
      </div>
      
      <div className="charts-section">
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