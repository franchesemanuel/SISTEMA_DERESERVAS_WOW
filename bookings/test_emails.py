"""
Script para probar el envío de emails en desarrollo
Ejecutar con: python manage.py shell < bookings/test_emails.py
"""

from django.contrib.auth.models import User
from bookings.models import Booking
from bookings.emails import (
    send_booking_confirmation_email,
    send_booking_reminder_email,
    send_review_request_email,
    send_booking_cancelled_email
)

# Obtener un usuario y una reserva de ejemplo
try:
    user = User.objects.first()
    booking = Booking.objects.first()
    
    if user and booking:
        print(f"Enviando emails de prueba para el usuario: {user.username}")
        print(f"Reserva: {booking.service.name} - {booking.booking_date}")
        
        # Probar cada email
        print("\n1. Enviando email de confirmación...")
        send_booking_confirmation_email(booking.id)
        print("✓ Email de confirmación enviado")
        
        print("\n2. Enviando email de recordatorio...")
        send_booking_reminder_email(booking.id)
        print("✓ Email de recordatorio enviado")
        
        print("\n3. Enviando email de solicitud de reseña...")
        send_review_request_email(booking.id)
        print("✓ Email de solicitud de reseña enviado")
        
        print("\n4. Enviando email de cancelación...")
        send_booking_cancelled_email(booking.id)
        print("✓ Email de cancelación enviado")
        
        print("\n✓ Todos los emails fueron enviados exitosamente")
        print("\nNota: Con EMAIL_BACKEND=console, los emails aparecerán en la consola")
    else:
        print("No hay usuarios o reservas en la base de datos")
        print("Primero crea un usuario y una reserva para probar los emails")
except Exception as e:
    print(f"Error: {e}")
