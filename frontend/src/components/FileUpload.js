import React, { useState } from "react";

function FileUpload({ onUpload }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Validate file type
      const validTypes = ['.xlsx', '.xls', '.csv'];
      const fileExtension = selectedFile.name.toLowerCase().substring(selectedFile.name.lastIndexOf('.'));
      
      if (validTypes.includes(fileExtension)) {
        setFile(selectedFile);
      } else {
        alert('Please select a valid Excel or CSV file (.xlsx, .xls, .csv)');
        e.target.value = null;
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    try {
      setUploading(true);
      await onUpload(file);
      setFile(null);
      // Reset file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = '';
    } catch (error) {
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      const validTypes = ['.xlsx', '.xls', '.csv'];
      const fileExtension = droppedFile.name.toLowerCase().substring(droppedFile.name.lastIndexOf('.'));
      
      if (validTypes.includes(fileExtension)) {
        setFile(droppedFile);
      } else {
        alert('Please select a valid Excel or CSV file (.xlsx, .xls, .csv)');
      }
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const redirectToDjangoUpload = () => {
    window.open('http://localhost:8000/api/upload-interface/', '_blank');
  };

  return (
    <div className="file-upload" style={{
      border: '2px dashed #ccc',
      borderRadius: '8px',
      padding: '20px',
      textAlign: 'center',
      backgroundColor: '#f9f9f9',
      transition: 'all 0.3s ease'
    }}
    onDrop={handleDrop}
    onDragOver={handleDragOver}>
      
      <div style={{ marginBottom: '15px' }}>
        <i className="fas fa-cloud-upload-alt" style={{ fontSize: '2rem', color: '#666' }}></i>
      </div>
      
      <h3 style={{ marginBottom: '10px', color: '#333' }}>
        Bank Transaction Upload
      </h3>
      
      <p style={{ color: '#666', marginBottom: '20px' }}>
        For the complete upload experience with manual review, please use the Django upload interface.
      </p>
      
      <button 
        onClick={redirectToDjangoUpload}
        style={{
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          padding: '12px 24px',
          borderRadius: '5px',
          cursor: 'pointer',
          fontSize: '16px',
          marginBottom: '15px'
        }}
      >
        Open Full Upload Interface
      </button>
      
      <div style={{ 
        borderTop: '1px solid #ddd', 
        paddingTop: '15px', 
        marginTop: '15px',
        fontSize: '12px', 
        color: '#666' 
      }}>
        <p><strong>Features available in Django interface:</strong></p>
        <ul style={{ textAlign: 'left', margin: '10px 0' }}>
          <li>✅ Manual input of Purpose and Payee/Recipient</li>
          <li>✅ Category selection and adjustment</li>
          <li>✅ Transaction review before saving</li>
          <li>✅ Automatic voucher number generation</li>
          <li>✅ Duplicate detection</li>
        </ul>
        <p><strong>Supported formats:</strong> .xlsx, .xls, .csv</p>
        <p><strong>Required columns:</strong> Txn Date, Value Date, Description, Ref No./Cheque No., Branch Code, Debit, Credit, Balance</p>
      </div>
    </div>
  );
}

export default FileUpload; 