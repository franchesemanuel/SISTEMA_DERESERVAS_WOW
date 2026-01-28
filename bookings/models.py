from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from services.models import Service

# Validador de teléfono
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Teléfono inválido. Formato esperado: +XX-XXXXXXXXX o 123456789'
)


class Booking(models.Model):
    """Reservas de servicios"""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('no_show', 'No presentado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField(help_text="Fecha de la reserva")
    booking_time = models.TimeField(help_text="Hora de inicio")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Datos de contacto al momento de reservar
    contact_phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        help_text="Teléfono de contacto (ej: +1-2025551234 o 2025551234)"
    )
    notes = models.TextField(blank=True, help_text="Notas especiales del cliente")
    
    # Información de pago
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-booking_date', '-booking_time']
        indexes = [
            models.Index(fields=['user', 'booking_date']),
            models.Index(fields=['status', 'booking_date']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.service.name} ({self.booking_date} {self.booking_time})"
    
    @property
    def is_past(self):
        """Verificar si la reserva ya pasó"""
        from datetime import datetime
        booking_datetime = timezone.make_aware(
            datetime.combine(self.booking_date, self.booking_time)
        )
        return booking_datetime < timezone.now()
    
    @property
    def end_time(self):
        """Calcular hora de finalización basada en duración del servicio"""
        from datetime import datetime, timedelta
        start = datetime.combine(self.booking_date, self.booking_time)
        end = start + timedelta(minutes=self.service.duration_minutes)
        return end.time()
    
    def can_be_cancelled(self):
        """Determinar si la reserva puede ser cancelada"""
        return self.status in ['pending', 'confirmed'] and not self.is_past
    
    def cancel(self, reason=''):
        """Cancelar la reserva"""
        if self.can_be_cancelled():
            self.status = 'cancelled'
            self.cancelled_at = timezone.now()
            self.cancellation_reason = reason
            self.save()
            return True
        return False


class Review(models.Model):
    """Reseñas y calificaciones de servicios"""
    RATING_CHOICES = [
        (1, '⭐ Muy malo'),
        (2, '⭐⭐ Malo'),
        (3, '⭐⭐⭐ Regular'),
        (4, '⭐⭐⭐⭐ Bueno'),
        (5, '⭐⭐⭐⭐⭐ Excelente'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de 1 a 5 estrellas"
    )
    comment = models.TextField(blank=True)
    is_verified = models.BooleanField(default=True, help_text="Compra verificada")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['booking', '-created_at']),
        ]
    
    def __str__(self):
        return f"⭐ {self.get_rating_display()} - {self.booking.service.name}"
