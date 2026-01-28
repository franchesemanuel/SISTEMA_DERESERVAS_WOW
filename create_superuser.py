"""
Script para crear superusuario automáticamente en producción
Ejecutar con: python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credenciales desde variables de entorno o valores por defecto
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@spahotel.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    print(f"🔑 Creando superusuario: {username}")
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superusuario {username} creado exitosamente")
    print(f"📧 Email: {email}")
    print(f"🔐 Password: {password}")
    print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login!")
else:
    print(f"ℹ️  Superusuario {username} ya existe")
