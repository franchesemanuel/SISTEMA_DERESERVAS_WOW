from django.urls import path
from . import views
from . import exports

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('bookings/', views.bookings_management, name='bookings'),
    path('revenue/', views.revenue_report, name='revenue'),
    path('services/', views.services_stats, name='services'),
    path('users/', views.users_stats, name='users'),
    
    # Exports
    path('export/revenue/pdf/', exports.export_revenue_pdf, name='export_revenue_pdf'),
    path('export/revenue/excel/', exports.export_revenue_excel, name='export_revenue_excel'),
    path('export/bookings/pdf/', exports.export_bookings_pdf, name='export_bookings_pdf'),
    path('export/bookings/excel/', exports.export_bookings_excel, name='export_bookings_excel'),
]
