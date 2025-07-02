const API_BASE_URL = 'http://localhost:8000/api';

// Upload Excel/CSV file to Django backend
export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/upload/`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
}

// Fetch transactions with optional filters
export async function fetchTransactions(filters = {}) {
  try {
    const params = new URLSearchParams();
    
    if (filters.type) params.append('type', filters.type);
    if (filters.category) params.append('category', filters.category);
    if (filters.monthYear) {
      const [year, month] = filters.monthYear.split('-');
      params.append('year', year);
      params.append('month', month);
    }

    const response = await fetch(`${API_BASE_URL}/transactions/?${params}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch transactions: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch transactions error:', error);
    throw error;
  }
}

// Fetch analytics data for charts
export async function fetchStats(filters = {}) {
  try {
    const params = new URLSearchParams();
    
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);

    const response = await fetch(`${API_BASE_URL}/analytics/?${params}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch analytics: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch analytics error:', error);
    throw error;
  }
}

// Export transactions as Excel
export async function exportExcel(filters = {}) {
  try {
    const params = new URLSearchParams();
    
    if (filters.type) params.append('type', filters.type);
    if (filters.category) params.append('category', filters.category);
    if (filters.monthYear) {
      const [year, month] = filters.monthYear.split('-');
      params.append('year', year);
      params.append('month', month);
    }

    const response = await fetch(`${API_BASE_URL}/transactions/export/?${params}&format=excel`);
    
    if (!response.ok) {
      throw new Error(`Export failed: ${response.statusText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'transactions.xlsx';
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Export error:', error);
    throw error;
  }
}

// Export transactions as PDF
export async function exportPDF(filters = {}) {
  try {
    const params = new URLSearchParams();
    
    if (filters.type) params.append('type', filters.type);
    if (filters.category) params.append('category', filters.category);
    if (filters.monthYear) {
      const [year, month] = filters.monthYear.split('-');
      params.append('year', year);
      params.append('month', month);
    }

    const response = await fetch(`${API_BASE_URL}/transactions/export/?${params}&format=pdf`);
    
    if (!response.ok) {
      throw new Error(`Export failed: ${response.statusText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'transactions.pdf';
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Export error:', error);
    throw error;
  }
} 