# 🚀 CHECKLIST DE DEPLOYMENT - SPA WELLNESS BOOKING SYSTEM

## 📋 RESUMEN DE CAMBIOS IMPLEMENTADOS

### ✅ 1. Settings.py - Configuración para Producción

**Cambios aplicados:**
- ✅ `DEBUG` controlado por variable de entorno (.env)
- ✅ `SECRET_KEY` desde variable de entorno
- ✅ `ALLOWED_HOSTS` configurable desde .env
- ✅ `CSRF_TRUSTED_ORIGINS` agregado para HTTPS
- ✅ WhiteNoise integrado en MIDDLEWARE
- ✅ `STORAGES` configurado para WhiteNoise
- ✅ `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE` activados en producción
- ✅ `SECURE_SSL_REDIRECT` activado en producción
- ✅ Logging configurado (console + file rotating)
- ✅ HSTS listo para activar (comentado)

### ✅ 2. Archivos Nuevos Creados

```
.env.example          ← Template de variables de entorno
Procfile              ← Configuración para Heroku/Railway/Render
requirements.txt      ← Dependencias limpias (10 paquetes)
logs/                 ← Directorio para logs (creado)
```

### ✅ 3. Dependencias Instaladas

```
Django==4.2.14        ← Framework
python-decouple==3.8  ← Variables de entorno
gunicorn==23.0.0      ← WSGI server para producción
whitenoise==6.8.2     ← Servir archivos estáticos
django-csp==4.0       ← Content Security Policy
reportlab==4.4.9      ← Generación de PDFs
openpyxl==3.1.5       ← Generación de Excel
Pillow==12.1.0        ← Manejo de imágenes
```

---

## 🔍 VERIFICACIÓN PRE-DEPLOYMENT

### **Paso 1: Verificar Variables de Entorno**

```bash
# Copiar .env.example a .env
cp .env.example .env

# Editar .env con valores reales
nano .env
```

**Variables OBLIGATORIAS para producción:**
```env
DEBUG=False
SECRET_KEY=<generar-clave-segura-de-50+-caracteres>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Generar SECRET_KEY segura:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### **Paso 2: Verificar Django Check (Deployment)**

```bash
# Activar venv
source venv/bin/activate

# Ejecutar deployment checklist
python manage.py check --deploy
```

**Output esperado (desarrollo con DEBUG=True):**
```
WARNINGS:
  security.W004  HSTS no configurado (normal en dev)
  security.W008  SSL_REDIRECT no activado (normal en dev)
  security.W012  SESSION_COOKIE_SECURE no activado (normal en dev)
  security.W016  CSRF_COOKIE_SECURE no activado (normal en dev)
  security.W018  DEBUG=True (cambiar a False en producción)
```

**Output esperado (producción con DEBUG=False y .env correcto):**
```
System check identified no issues (0 silenced).
```

---

### **Paso 3: Verificar Static Files**

```bash
# Colectar archivos estáticos
python manage.py collectstatic --noinput
```

**Output esperado:**
```
126 static files copied to '/path/staticfiles', 378 post-processed.
```

**Verificar que funciona:**
```bash
# Iniciar con Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000

# En otra terminal, verificar CSS carga
curl -I http://127.0.0.1:8000/static/css/base.css
# Debe devolver: HTTP/1.1 200 OK
```

---

### **Paso 4: Verificar Migraciones**

```bash
# Verificar migraciones pendientes
python manage.py makemigrations --check --dry-run

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (si no existe)
python manage.py createsuperuser
```

---

### **Paso 5: Verificar Logging**

```bash
# Verificar que el directorio logs/ existe
ls -la logs/

# Iniciar servidor y generar un error intencional
python manage.py runserver

# En otra terminal, causar un 404
curl http://127.0.0.1:8000/pagina-que-no-existe

# Verificar que se generó log
cat logs/django.log
```

---

### **Paso 6: Verificar Seguridad (Headers)**

```bash
# Iniciar servidor
python manage.py runserver 8001

# Verificar headers de seguridad
curl -I http://127.0.0.1:8001/login/ | grep -E "(X-Frame|X-Content|CSP|Referrer)"
```

**Headers esperados:**
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Content-Security-Policy: default-src 'self'; ...
```

---

## 🌐 DEPLOYMENT A PRODUCCIÓN

### **Opción 1: Render.com**

1. Crear `render.yaml`:
```yaml
services:
  - type: web
    name: spa-wellness
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
    startCommand: gunicorn config.wsgi:application
    envVars:
      - key: DEBUG
        value: False
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: .onrender.com
      - key: CSRF_TRUSTED_ORIGINS
        value: https://your-app.onrender.com
```

