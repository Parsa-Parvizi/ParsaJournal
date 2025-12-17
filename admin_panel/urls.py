"""
Admin Panel URLs for Parsa Journal
Custom admin panel routes
"""
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('articles/<int:pk>/toggle-featured/', views.article_toggle_featured, name='article_toggle_featured'),
    path('articles/<int:pk>/change-status/', views.article_change_status, name='article_change_status'),
    path('articles/bulk-delete/', views.article_bulk_delete, name='article_bulk_delete'),
    path('statistics/', views.statistics, name='statistics'),
    path('api/chart-data/', views.chart_data, name='chart_data'),
]

