"""
Tests para modelos del sistema de reservas
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, time

from accounts.models import UserProfile
from services.models import Category, Service, Availability
from bookings.models import Booking, Review


class UserProfileModelTest(TestCase):
    """Tests para el modelo UserProfile"""
    
    def setUp(self):
        """Crear datos de prueba"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation(self):
        """Verificar que se crea el perfil automáticamente"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_profile_string_representation(self):
        """Verificar la representación en string del perfil"""
        profile = self.user.profile
        self.assertEqual(str(profile), f"Perfil de {self.user.username}")
    
    def test_profile_notify_email_default(self):
        """Verificar que notify_email es True por defecto"""
        profile = self.user.profile
        self.assertTrue(profile.notify_email)
    
    def test_profile_fields(self):
        """Verificar que el perfil tiene todos los campos"""
        profile = self.user.profile
        self.assertTrue(hasattr(profile, 'phone'))
        self.assertTrue(hasattr(profile, 'document'))
        self.assertTrue(hasattr(profile, 'address'))
        self.assertTrue(hasattr(profile, 'bio'))
        self.assertTrue(hasattr(profile, 'avatar'))


class CategoryModelTest(TestCase):
    """Tests para el modelo Category"""
    
    def setUp(self):
        """Crear categoría de prueba"""
        self.category = Category.objects.create(
            name='Masajes',
            description='Servicios de masaje terapéutico',
            icon='🧖'
        )
    
    def test_category_creation(self):
        """Verificar creación de categoría"""
        self.assertEqual(self.category.name, 'Masajes')
        self.assertEqual(self.category.icon, '🧖')
    
    def test_category_string_representation(self):
        """Verificar representación en string"""
        self.assertEqual(str(self.category), 'Masajes')


class ServiceModelTest(TestCase):
    """Tests para el modelo Service"""
    
    def setUp(self):
        """Crear servicio de prueba"""
        self.category = Category.objects.create(name='Masajes', icon='🧖')
        self.service = Service.objects.create(
            name='Masaje Relajante',
            description='Masaje relajante de 60 minutos',
            category=self.category,
            duration_minutes=60,
            price=50.00,
            max_capacity=1
        )
    
    def test_service_creation(self):
        """Verificar creación de servicio"""
        self.assertEqual(self.service.name, 'Masaje Relajante')
        self.assertEqual(self.service.price, 50.00)
        self.assertEqual(self.service.duration_minutes, 60)
    
    def test_service_string_representation(self):
        """Verificar representación en string"""
        self.assertEqual(str(self.service), 'Masaje Relajante')
    
    def test_service_is_active_default(self):
        """Verificar que is_active es True por defecto"""
        self.assertTrue(self.service.is_active)
    
    def test_service_category_relationship(self):
        """Verificar relación con categoría"""
        self.assertEqual(self.service.category, self.category)


class AvailabilityModelTest(TestCase):
    """Tests para el modelo Availability"""
    
    def setUp(self):
        """Crear disponibilidad de prueba"""
        self.category = Category.objects.create(name='Masajes', icon='🧖')
        self.service = Service.objects.create(
            name='Masaje',
            category=self.category,
            duration_minutes=60,
            price=50.00
        )
        self.availability = Availability.objects.create(
            service=self.service,
            day_of_week=0,  # Monday
            start_time=time(9, 0),
            end_time=time(17, 0)
        )
    
    def test_availability_creation(self):
        """Verificar creación de disponibilidad"""
        self.assertEqual(self.availability.day_of_week, 0)
        self.assertEqual(self.availability.start_time, time(9, 0))
    
    def test_availability_string_representation(self):
        """Verificar representación en string"""
        self.assertIn('Masaje', str(self.availability))


class BookingModelTest(TestCase):
    """Tests para el modelo Booking"""
    
    def setUp(self):
        """Crear reserva de prueba"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Masajes', icon='🧖')
        self.service = Service.objects.create(
            name='Masaje',
            category=self.category,
            duration_minutes=60,
            price=50.00
        )
        self.tomorrow = timezone.now().date() + timedelta(days=1)
        self.booking = Booking.objects.create(
            user=self.user,
            service=self.service,
            booking_date=self.tomorrow,
            booking_time=time(10, 0),
            total_price=50.00
        )
    
    def test_booking_creation(self):
        """Verificar creación de reserva"""
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.service, self.service)
        self.assertEqual(self.booking.total_price, 50.00)
    
    def test_booking_status_default(self):
        """Verificar que status es 'pending' por defecto"""
        self.assertEqual(self.booking.status, 'pending')
    
    def test_booking_string_representation(self):
        """Verificar representación en string"""
        self.assertIn(self.service.name, str(self.booking))
    
    def test_is_past_future_booking(self):
        """Verificar que una reserva futura no está en el pasado"""
        self.assertFalse(self.booking.is_past())
    
    def test_is_past_past_booking(self):
        """Verificar que una reserva pasada sí está en el pasado"""
        past_booking = Booking.objects.create(
            user=self.user,
            service=self.service,
            booking_date=timezone.now().date() - timedelta(days=1),
            booking_time=time(10, 0),
            total_price=50.00
        )
        self.assertTrue(past_booking.is_past())
    
    def test_can_be_cancelled_pending(self):
        """Verificar que una reserva pendiente puede ser cancelada"""
        self.assertTrue(self.booking.can_be_cancelled())
    
    def test_can_be_cancelled_confirmed(self):
        """Verificar que una reserva confirmada puede ser cancelada"""
        self.booking.status = 'confirmed'
        self.booking.save()
        self.assertTrue(self.booking.can_be_cancelled())
    
    def test_can_be_cancelled_completed(self):
        """Verificar que una reserva completada NO puede ser cancelada"""
        self.booking.status = 'completed'
        self.booking.save()
        self.assertFalse(self.booking.can_be_cancelled())
    
    def test_can_be_cancelled_cancelled(self):
        """Verificar que una reserva cancelada NO puede ser cancelada"""
        self.booking.status = 'cancelled'
        self.booking.save()
        self.assertFalse(self.booking.can_be_cancelled())
    
    def test_cancel_method(self):
        """Verificar que el método cancel funciona"""
        result = self.booking.cancel(reason='Cambio de planes')
        self.assertTrue(result)
        self.assertEqual(self.booking.status, 'cancelled')
        self.assertEqual(self.booking.cancellation_reason, 'Cambio de planes')
    
    def test_end_time_calculation(self):
        """Verificar cálculo de hora de finalización"""
        # Booking de 60 minutos comenzando a las 10:00
        end = self.booking.end_time
        self.assertEqual(end.hour, 11)
        self.assertEqual(end.minute, 0)


class ReviewModelTest(TestCase):
    """Tests para el modelo Review"""
    
    def setUp(self):
        """Crear reseña de prueba"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Masajes', icon='🧖')
        self.service = Service.objects.create(
            name='Masaje',
            category=self.category,
            duration_minutes=60,
            price=50.00
        )
        self.booking = Booking.objects.create(
            user=self.user,
            service=self.service,
            booking_date=timezone.now().date() - timedelta(days=1),
            booking_time=time(10, 0),
            total_price=50.00
        )
        self.review = Review.objects.create(
            booking=self.booking,
            rating=5,
            comment='Excelente servicio'
        )
    
    def test_review_creation(self):
        """Verificar creación de reseña"""
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Excelente servicio')
    
    def test_review_string_representation(self):
        """Verificar representación en string"""
        self.assertIn(str(self.review.rating), str(self.review))
    
    def test_review_rating_choices(self):
        """Verificar que las opciones de rating son válidas"""
        # Rating válido: 5
        self.assertEqual(self.review.rating, 5)
        
        # Crear reseña con rating diferente
        review_4 = Review.objects.create(
            booking=self.booking,
            rating=4,
            comment='Muy bueno'
        )
        self.assertEqual(review_4.rating, 4)

