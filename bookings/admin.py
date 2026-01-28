from django.contrib import admin
from .models import Booking, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'service_name', 'booking_date', 'booking_time', 'status', 'paid']
    list_filter = ['status', 'paid', 'booking_date', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'service__name']
    readonly_fields = ['created_at', 'updated_at', 'cancelled_at']
    date_hierarchy = 'booking_date'
    
    fieldsets = (
        ('Información de Reserva', {
            'fields': ('user', 'service', 'booking_date', 'booking_time')
        }),
        ('Datos de Contacto', {
            'fields': ('contact_phone', 'notes')
        }),
        ('Pago', {
            'fields': ('total_price', 'paid', 'payment_date')
        }),
        ('Estado', {
            'fields': ('status', 'cancellation_reason')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_name.short_description = 'Usuario'
    
    def service_name(self, obj):
        return obj.service.name
    service_name.short_description = 'Servicio'
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} reservas confirmadas')
    mark_as_confirmed.short_description = 'Marcar como confirmadas'
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} reservas completadas')
    mark_as_completed.short_description = 'Marcar como completadas'
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} reservas canceladas')
    mark_as_cancelled.short_description = 'Marcar como canceladas'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'get_rating_display', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = ['booking__user__first_name', 'booking__user__last_name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_rating_display(self, obj):
        return obj.get_rating_display()
    get_rating_display.short_description = 'Calificación'
