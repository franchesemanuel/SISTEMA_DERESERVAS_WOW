from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from services.models import Service


@require_http_methods(["GET"])
def home(request):
    """Página de inicio del sistema"""
    # Obtener servicios destacados (máx 3 para la home)
    featured_services = Service.objects.filter(is_active=True).order_by('-id')[:3]
    
    context = {
        'title': 'Inicio',
        'featured_services': featured_services,
    }
    return render(request, 'home.html', context)


@require_http_methods(["GET"])
@login_required
def dashboard_view(request):
    """Dashboard principal"""
    context = {
        'title': 'Dashboard',
    }
    return render(request, 'dashboard/index.html', context)
