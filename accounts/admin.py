from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'phone', 'city', 'created_at']
    list_filter = ['notify_email', 'notify_sms', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('user', 'phone', 'document_type', 'document_number', 'profile_image')
        }),
        ('Dirección', {
            'fields': ('address', 'city', 'zipcode')
        }),
        ('Preferencias', {
            'fields': ('bio', 'notify_email', 'notify_sms')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Nombre'
