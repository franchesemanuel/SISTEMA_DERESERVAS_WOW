from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    """Extensión del modelo User de Django"""
    DOCUMENT_TYPES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PAS', 'Pasaporte'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPES, blank=True)
    document_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    # Preferencias
    notify_email = models.BooleanField(default=True, help_text="Recibir notificaciones por email")
    notify_sms = models.BooleanField(default=False, help_text="Recibir notificaciones por SMS")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"
