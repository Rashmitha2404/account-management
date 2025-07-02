from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('analytics/', views.analytics_view, name='analytics'),
] 