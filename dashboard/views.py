from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from bookings.models import Booking, Review
from services.models import Service, Category
from accounts.models import UserProfile


def is_staff(user):
    """Verificar si el usuario es staff"""
    return user.is_staff


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_staff)
def dashboard_index(request):
    """Dashboard principal del administrador"""
    now = timezone.now()
    today = now.date()
    
    # Estadísticas generales
    total_bookings = Booking.objects.count()
    total_users = UserProfile.objects.count()
    total_services = Service.objects.filter(is_active=True).count()
    
    # Ingresos
    total_revenue = Booking.objects.filter(paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
    today_revenue = Booking.objects.filter(paid=True, payment_date__date=today).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Reservas por estado
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    
    # Próximas reservas (próximos 7 días)
    upcoming_bookings = Booking.objects.filter(
        booking_date__gte=today,
        booking_date__lte=today + timedelta(days=7),
        status__in=['pending', 'confirmed']
    ).select_related('user', 'service').order_by('booking_date', 'booking_time')[:10]
    
    # Calificación promedio
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']
    
    # Reservas hoy
    today_bookings = Booking.objects.filter(booking_date=today).count()
    
    # Calcular porcentajes para las barras de progreso
    pending_percentage = (pending_bookings * 100 / total_bookings) if total_bookings > 0 else 0
    confirmed_percentage = (confirmed_bookings * 100 / total_bookings) if total_bookings > 0 else 0
    completed_percentage = (completed_bookings * 100 / total_bookings) if total_bookings > 0 else 0
    
    context = {
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_services': total_services,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'upcoming_bookings': upcoming_bookings,
        'avg_rating': avg_rating,
        'today_bookings': today_bookings,
        'pending_percentage': pending_percentage,
        'confirmed_percentage': confirmed_percentage,
        'completed_percentage': completed_percentage,
    }
    return render(request, 'dashboard/index.html', context)


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_staff)
def bookings_management(request):
    """Gestión de reservas"""
    bookings = Booking.objects.select_related('user', 'service').order_by('-booking_date')
    
    # Filtros
    status_filter = request.GET.get('status')
    service_filter = request.GET.get('service')
    date_filter = request.GET.get('date')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if service_filter:
        bookings = bookings.filter(service_id=service_filter)
    
    if date_filter:
        bookings = bookings.filter(booking_date=date_filter)
    
    services = Service.objects.filter(is_active=True)
    
    context = {
        'bookings': bookings,
        'services': services,
        'status_filter': status_filter,
        'service_filter': service_filter,
        'date_filter': date_filter,
    }
    return render(request, 'dashboard/bookings_management.html', context)


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_staff)
def revenue_report(request):
    """Reporte de ingresos"""
    # Últimos 30 días
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    
    daily_revenue = Booking.objects.filter(
        paid=True,
        payment_date__date__gte=thirty_days_ago
    ).extra(
        select={'date': 'DATE(payment_date)'}
    ).values('date').annotate(
        total=Sum('total_price'),
        count=Count('id')
    ).order_by('date')
    
    # Calcular promedio para daily_revenue
    daily_revenue_with_avg = []
    for item in daily_revenue:
        item_dict = dict(item)
        item_dict['average'] = item['total'] / item['count'] if item['count'] > 0 else 0
        daily_revenue_with_avg.append(item_dict)
    
    # Ingresos por servicio
    revenue_by_service = Booking.objects.filter(
        paid=True
    ).values('service__name').annotate(
        total=Sum('total_price'),
        count=Count('id')
    ).order_by('-total')[:10]
    
    # Ingresos por categoría
    revenue_by_category = Booking.objects.filter(
        paid=True
    ).values('service__category__name').annotate(
        total=Sum('total_price'),
        count=Count('id')
    ).order_by('-total')
    
    # Totales
    total_all_time = Booking.objects.filter(paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_thirty_days = Booking.objects.filter(
        paid=True,
        payment_date__date__gte=thirty_days_ago
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    context = {
        'daily_revenue': daily_revenue_with_avg,
        'revenue_by_service': list(revenue_by_service),
        'revenue_by_category': list(revenue_by_category),
        'total_all_time': total_all_time,
        'total_thirty_days': total_thirty_days,
    }
    return render(request, 'dashboard/revenue_report.html', context)


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_staff)
def services_stats(request):
    """Estadísticas de servicios"""
    services = Service.objects.annotate(
        total_bookings=Count('bookings'),
        avg_rating=Avg('bookings__review__rating'),
        total_revenue=Sum('bookings__total_price')
    ).order_by('-total_bookings')
    
    # Servicios por categoría
    categories = Category.objects.annotate(
        total_services=Count('services'),
        total_bookings=Count('services__bookings')
    ).order_by('-total_bookings')
    
    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'dashboard/services_stats.html', context)


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_staff)
def users_stats(request):
    """Estadísticas de usuarios"""
    total_users = UserProfile.objects.count()
    users_with_bookings = UserProfile.objects.filter(user__bookings__isnull=False).distinct().count()
    
    # Top usuarios
    top_users_qs = UserProfile.objects.annotate(
        total_bookings=Count('user__bookings'),
        total_spent=Sum('user__bookings__total_price')
    ).filter(total_bookings__gt=0).order_by('-total_spent')[:10]
    
    # Calcular promedio por reserva para cada usuario
    top_users = []
    for user in top_users_qs:
        user_dict = {
            'user': user.user,
            'total_bookings': user.total_bookings,
            'total_spent': user.total_spent or 0,
            'average_per_booking': (user.total_spent / user.total_bookings) if user.total_bookings > 0 and user.total_spent else 0
        }
        top_users.append(user_dict)
    
    # Usuarios nuevos últimos 30 días
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users = UserProfile.objects.filter(
        created_at__gte=thirty_days_ago
    ).count()
    
    # Calcular porcentaje de usuarios con reservas
    users_with_bookings_percentage = (users_with_bookings * 100 / total_users) if total_users > 0 else 0
    
    context = {
        'total_users': total_users,
        'users_with_bookings': users_with_bookings,
        'users_with_bookings_percentage': users_with_bookings_percentage,
        'top_users': top_users,
        'new_users': new_users,
    }
    return render(request, 'dashboard/users_stats.html', context)
