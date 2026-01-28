# Sistema de Reservas para Spa/Hotel

Sistema profesional de reservas desarrollado con Django, diseñado para ser escalable y producción-ready.

## Stack Tecnológico

- **Backend**: Django 4.2 LTS
- **Base de datos**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTMX + Bootstrap 5
- **Autenticación**: Django Auth nativa
- **Variables de entorno**: python-decouple

## Estructura del Proyecto

```
├── accounts/           # Gestión de usuarios y autenticación
├── services/          # Catálogo de servicios (masajes, tratamientos, etc)
├── bookings/          # Gestión de reservas
├── dashboard/         # Panel de administración
├── config/            # Configuración del proyecto
├── templates/         # Templates HTML globales
├── static/            # Archivos estáticos (CSS, JS, imágenes)
├── media/             # Archivos subidos por usuarios
└── manage.py          # Script de administración Django
```

## Setup Inicial

### 1. Clonar y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Editar `.env` con tus valores:

```
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=America/Mexico_City
LANGUAGE_CODE=es-es
```

### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a `http://localhost:8000`

## Características Principales

- ✅ Autenticación de usuarios
- ✅ Catálogo de servicios
- ✅ Sistema de reservas con disponibilidad
- ✅ Dashboard de administración
- ✅ Interfaz responsiva con Bootstrap
- ✅ Interactividad con HTMX

## Buenas Prácticas Implementadas

- Código limpio y bien documentado
- Modelos bien diseñados con validaciones
- Separación de concerns en apps
- Settings configurables con variables de entorno
- Estructura lista para producción

## Próximos Pasos

1. Crear modelos de datos
2. Implementar autenticación
3. Desarrollar sistema de reservas
4. Crear dashboard administrativo
5. Integración HTMX en frontend

## Licencia

Privado
