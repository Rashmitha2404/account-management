from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    # Upload interface
    path('upload-interface/', views.upload_interface, name='upload_interface'),
    
    # File upload - use new FileUploadView
    path('upload/', views.FileUploadView.as_view(), name='upload_file'),
    
    # Save transactions after manual review
    path('save-transactions/', views.save_transactions, name='save_transactions'),
    
    # Data retrieval
    path('transactions/', views.get_transactions, name='get_transactions'),
    path('analytics/', views.get_analytics, name='get_analytics'),
    path('analytics-view/', views.analytics_view, name='analytics_view'),
    
    # Export functionality - Fixed URL patterns
    path('export/', views.export_transactions, name='export_transactions'),
    path('export', views.export_transactions, name='export_transactions_no_slash'),  # Handle without trailing slash
    path('test-export/', views.test_export, name='test_export'),  # Test endpoint
    path('chart-data/export/', views.export_chart_data, name='export_chart_data'),
    
    # Debug test endpoint
    path('export-test/', views.export_test, name='export_test'),
    path('debug-export/', views.debug_export, name='debug_export'),
] 