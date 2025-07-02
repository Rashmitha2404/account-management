import React from "react";

function ExportButtons({ onExportExcel, onExportPDF, onExportChart }) {
  return (
    <div className="export-buttons">
      <button onClick={onExportExcel}>Export Excel</button>
      <button onClick={onExportPDF}>Export PDF</button>
      <button onClick={onExportChart}>Export Chart</button>
    </div>
  );
}

export default ExportButtons; 