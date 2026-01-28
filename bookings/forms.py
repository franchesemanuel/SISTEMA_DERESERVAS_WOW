from django import forms
from datetime import datetime
from django.utils import timezone
from .models import Booking, Review


class BookingForm(forms.ModelForm):
    """Formulario para crear reservas"""
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de la Reserva'
    )
    booking_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Hora de Inicio'
    )
    
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'contact_phone', 'notes']
        labels = {
            'contact_phone': 'Teléfono de Contacto',
            'notes': 'Notas Especiales',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service
    
    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        
        if booking_date and booking_time:
            # ✅ Validar que no sea en el pasado
            booking_datetime = timezone.make_aware(
                datetime.combine(booking_date, booking_time)
            )
            if booking_datetime < timezone.now():
                raise forms.ValidationError('No puedes reservar en el pasado')
            
            # ✅ Validar disponibilidad del servicio
            from services.models import Availability
            day_of_week = booking_date.weekday()
            
            # Obtener servicio desde la vista
            service = self.service
            if service:
                availability = service.availabilities.filter(
                    day_of_week=day_of_week,
                    is_available=True
                ).first()
                
                if not availability:
                    day_name = dict(Availability.DAYS_OF_WEEK)[day_of_week]
                    raise forms.ValidationError(
                        f'El servicio no está disponible los {day_name}'
                    )
                
                # Validar horario dentro de disponibilidad
                if not (availability.start_time <= booking_time <= availability.end_time):
                    raise forms.ValidationError(
                        f'Horario fuera de disponibilidad. Disponible de {availability.start_time} a {availability.end_time}'
                    )
            
            # ✅ Validar conflictos de capacidad
            if service:
                conflicting_bookings = Booking.objects.filter(
                    service=service,
                    booking_date=booking_date,
                    booking_time=booking_time,
                    status__in=['pending', 'confirmed']
                ).count()
                
                if conflicting_bookings >= service.max_capacity:
                    raise forms.ValidationError(
                        'No hay capacidad disponible para esta fecha y hora. Intenta otro horario.'
                    )
        
        return cleaned_data


class ReviewForm(forms.ModelForm):
    """Formulario para reseñas"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Calificación',
            'comment': 'Comentario',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
