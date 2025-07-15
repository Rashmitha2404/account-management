import React from "react";

function TransactionTable({ transactions }) {
  if (!transactions || transactions.length === 0) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '20px',
        color: '#666',
        fontStyle: 'italic'
      }}>
        No transactions found for the selected filters.
      </div>
    );
  }

  const headerStyle = {
    padding: '12px 8px',
    textAlign: 'left',
    fontWeight: 'bold',
    fontSize: '14px',
    color: '#495057'
  };
  const cellStyle = {
    padding: '12px 8px',
    fontSize: '14px',
    color: '#495057',
    maxWidth: '200px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap'
  };

  return (
    <div className="transaction-table">
      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        backgroundColor: 'white',
        borderRadius: '8px',
        overflow: 'hidden',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <thead>
          <tr style={{
            backgroundColor: '#f8f9fa',
            borderBottom: '2px solid #dee2e6'
          }}>
            <th style={headerStyle}>Date</th>
            <th style={headerStyle}>Type</th>
            <th style={headerStyle}>Amount</th>
            <th style={headerStyle}>Category</th>
            <th style={headerStyle}>Purpose</th>
            <th style={headerStyle}>Payee/Recipient</th>
            <th style={headerStyle}>Voucher No.</th>
            <th style={headerStyle}>Description</th>
            <th style={headerStyle}>Cheque/Ref No.</th>
            <th style={headerStyle}>Branch Code</th>
            <th style={headerStyle}>Balance</th>
            <th style={headerStyle}>Category Type</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={transaction.id || index} style={{
              borderBottom: '1px solid #dee2e6',
              backgroundColor: index % 2 === 0 ? 'white' : '#f8f9fa'
            }}>
              <td style={cellStyle}>{new Date(transaction.date).toLocaleDateString()}</td>
              <td style={{...cellStyle, color: transaction.type === 'Credit' ? '#28a745' : '#dc3545', fontWeight: 'bold'}}>{transaction.type}</td>
              <td style={{...cellStyle, textAlign: 'right', fontWeight: 'bold', color: transaction.type === 'Credit' ? '#28a745' : '#dc3545'}}>
                ₹{parseFloat(transaction.amount).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </td>
              <td style={cellStyle}>{transaction.category}</td>
              <td style={cellStyle}>{transaction.purpose || '-'}</td>
              <td style={cellStyle}>{transaction.payee_recipient_name || transaction.name || '-'}</td>
              <td style={{...cellStyle, fontFamily: 'monospace', fontWeight: 'bold'}}>{transaction.voucher_number}</td>
              <td style={cellStyle}>{transaction.remarks || transaction.description || '-'}</td>
              <td style={cellStyle}>{transaction.cheque_number || transaction.reference_number || '-'}</td>
              <td style={cellStyle}>{transaction.branch_code || '-'}</td>
              <td style={cellStyle}>{transaction.balance !== undefined && transaction.balance !== null ? `₹${parseFloat(transaction.balance).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : '-'}</td>
              <td style={cellStyle}>{transaction.category_type || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionTable; 