2. Variables de entorno en Render Dashboard:
   - `DEBUG=False`
   - `SECRET_KEY=<generar>`
   - `ALLOWED_HOSTS=your-app.onrender.com`
   - `CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com`

---

### **Opción 2: Railway.app**

1. Conectar repositorio Git
2. Configurar variables de entorno:
   ```
   DEBUG=False
   SECRET_KEY=<generar>
   ALLOWED_HOSTS=$RAILWAY_PUBLIC_DOMAIN
   CSRF_TRUSTED_ORIGINS=https://$RAILWAY_PUBLIC_DOMAIN
   ```
3. Railway detecta `Procfile` automáticamente

---

### **Opción 3: Heroku**

```bash
# Login
heroku login

# Crear app
heroku create your-spa-wellness

# Configurar variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=<generar>
heroku config:set ALLOWED_HOSTS=your-spa-wellness.herokuapp.com
heroku config:set CSRF_TRUSTED_ORIGINS=https://your-spa-wellness.herokuapp.com

# Deploy
git push heroku main

# Ejecutar migraciones
heroku run python manage.py migrate

# Crear superusuario
heroku run python manage.py createsuperuser
```

---

## ⚠️ CHECKLIST FINAL PRE-DEPLOY

### **Desarrollo (DEBUG=True)**
- [x] `.env` existe con `DEBUG=True`
- [x] `SECRET_KEY` configurado en `.env`
- [x] `python manage.py check` sin errores críticos
- [x] `python manage.py migrate` ejecutado
- [x] `python manage.py collectstatic` funciona
- [x] Servidor corre con `python manage.py runserver`
- [x] Admin accesible en `/admin/`
- [x] Static files cargan correctamente

### **Producción (DEBUG=False)**
- [ ] `.env` con `DEBUG=False`
- [ ] `SECRET_KEY` segura (50+ caracteres, aleatoria)
- [ ] `ALLOWED_HOSTS` con dominio real
- [ ] `CSRF_TRUSTED_ORIGINS` con https://
- [ ] `python manage.py check --deploy` sin warnings críticos
- [ ] `python manage.py migrate` ejecutado en producción
- [ ] `python manage.py collectstatic --noinput` ejecutado
- [ ] Gunicorn funciona: `gunicorn config.wsgi:application`
- [ ] Logs se generan en `logs/django.log`
- [ ] Headers de seguridad activos (curl -I)
- [ ] HTTPS activo en dominio
- [ ] Backups de base de datos configurados
- [ ] Monitoreo de errores configurado (opcional: Sentry)

---

## 🔒 ACTIVAR HSTS (SOLO DESPUÉS DE HTTPS VERIFICADO)

**IMPORTANTE:** HSTS es **irreversible** por 1 año. Solo activar cuando HTTPS esté 100% funcional.

En `config/settings.py`, descomentar:
```python
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

## 📊 COMANDOS DE MONITOREO

```bash
# Ver logs en tiempo real (producción)
tail -f logs/django.log

# Ver últimos errores
grep ERROR logs/django.log | tail -20

# Verificar procesos Gunicorn
ps aux | grep gunicorn

# Reiniciar Gunicorn (si se usa supervisor)
supervisorctl restart spa-wellness

# Verificar uso de recursos
htop
```

---

## 🐛 TROUBLESHOOTING

### **Error: Static files no cargan**
```bash
# Verificar STATIC_ROOT
python manage.py findstatic css/base.css

# Recolectar static files
python manage.py collectstatic --clear --noinput

# Verificar WhiteNoise en MIDDLEWARE
grep -n "whitenoise" config/settings.py
```

### **Error: CSRF verification failed**
```bash
# Verificar CSRF_TRUSTED_ORIGINS en .env
echo $CSRF_TRUSTED_ORIGINS

# Debe incluir https:// y dominio exacto
# Ejemplo: https://yourdomain.com,https://www.yourdomain.com
```

### **Error: 500 Internal Server Error**
```bash
# Ver logs detallados
cat logs/django.log | grep ERROR

# Verificar variables de entorno
python manage.py diffsettings
```

---

## ✅ CONCLUSIÓN

El proyecto está **listo para producción** con:
- ✅ Configuración segura (headers, cookies, CSRF)
- ✅ Static files optimizados (WhiteNoise + compression)
- ✅ Logging configurado (rotating file handler)
- ✅ Gunicorn instalado y Procfile creado
- ✅ Variables de entorno separadas (.env.example)
- ✅ Deployment checklist completo

**Próximos pasos:**
1. Crear `.env` con valores reales
2. Ejecutar `python manage.py check --deploy` con `DEBUG=False`
3. Desplegar en plataforma elegida (Render/Railway/Heroku)
4. Verificar HTTPS funcional
5. Activar HSTS (opcional, después de HTTPS)
