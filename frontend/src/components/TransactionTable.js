import React from "react";

function TransactionTable({ transactions }) {
  // Debug logging
  console.log("TransactionTable received transactions:", transactions);
  console.log("Number of transactions:", transactions.length);
  
  if (transactions.length > 0) {
    console.log("First transaction:", transactions[0]);
    console.log("First transaction voucher_number:", transactions[0].voucher_number);
  }

  return (
    <table className="transaction-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Type</th>
          <th>Amount</th>
          <th>Category</th>
          <th>Remarks</th>
          <th>Voucher #</th>
          <th>From</th>
          <th>To</th>
          <th>Reference #</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((tx, idx) => (
          <tr key={idx}>
            <td>{tx.date}</td>
            <td>{tx.type}</td>
            <td>{tx.amount}</td>
            <td>{tx.category}</td>
            <td>{tx.remarks}</td>
            <td style={{ backgroundColor: tx.voucher_number ? '#e8f5e8' : '#ffebee' }}>
              {tx.voucher_number || 'N/A'}
            </td>
            <td>{tx.from_party}</td>
            <td>{tx.to_party}</td>
            <td>{tx.reference_number}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TransactionTable; 