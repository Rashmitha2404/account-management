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
            <th style={{
              padding: '12px 8px',
              textAlign: 'left',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Date</th>
            <th style={{
              padding: '12px 8px',
              textAlign: 'left',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Type</th>
            <th style={{
              padding: '12px 8px',
              textAlign: 'right',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Amount</th>
            <th style={{
              padding: '12px 8px',
              textAlign: 'left',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Category</th>
            <th style={{
              padding: '12px 8px',
              textAlign: 'left',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Name</th>
            <th style={{
              padding: '12px 8px',
              textAlign: 'left',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Voucher No.</th>
            <th style={{
              padding: '12px 8px',
              textAlign: 'left',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Description</th>
            <th style={{
              padding: '12px 8px',
              textAlign: 'left',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Reference</th>
            <th style={{
              padding: '12px 8px',
              textAlign: 'left',
              fontWeight: 'bold',
              fontSize: '14px',
              color: '#495057'
            }}>Category Type</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={transaction.id} style={{
              borderBottom: '1px solid #dee2e6',
              backgroundColor: index % 2 === 0 ? 'white' : '#f8f9fa'
            }}>
              <td style={{
                padding: '12px 8px',
                fontSize: '14px',
                color: '#495057'
              }}>
                {new Date(transaction.date).toLocaleDateString()}
              </td>
              <td style={{
                padding: '12px 8px',
                fontSize: '14px',
                color: transaction.type === 'Credit' ? '#28a745' : '#dc3545',
                fontWeight: 'bold'
              }}>
                {transaction.type}
              </td>
              <td style={{
                padding: '12px 8px',
                textAlign: 'right',
                fontSize: '14px',
                fontWeight: 'bold',
                color: transaction.type === 'Credit' ? '#28a745' : '#dc3545'
              }}>
                ₹{parseFloat(transaction.amount).toLocaleString('en-IN', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2
                })}
              </td>
              <td style={{
                padding: '12px 8px',
                fontSize: '14px',
                color: '#495057',
                maxWidth: '200px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap'
              }}>
                {transaction.category}
              </td>
              <td style={{
                padding: '12px 8px',
                fontSize: '14px',
                color: '#495057',
                maxWidth: '200px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap'
              }}>
                {transaction.name}
              </td>
              <td style={{
                padding: '12px 8px',
                fontSize: '14px',
                color: '#495057',
                fontFamily: 'monospace',
                fontWeight: 'bold'
              }}>
                {transaction.voucher_number}
              </td>
              <td style={{
                padding: '12px 8px',
                fontSize: '14px',
                color: '#495057',
                maxWidth: '250px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap'
              }}>
                {transaction.remarks || transaction.description || '-'}
              </td>
              <td style={{
                padding: '12px 8px',
                fontSize: '14px',
                color: '#495057',
                fontFamily: 'monospace'
              }}>
                {transaction.reference_number || transaction.cheque_number || '-'}
              </td>
              <td style={{
                padding: '12px 8px',
                fontSize: '14px',
                color: '#495057'
              }}>
                {transaction.category_type || '-'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionTable; 