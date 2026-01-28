from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    """Categorías de servicios"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji o nombre de icon")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Service(models.Model):
    """Servicios disponibles en el SPA"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=150)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(15)],
        help_text="Duración en minutos"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True)
    max_capacity = models.PositiveIntegerField(
        default=1,
        help_text="Máximo de personas simultáneamente"
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['is_active', 'category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.duration_minutes}min - ${self.price})"


class Availability(models.Model):
    """Horarios de disponibilidad por día"""
    DAYS_OF_WEEK = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Disponibilidad"
        verbose_name_plural = "Disponibilidades"
        unique_together = ('service', 'day_of_week')
        ordering = ['service', 'day_of_week', 'start_time']
    
    def __str__(self):
        day_name = dict(self.DAYS_OF_WEEK)[self.day_of_week]
        return f"{self.service.name} - {day_name} ({self.start_time}-{self.end_time})"
