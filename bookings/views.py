from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django import forms
from datetime import datetime, timedelta
from .models import Booking, Review
from .emails import send_booking_confirmation_email, send_booking_cancelled_email
from services.models import Service


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
    
    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        
        if booking_date and booking_time:
            booking_datetime = timezone.make_aware(
                datetime.combine(booking_date, booking_time)
            )
            if booking_datetime < timezone.now():
                raise forms.ValidationError('No puedes reservar en el pasado')
        
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


@require_http_methods(["GET", "POST"])
@login_required
def create_booking(request, service_id):
    """Crear una nueva reserva"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, service=service)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.total_price = service.price
            booking.save()
            
            # Enviar email de confirmación
            send_booking_confirmation_email(booking.id)
            
            messages.success(request, f'¡Reserva creada exitosamente! Te hemos enviado un email de confirmación.')
            return redirect('bookings:list')
    else:
        # Prellenar con teléfono del perfil si existe
        initial = {}
        if request.user.profile.phone:
            initial['contact_phone'] = request.user.profile.phone
        form = BookingForm(initial=initial, service=service)
    
    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'bookings/create.html', context)


@require_http_methods(["GET"])
@login_required
def bookings_list(request):
    """Listado de mis reservas"""
    bookings = request.user.bookings.all().select_related('service').order_by('-booking_date')
    
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
    }
    return render(request, 'bookings/list.html', context)


@require_http_methods(["GET"])
@login_required
def booking_detail(request, pk):
    """Detalle de una reserva"""
    booking = get_object_or_404(Booking, id=pk, user=request.user)
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/detail.html', context)


@require_http_methods(["POST"])
@login_required
def cancel_booking(request, pk):
    """Cancelar una reserva"""
    booking = get_object_or_404(Booking, id=pk, user=request.user)
    
    if booking.cancel(reason=request.POST.get('reason', '')):
        # Enviar email de cancelación
        send_booking_cancelled_email(booking.id)
        messages.success(request, 'Reserva cancelada exitosamente. Te hemos enviado una confirmación por email.')
    else:
        messages.error(request, 'No se puede cancelar esta reserva')
    
    return redirect('bookings:detail', pk=booking.id)


@require_http_methods(["GET", "POST"])
@login_required
def create_review(request, booking_id):
    """Crear una reseña"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Verificar que la reserva esté completada
    if booking.status != 'completed':
        messages.error(request, 'Solo puedes reseñar reservas completadas')
        return redirect('bookings:detail', pk=booking.id)
    
    # Verificar que no tenga reseña
    if hasattr(booking, 'review'):
        messages.info(request, 'Ya has reseñado esta reserva')
        return redirect('bookings:detail', pk=booking.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            
            messages.success(request, '¡Gracias por tu reseña!')
            return redirect('bookings:detail', pk=booking.id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'bookings/review.html', context)
