import React from "react";
import { Bar, Pie } from "react-chartjs-2";

function isValidChartData(data) {
  return data && Array.isArray(data.labels) && Array.isArray(data.datasets);
}

function ChartSection({ stats }) {
  return (
    <div className="charts">
      <div>
        <h3>Credit Categories</h3>
        {isValidChartData(stats.creditCategories) ? (
          <Pie data={stats.creditCategories} />
        ) : (
          <div>No data</div>
        )}
      </div>
      <div>
        <h3>Debit Categories</h3>
        {isValidChartData(stats.debitCategories) ? (
          <Pie data={stats.debitCategories} />
        ) : (
          <div>No data</div>
        )}
      </div>
      <div style={{width: '100%'}}>
        <h3>Monthly Trends</h3>
        {isValidChartData(stats.monthly) ? (
          <Bar data={stats.monthly} />
        ) : (
          <div>No data</div>
        )}
      </div>
    </div>
  );
}

export default ChartSection; 