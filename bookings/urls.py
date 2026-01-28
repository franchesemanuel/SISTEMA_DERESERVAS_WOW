from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.bookings_list, name='list'),
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('<int:service_id>/create/', views.create_booking, name='create'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel'),
    path('<int:booking_id>/review/', views.create_review, name='review'),
]
