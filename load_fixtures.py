"""
Script para cargar datos de prueba en la base de datos
Ejecutar: python manage.py shell < load_fixtures.py
"""

from services.models import Category, Service, Availability
from datetime import time

# Crear categorías
masajes_cat, _ = Category.objects.get_or_create(
    name='Masajes',
    defaults={'icon': '💆‍♀️', 'description': 'Masajes relajantes y terapéuticos'}
)

faciales_cat, _ = Category.objects.get_or_create(
    name='Faciales',
    defaults={'icon': '✨', 'description': 'Tratamientos faciales personalizados'}
)

spa_cat, _ = Category.objects.get_or_create(
    name='Spa y Bienestar',
    defaults={'icon': '🧖', 'description': 'Experiencias completas de spa'}
)

# Crear servicios
services_data = [
    {
        'category': masajes_cat,
        'name': 'Masaje Relajante',
        'description': 'Masaje suave y relajante para aliviar el estrés',
        'duration_minutes': 60,
        'price': 50.00,
    },
    {
        'category': masajes_cat,
        'name': 'Masaje Descontracturante',
        'description': 'Masaje profundo para aliviar tensiones musculares',
        'duration_minutes': 90,
        'price': 75.00,
    },
    {
        'category': masajes_cat,
        'name': 'Masaje Hot Stones',
        'description': 'Masaje con piedras calientes',
        'duration_minutes': 75,
        'price': 85.00,
    },
    {
        'category': faciales_cat,
        'name': 'Facial Limpieza Profunda',
        'description': 'Limpieza profunda y exfoliación facial',
        'duration_minutes': 60,
        'price': 45.00,
    },
    {
        'category': faciales_cat,
        'name': 'Facial Antienvejecimiento',
        'description': 'Tratamiento anti-edad con productos premium',
        'duration_minutes': 75,
        'price': 65.00,
    },
    {
        'category': spa_cat,
        'name': 'Paquete Relax Total',
        'description': 'Masaje + sauna + jacuzzi',
        'duration_minutes': 120,
        'price': 120.00,
        'max_capacity': 2,
    },
    {
        'category': spa_cat,
        'name': 'Ritual de Pareja',
        'description': 'Experiencia spa para parejas',
        'duration_minutes': 120,
        'price': 180.00,
        'max_capacity': 2,
    },
]

for data in services_data:
    service, created = Service.objects.get_or_create(
        name=data['name'],
        category=data['category'],
        defaults={k: v for k, v in data.items() if k != 'category'}
    )
    if created:
        print(f"✅ Servicio creado: {service.name}")
    
    # Crear disponibilidades (Lunes a Sábado, 9 AM a 7 PM)
    for day in range(6):  # 0 = Lunes, 5 = Sábado
        Availability.objects.get_or_create(
            service=service,
            day_of_week=day,
            defaults={
                'start_time': time(9, 0),
                'end_time': time(19, 0),
                'is_available': True,
            }
        )

print("\n✅ Datos de prueba cargados exitosamente")
print(f"Total servicios: {Service.objects.count()}")
print(f"Total disponibilidades: {Availability.objects.count()}")
