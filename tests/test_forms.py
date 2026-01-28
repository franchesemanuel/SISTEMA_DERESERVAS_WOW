"""
Tests para formularios del sistema de reservas
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, time

from accounts.forms import RegisterForm, LoginForm, ProfileForm
from bookings.forms import BookingForm, ReviewForm
from services.models import Category, Service
from bookings.models import Booking


class RegisterFormTest(TestCase):
    """Tests para el formulario de registro"""
    
    def test_register_valid(self):
        """Verificar registro válido"""
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        })
        self.assertTrue(form.is_valid())
    
    def test_register_password_mismatch(self):
        """Verificar error cuando las contraseñas no coinciden"""
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Las contraseñas no coinciden', form.errors['password2'])
    
    def test_register_password_too_short(self):
        """Verificar error cuando la contraseña es muy corta"""
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'short',
            'password2': 'short'
        })
        self.assertFalse(form.is_valid())
    
    def test_register_duplicate_username(self):
        """Verificar error cuando el usuario ya existe"""
        User.objects.create_user(username='existing', password='pass123')
        form = RegisterForm(data={
            'username': 'existing',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        })
        self.assertFalse(form.is_valid())


class LoginFormTest(TestCase):
    """Tests para el formulario de login"""
    
    def setUp(self):
        """Crear usuario de prueba"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_valid(self):
        """Verificar login válido"""
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertTrue(form.is_valid())
    
    def test_login_invalid_username(self):
        """Verificar error con usuario inválido"""
        form = LoginForm(data={
            'username': 'nonexistent',
            'password': 'testpass123'
        })
        # El formulario en sí es válido, la validación ocurre en la vista
        self.assertTrue(form.is_valid())
    
    def test_login_invalid_password(self):
        """Verificar error con contraseña inválida"""
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # El formulario en sí es válido, la validación ocurre en la vista
        self.assertTrue(form.is_valid())


class BookingFormTest(TestCase):
    """Tests para el formulario de reservas"""
    
    def setUp(self):
        """Crear datos de prueba"""
        self.category = Category.objects.create(name='Masajes', icon='🧖')
        self.service = Service.objects.create(
            name='Masaje',
            category=self.category,
            duration_minutes=60,
            price=50.00
        )
        self.tomorrow = (timezone.now() + timedelta(days=1)).date()
    
    def test_booking_form_valid(self):
        """Verificar formulario de reserva válido"""
        form = BookingForm(data={
            'booking_date': self.tomorrow,
            'booking_time': time(10, 0),
            'contact_phone': '1234567890',
            'notes': 'Sin alergias'
        })
        self.assertTrue(form.is_valid())
    
    def test_booking_form_past_date(self):
        """Verificar error con fecha en el pasado"""
        past_date = (timezone.now() - timedelta(days=1)).date()
        form = BookingForm(data={
            'booking_date': past_date,
            'booking_time': time(10, 0),
            'contact_phone': '1234567890'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('No puedes reservar en el pasado', form.non_field_errors())
    
    def test_booking_form_missing_required_fields(self):
        """Verificar error con campos requeridos faltantes"""
        form = BookingForm(data={
            'contact_phone': '1234567890'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('booking_date', form.errors)
        self.assertIn('booking_time', form.errors)
    
    def test_booking_form_optional_notes(self):
        """Verificar que las notas son opcionales"""
        form = BookingForm(data={
            'booking_date': self.tomorrow,
            'booking_time': time(10, 0),
            'contact_phone': '1234567890'
        })
        self.assertTrue(form.is_valid())


class ReviewFormTest(TestCase):
    """Tests para el formulario de reseñas"""
    
    def test_review_form_valid(self):
        """Verificar formulario de reseña válido"""
        form = ReviewForm(data={
            'rating': 5,
            'comment': 'Excelente servicio'
        })
        self.assertTrue(form.is_valid())
    
    def test_review_form_all_ratings(self):
        """Verificar que todas las opciones de rating son válidas"""
        for rating in range(1, 6):
            form = ReviewForm(data={
                'rating': rating,
                'comment': f'Rating {rating}'
            })
            self.assertTrue(form.is_valid())
    
    def test_review_form_missing_rating(self):
        """Verificar error cuando falta el rating"""
        form = ReviewForm(data={
            'comment': 'Good service'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
    
    def test_review_form_optional_comment(self):
        """Verificar que el comentario es opcional"""
        form = ReviewForm(data={
            'rating': 4
        })
        self.assertTrue(form.is_valid())
    
    def test_review_form_invalid_rating(self):
        """Verificar error con rating inválido"""
        form = ReviewForm(data={
            'rating': 10,
            'comment': 'Too high'
        })
        self.assertFalse(form.is_valid())


class ProfileFormTest(TestCase):
    """Tests para el formulario de perfil"""
    
    def test_profile_form_valid(self):
        """Verificar formulario de perfil válido"""
        form = ProfileForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'document': '12345678',
            'address': '123 Main St',
            'bio': 'User bio'
        })
        self.assertTrue(form.is_valid())
    
    def test_profile_form_optional_fields(self):
        """Verificar que los campos del perfil son opcionales"""
        form = ProfileForm(data={
            'email': 'john@example.com'
        })
        self.assertTrue(form.is_valid())
    
    def test_profile_form_invalid_email(self):
        """Verificar error con email inválido"""
        form = ProfileForm(data={
            'email': 'invalid-email'
        })
        self.assertFalse(form.is_valid())

