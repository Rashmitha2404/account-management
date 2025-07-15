import React from "react";

function ExportButtons({ onExportExcel, onExportFiltered, onExportPDF, onExportChart }) {
  return (
    <div className="export-buttons" style={{
      display: 'flex',
      gap: '12px',
      justifyContent: 'center',
      marginTop: '20px',
      padding: '20px',
      backgroundColor: '#f8fafc',
      borderRadius: '8px',
      border: '1px solid #e2e8f0'
    }}>
      <button 
        onClick={onExportExcel}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '12px 20px',
          backgroundColor: '#2563eb', // blue
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontWeight: '600',
          fontSize: '14px',
          transition: 'all 0.2s ease',
          boxShadow: '0 2px 4px rgba(37,99,235,0.08)'
        }}
        onMouseEnter={(e) => {
          e.target.style.backgroundColor = '#1d4ed8';
          e.target.style.transform = 'translateY(-1px)';
        }}
        onMouseLeave={(e) => {
          e.target.style.backgroundColor = '#2563eb';
          e.target.style.transform = 'translateY(0)';
        }}
      >
        📊 Export All
      </button>
      <button
        onClick={onExportFiltered}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '12px 20px',
          backgroundColor: '#10b981', // green
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontWeight: '600',
          fontSize: '14px',
          transition: 'all 0.2s ease',
          boxShadow: '0 2px 4px rgba(16, 185, 129, 0.2)'
        }}
        onMouseEnter={(e) => {
          e.target.style.backgroundColor = '#059669';
          e.target.style.transform = 'translateY(-1px)';
        }}
        onMouseLeave={(e) => {
          e.target.style.backgroundColor = '#10b981';
          e.target.style.transform = 'translateY(0)';
        }}
      >
        🟢 Export Filtered
      </button>
      <button 
        onClick={onExportPDF}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '12px 20px',
          backgroundColor: '#ef4444',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontWeight: '600',
          fontSize: '14px',
          transition: 'all 0.2s ease',
          boxShadow: '0 2px 4px rgba(239, 68, 68, 0.2)'
        }}
        onMouseEnter={(e) => {
          e.target.style.backgroundColor = '#dc2626';
          e.target.style.transform = 'translateY(-1px)';
        }}
        onMouseLeave={(e) => {
          e.target.style.backgroundColor = '#ef4444';
          e.target.style.transform = 'translateY(0)';
        }}
      >
        📄 Export PDF
      </button>
      <button 
        onClick={onExportChart}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '12px 20px',
          backgroundColor: '#8b5cf6',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontWeight: '600',
          fontSize: '14px',
          transition: 'all 0.2s ease',
          boxShadow: '0 2px 4px rgba(139, 92, 246, 0.2)'
        }}
        onMouseEnter={(e) => {
          e.target.style.backgroundColor = '#7c3aed';
          e.target.style.transform = 'translateY(-1px)';
        }}
        onMouseLeave={(e) => {
          e.target.style.backgroundColor = '#8b5cf6';
          e.target.style.transform = 'translateY(0)';
        }}
      >
        📈 Export Charts
      </button>
    </div>
  );
}

export default ExportButtons; 