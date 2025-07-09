from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    # File upload - use new FileUploadView
    path('upload/', views.FileUploadView.as_view(), name='upload_file'),
    
    # Data retrieval
    path('transactions/', views.get_transactions, name='get_transactions'),
    path('analytics/', views.get_analytics, name='get_analytics'),
    path('analytics-view/', views.analytics_view, name='analytics_view'),
    
    # Export functionality
    path('transactions/export/', views.export_transactions, name='export_transactions'),
    path('chart-data/export/', views.export_chart_data, name='export_chart_data'),
] 