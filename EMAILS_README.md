# Email Notifications - Sistema de Reservas SPA

## Descripción

El sistema de notificaciones por email automáticamente envía confirmaciones, recordatorios y solicitudes de reseña a los usuarios sobre sus reservas.

## Emails Implementados

### 1. Confirmación de Reserva (booking_confirmation.html)
- **Cuándo:** Se envía inmediatamente después de crear una reserva
- **Contenido:** Detalles de la reserva (servicio, fecha, hora, precio)
- **Propósito:** Confirmar al usuario que su reserva fue registrada exitosamente

### 2. Recordatorio de Cita (booking_reminder.html)
- **Cuándo:** 24 horas antes de la reserva (mediante Celery Beat)
- **Contenido:** Detalles de la cita al día siguiente
- **Propósito:** Recordarle al usuario que tiene una cita programada

### 3. Solicitud de Reseña (review_request.html)
- **Cuándo:** Después de que la reserva ha pasado (mediante Celery Beat)
- **Contenido:** Invitación a dejar una reseña del servicio
- **Propósito:** Recopilar feedback de los clientes

### 4. Cancelación de Reserva (booking_cancelled.html)
- **Cuándo:** Cuando el usuario cancela una reserva
- **Contenido:** Confirmación de cancelación y detalles del reembolso
- **Propósito:** Confirmar la cancelación y informar sobre la política de reembolso

## Configuración

### 1. Variables de Entorno (.env)
```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # Para desarrollo
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend   # Para producción

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@spahotel.com
SERVER_EMAIL=admin@spahotel.com
```

### 2. Backends Disponibles

#### Desarrollo (Console Backend)
```python
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
```
- Los emails se imprimen en la consola
- Perfecto para testing y desarrollo
- **Actualmente configurado por defecto**

#### Producción (SMTP)
```python
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='your-email@gmail.com'
EMAIL_HOST_PASSWORD='app-password'
```

### 3. Preferencias de Usuario

Los usuarios pueden controlar si desean recibir emails:
- Editar en: `/accounts/profile/`
- Campo: "Recibir notificaciones por email"
- Los emails NO se enviarán si el usuario deshabilita esta opción

## Estructura de Archivos

```
bookings/
├── emails.py              # Funciones de envío de email
├── test_emails.py         # Script para probar emails
└── templates/
    └── emails/
        ├── booking_confirmation.html
        ├── booking_reminder.html
        ├── review_request.html
        └── booking_cancelled.html
```

## Funciones Disponibles

### send_booking_confirmation_email(booking_id)
```python
from bookings.emails import send_booking_confirmation_email

# Llamado automáticamente en create_booking view
send_booking_confirmation_email(booking.id)
```

### send_booking_reminder_email(booking_id)
```python
from bookings.emails import send_booking_reminder_email

# Será llamado automáticamente por Celery Beat 24 horas antes
send_booking_reminder_email(booking.id)
```

### send_review_request_email(booking_id)
```python
from bookings.emails import send_review_request_email

# Será llamado automáticamente por Celery Beat después de la cita
send_review_request_email(booking.id)
```

### send_booking_cancelled_email(booking_id)
```python
from bookings.emails import send_booking_cancelled_email

# Llamado automáticamente en cancel_booking view
send_booking_cancelled_email(booking.id)
```

## Pruebas Locales

### Opción 1: Usar Django Shell
```bash
python manage.py shell
```
Dentro del shell:
```python
from bookings.models import Booking
from bookings.emails import send_booking_confirmation_email

booking = Booking.objects.first()
send_booking_confirmation_email(booking.id)
```

### Opción 2: Script de Prueba
```bash
python manage.py shell < bookings/test_emails.py
```

## Plantillas de Email

Las plantillas HTML se encuentran en `templates/emails/` y usan:
- **Bootstrap 5** para estilos responsivos
- **Django template tags** para variables dinámicas
- **Colores temáticos:**
  - Azul (#007bff) para confirmación y recordatorio
  - Amarillo (#ffc107) para recordatorio
  - Verde (#28a745) para solicitud de reseña
  - Rojo (#dc3545) para cancelación

### Variables Disponibles en Templates
```django
{{ user }}              # Objeto User
{{ user.first_name }}   # Nombre del usuario
{{ booking }}           # Objeto Booking
{{ booking.id }}        # ID de la reserva
{{ booking.booking_date }}    # Fecha de la reserva
{{ booking.booking_time }}    # Hora de la reserva
{{ booking.total_price }}     # Precio total
{{ booking.service }}   # Objeto Service
{{ booking.service.name }}    # Nombre del servicio
{{ booking.service.duration_minutes }}  # Duración
{{ booking.cancellation_reason }}  # Razón de cancelación (si aplica)
```

## Próximos Pasos

1. **Celery Configuration** (Tareas Programadas)
   - Configurar Celery Beat para enviar recordatorios 24h antes
   - Configurar tareas para solicitar reseñas después de las citas
   - Ver: `/config/celery.py` (a crear)

2. **Email Real** (Producción)
   - Cambiar EMAIL_BACKEND a SMTP real
   - Usar SendGrid, AWS SES o Gmail SMTP
   - Actualizar credenciales en variables de entorno

3. **Mejoras Futuras**
   - Plantillas multilengua
   - Análisis de aperturas de email
   - Sistema de preferencias de notificaciones más granular

## Solución de Problemas

### "Los emails no se envían"
1. Verificar `user.profile.notify_email = True`
2. Verificar `EMAIL_BACKEND` está correctamente configurado
3. Si usa SMTP real, verificar credenciales

### "Error: Template not found"
1. Asegurar que existe `templates/emails/` con los 4 archivos HTML
2. Verificar que TEMPLATES.DIRS incluye `BASE_DIR / 'templates'`

### "Error de autenticación SMTP"
1. Si usa Gmail, usar "App Password" no la contraseña normal
2. Habilitar "Less secure app access" si es necesario
3. Considerar usar SendGrid o AWS SES para producción

## Referencias
- Django Email Documentation: https://docs.djangoproject.com/en/4.2/topics/email/
- Celery Beat: https://docs.celeryproject.org/en/stable/userguide/beat.html

