"""
Tests para vistas del sistema de reservas
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, time

from accounts.models import UserProfile
from services.models import Category, Service
from bookings.models import Booking, Review


class BookingViewsTest(TestCase):
    """Tests para las vistas de reservas"""
    
    def setUp(self):
        """Crear datos de prueba"""
        self.client = Client()
        
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear categoría y servicio
        self.category = Category.objects.create(name='Masajes', icon='🧖')
        self.service = Service.objects.create(
            name='Masaje Relajante',
            description='Masaje de 60 minutos',
            category=self.category,
            duration_minutes=60,
            price=50.00,
            max_capacity=1
        )
        
        # Crear reserva de prueba
        self.tomorrow = (timezone.now() + timedelta(days=1)).date()
        self.booking = Booking.objects.create(
            user=self.user,
            service=self.service,
            booking_date=self.tomorrow,
            booking_time=time(10, 0),
            total_price=50.00
        )
    
    def test_bookings_list_requires_login(self):
        """Verificar que la lista de reservas requiere autenticación"""
        response = self.client.get(reverse('bookings:list'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/accounts/login/', response.url)
    
    def test_bookings_list_authenticated(self):
        """Verificar que usuario autenticado puede ver sus reservas"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookings:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.service.name, response.content.decode())
    
    def test_booking_detail_requires_login(self):
        """Verificar que el detalle de reserva requiere autenticación"""
        response = self.client.get(reverse('bookings:detail', args=[self.booking.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_booking_detail_authenticated(self):
        """Verificar que usuario puede ver su reserva"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookings:detail', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.service.name, response.content.decode())
    
    def test_create_booking_requires_login(self):
        """Verificar que crear reserva requiere autenticación"""
        response = self.client.get(reverse('bookings:create', args=[self.service.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_create_booking_page_loads(self):
        """Verificar que la página de crear reserva carga"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookings:create', args=[self.service.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_create_booking_valid(self):
        """Verificar que se puede crear una reserva válida"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'booking_date': self.tomorrow,
            'booking_time': time(14, 0),
            'contact_phone': '1234567890',
            'notes': 'Sin alergias conocidas'
        }
        response = self.client.post(
            reverse('bookings:create', args=[self.service.id]),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # Verificar que se creó la reserva
        self.assertEqual(Booking.objects.count(), 2)
    
    def test_create_booking_past_date(self):
        """Verificar que no se puede crear reserva en el pasado"""
        self.client.login(username='testuser', password='testpass123')
        past_date = (timezone.now() - timedelta(days=1)).date()
        data = {
            'booking_date': past_date,
            'booking_time': time(10, 0),
            'contact_phone': '1234567890'
        }
        response = self.client.post(
            reverse('bookings:create', args=[self.service.id]),
            data
        )
        # Debería mostrar error de formulario
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'No puedes reservar en el pasado')
    
    def test_cancel_booking(self):
        """Verificar que se puede cancelar una reserva"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('bookings:cancel', args=[self.booking.id]),
            {'reason': 'Cambio de planes'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')
    
    def test_create_review(self):
        """Verificar que se puede crear una reseña"""
        # Hacer que la reserva sea pasada
        self.booking.booking_date = timezone.now().date() - timedelta(days=1)
        self.booking.status = 'completed'
        self.booking.save()
        
        self.client.login(username='testuser', password='testpass123')
        data = {
            'rating': 5,
            'comment': 'Excelente servicio'
        }
        response = self.client.post(
            reverse('bookings:review', args=[self.booking.id]),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # Verificar que se creó la reseña
        self.assertTrue(Review.objects.filter(booking=self.booking).exists())


class ServiceViewsTest(TestCase):
    """Tests para las vistas de servicios"""
    
    def setUp(self):
        """Crear datos de prueba"""
        self.client = Client()
        
        # Crear categoría y servicios
        self.category = Category.objects.create(name='Masajes', icon='🧖')
        self.service1 = Service.objects.create(
            name='Masaje Relajante',
            category=self.category,
            duration_minutes=60,
            price=50.00
        )
        self.service2 = Service.objects.create(
            name='Masaje Deportivo',
            category=self.category,
            duration_minutes=45,
            price=40.00
        )
    
    def test_services_list_no_login(self):
        """Verificar que la lista de servicios es pública"""
        response = self.client.get(reverse('services:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_services_list_contains_all(self):
        """Verificar que la lista muestra todos los servicios"""
        response = self.client.get(reverse('services:list'))
        self.assertIn(self.service1.name, response.content.decode())
        self.assertIn(self.service2.name, response.content.decode())
    
    def test_services_list_by_category(self):
        """Verificar filtrado por categoría"""
        response = self.client.get(reverse('services:list'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.service1.name, response.content.decode())
    
    def test_service_detail_no_login(self):
        """Verificar que el detalle de servicio es público"""
        response = self.client.get(reverse('services:detail', args=[self.service1.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_service_detail_contains_info(self):
        """Verificar que el detalle muestra la información del servicio"""
        response = self.client.get(reverse('services:detail', args=[self.service1.id]))
        self.assertIn(self.service1.name, response.content.decode())
        self.assertIn(str(self.service1.price), response.content.decode())


class AuthViewsTest(TestCase):
    """Tests para las vistas de autenticación"""
    
    def setUp(self):
        """Crear datos de prueba"""
        self.client = Client()
    
    def test_register_page_loads(self):
        """Verificar que la página de registro carga"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_register_valid(self):
        """Verificar registro válido"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_valid(self):
        """Verificar login válido"""
        User.objects.create_user(username='testuser', password='testpass123')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login_view'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_invalid(self):
        """Verificar login inválido"""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login_view'), data)
        self.assertEqual(response.status_code, 200)
        # El usuario no debe estar autenticado
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_logout(self):
        """Verificar logout"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout_view'), follow=True)
        self.assertEqual(response.status_code, 200)


class DashboardViewsTest(TestCase):
    """Tests para las vistas del dashboard"""
    
    def setUp(self):
        """Crear datos de prueba"""
        self.client = Client()
        
        # Crear usuario staff
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Crear usuario regular
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_dashboard_requires_staff(self):
        """Verificar que el dashboard requiere ser staff"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_dashboard_admin_access(self):
        """Verificar que admin puede acceder al dashboard"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_bookings_management_requires_staff(self):
        """Verificar que la gestión de reservas requiere staff"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:bookings'))
        self.assertEqual(response.status_code, 403)
    
    def test_revenue_report_requires_staff(self):
        """Verificar que el reporte de ingresos requiere staff"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:revenue'))
        self.assertEqual(response.status_code, 403)

