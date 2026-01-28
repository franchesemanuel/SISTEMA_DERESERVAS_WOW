"""
Tareas asincrónicas con Celery
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from bookings.models import Booking


def send_booking_confirmation_email(booking_id):
    """Enviar email de confirmación de reserva"""
    try:
        booking = Booking.objects.get(id=booking_id)
        user = booking.user
        
        # Solo enviar si el usuario tiene notificaciones habilitadas
        if not user.profile.notify_email:
            return
        
        context = {
            'user': user,
            'booking': booking,
            'service': booking.service,
        }
        
        html_message = render_to_string('emails/booking_confirmation.html', context)
        
        send_mail(
            subject=f'Confirmación de Reserva - {booking.service.name}',
            message=f'Tu reserva para {booking.service.name} ha sido confirmada',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error enviando email: {e}")


def send_booking_reminder_email(booking_id):
    """Enviar recordatorio 24 horas antes de la reserva"""
    try:
        booking = Booking.objects.get(id=booking_id)
        user = booking.user
        
        if not user.profile.notify_email:
            return
        
        context = {
            'user': user,
            'booking': booking,
            'service': booking.service,
        }
        
        html_message = render_to_string('emails/booking_reminder.html', context)
        
        send_mail(
            subject=f'Recordatorio: {booking.service.name} mañana',
            message=f'Recordatorio de tu reserva para {booking.service.name}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error enviando email: {e}")


def send_review_request_email(booking_id):
    """Solicitar reseña después de completar servicio"""
    try:
        booking = Booking.objects.get(id=booking_id)
        user = booking.user
        
        if not user.profile.notify_email or hasattr(booking, 'review'):
            return
        
        context = {
            'user': user,
            'booking': booking,
            'service': booking.service,
        }
        
        html_message = render_to_string('emails/review_request.html', context)
        
        send_mail(
            subject=f'¿Qué te pareció {booking.service.name}?',
            message=f'Cuéntanos tu experiencia con {booking.service.name}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error enviando email: {e}")


def send_booking_cancelled_email(booking_id):
    """Notificar cancelación de reserva"""
    try:
        booking = Booking.objects.get(id=booking_id)
        user = booking.user
        
        if not user.profile.notify_email:
            return
        
        context = {
            'user': user,
            'booking': booking,
            'service': booking.service,
        }
        
        html_message = render_to_string('emails/booking_cancelled.html', context)
        
        send_mail(
            subject=f'Reserva Cancelada - {booking.service.name}',
            message=f'Tu reserva para {booking.service.name} ha sido cancelada',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error enviando email: {e}")
