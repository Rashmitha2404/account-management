const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Upload file and get parsed transactions for manual review
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Upload failed: ${errorData.error || response.statusText}`);
  }

  const result = await response.json();
  
  // If we get parsed transactions, we need to handle the manual review workflow
  if (result.success && result.transactions) {
    // For now, we'll just return the parsed data
    // In a full implementation, you'd want to show a modal or new page for manual review
    console.log('Parsed transactions:', result.transactions);
    console.log('Total parsed:', result.total_parsed);
    console.log('Errors:', result.errors);
    
    // Return a success message for now
    return {
      created_count: result.total_parsed,
      message: `Successfully parsed ${result.total_parsed} transactions. Please use the Django upload interface for manual review.`
    };
  }

  return result;
};

// Get transactions with filters
export const getTransactions = async (filters = {}) => {
  const params = new URLSearchParams();
  
  if (filters.start_date) params.append('start_date', filters.start_date);
  if (filters.end_date) params.append('end_date', filters.end_date);
  if (filters.type) params.append('type', filters.type);
  if (filters.category) params.append('category', filters.category);

  const response = await fetch(`${API_BASE_URL}/transactions/?${params}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch transactions: ${response.statusText}`);
  }

  return response.json();
};

// Get analytics data
export const getAnalytics = async (filters = {}) => {
  const params = new URLSearchParams();
  
  if (filters.start_date) params.append('start_date', filters.start_date);
  if (filters.end_date) params.append('end_date', filters.end_date);
  if (filters.view_type) params.append('view_type', filters.view_type);

  const response = await fetch(`${API_BASE_URL}/analytics/?${params}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch analytics: ${response.statusText}`);
  }

  return response.json();
};

// Export transactions
export const exportTransactions = async (filters = null, format = "excel") => {
  let url = 'http://127.0.0.1:8000/api/export/'; // Always use /api/export/ with trailing slash
  if (filters) {
    const params = new URLSearchParams();
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);
    if (filters.type) params.append('type', filters.type);
    if (filters.category) params.append('category', filters.category);
    // Don't send format parameter - let backend default to Excel
    // if (format) params.append('format', format);
    url += `?${params.toString()}`;
  }
  const response = await fetch(url, { method: 'GET' });

  if (!response.ok) {
    throw new Error(`Export failed: ${response.statusText}`);
  }

  // Create blob and download
  const blob = await response.blob();
  const downloadUrl = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = 'transactions.xlsx';
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(downloadUrl);
  document.body.removeChild(a);
};

// Export chart data
export const exportChartData = async (filters = {}) => {
  const params = new URLSearchParams();
  
  if (filters.start_date) params.append('start_date', filters.start_date);
  if (filters.end_date) params.append('end_date', filters.end_date);

  const response = await fetch(`${API_BASE_URL}/chart-data/export/?${params}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Chart export failed: ${response.statusText}`);
  }

  const data = await response.json();
  
  // Create and download JSON file
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'chart_data.json';
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}; 