from django.contrib import admin
from .models import Category, Service, Availability


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_service_count']
    search_fields = ['name', 'description']
    
    def get_service_count(self, obj):
        return obj.services.count()
    get_service_count.short_description = 'Servicios'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'duration_minutes', 'price', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('category', 'name', 'description')
        }),
        ('Detalles del Servicio', {
            'fields': ('duration_minutes', 'price', 'max_capacity')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['service', 'get_day_name', 'start_time', 'end_time', 'is_available']
    list_filter = ['service', 'day_of_week', 'is_available']
    ordering = ['service', 'day_of_week', 'start_time']
    
    def get_day_name(self, obj):
        return dict(obj.DAYS_OF_WEEK)[obj.day_of_week]
    get_day_name.short_description = 'Día'
