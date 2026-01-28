from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg, Count
from .models import Service, Category, Availability


@require_http_methods(["GET"])
def services_list(request):
    """Listado de servicios disponibles"""
    services = Service.objects.filter(is_active=True).prefetch_related('category', 'availabilities')
    category_filter = request.GET.get('category')
    
    if category_filter:
        # ✅ Validar que la categoría existe
        from .models import Category
        if not Category.objects.filter(id=category_filter).exists():
            category_filter = None
        else:
            services = services.filter(category_id=category_filter)
    
    categories = Category.objects.all()
    
    context = {
        'services': services,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, 'services/list.html', context)


@require_http_methods(["GET"])
def service_detail(request, pk):
    """Detalle de un servicio"""
    service = get_object_or_404(Service, id=pk, is_active=True)
    
    # Obtener reseñas
    reviews = service.bookings.filter(review__isnull=False).select_related('review')
    avg_rating = reviews.aggregate(avg=Avg('review__rating'))['avg']
    review_count = reviews.count()
    
    # Obtener disponibilidades
    availabilities = service.availabilities.filter(is_available=True)
    
    context = {
        'service': service,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'availabilities': availabilities,
    }
    return render(request, 'services/detail.html', context)
