import React from "react";

function ExportButtons({ onExportExcel, onExportPDF }) {
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
          backgroundColor: '#10b981',
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
        📊 Export Excel
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
    </div>
  );
}

export default ExportButtons; 