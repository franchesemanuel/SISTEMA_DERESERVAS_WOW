# 🚀 GUÍA DE DEPLOYMENT EN RENDER.COM

## 📋 PRE-REQUISITOS

- [x] Cuenta en GitHub
- [x] Cuenta en Render.com (gratuita)
- [x] Proyecto Django listo
- [x] Git instalado

---

## 🔧 PASO 1: PREPARAR REPOSITORIO GITHUB

### 1.1 Inicializar Git (si no está inicializado)

```bash
cd "/Users/francoemanuelsalcedo/Desktop/SISTEMA DE RESERVAS _WOW"

# Inicializar git
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit - Django Spa Wellness Booking System"
```

### 1.2 Crear Repositorio en GitHub

1. Ir a https://github.com/new
2. Nombre: `spa-wellness-booking` (o el que prefieras)
3. Descripción: `Django Spa & Wellness Booking System`
4. Visibilidad: **Public** o **Private**
5. **NO** inicializar con README (ya tenemos archivos)
6. Click en "Create repository"

### 1.3 Conectar y Push

```bash
# Conectar con GitHub (reemplaza TU_USUARIO con tu username)
git remote add origin https://github.com/TU_USUARIO/spa-wellness-booking.git

# Verificar rama principal (debe ser main o master)
git branch -M main

# Push
git push -u origin main
```

**✅ Verificar:** Refrescar GitHub, debes ver todos los archivos subidos.

---

## 🌐 PASO 2: CREAR SERVICIO WEB EN RENDER

### 2.1 Conectar GitHub a Render

1. Ir a https://render.com/
2. Click en **"Sign In"** o **"Get Started"**
3. Seleccionar **"Sign in with GitHub"**
4. Autorizar Render para acceder a tus repositorios

### 2.2 Crear Nuevo Web Service

1. En Render Dashboard, click **"New +"** → **"Web Service"**
2. Conectar repositorio:
   - Si ves tu repo `spa-wellness-booking`: Click **"Connect"**
   - Si no lo ves: Click **"Configure account"** → Autorizar repositorio específico
3. Configurar servicio:

**Name:**
```
spa-wellness-booking
```

**Region:**
```
Oregon (US West) o Frankfurt (EU Central) - el más cercano a ti
```

**Branch:**
```
main
```

**Root Directory:**
```
(dejar vacío)
```

**Runtime:**
```
Python 3
```

**Build Command:**
```
./build.sh
```

**Start Command:**
```
gunicorn config.wsgi:application
```

**Instance Type:**
```
Free
```

---

## 🔐 PASO 3: CONFIGURAR VARIABLES DE ENTORNO

En la sección **"Environment Variables"**, agregar:

### Variables OBLIGATORIAS:

| Key | Value | Notas |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.12.0` | Versión de Python |
| `DEBUG` | `False` | **CRÍTICO**: Siempre False en producción |
| `SECRET_KEY` | `<generar-nueva>` | Ver comando abajo |
| `ALLOWED_HOSTS` | `.onrender.com` | Render agrega automáticamente el dominio |
| `CSRF_TRUSTED_ORIGINS` | `https://spa-wellness-booking.onrender.com` | Reemplazar con tu URL |

### Variables OPCIONALES (Email):

| Key | Value | Notas |
|-----|-------|-------|
| `EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` | Para demo |
| `DEFAULT_FROM_EMAIL` | `noreply@spahotel.com` | Email por defecto |

### Variables DEMO (Superuser):

| Key | Value | Notas |
|-----|-------|-------|
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Usuario demo |
| `DJANGO_SUPERUSER_EMAIL` | `admin@demo.com` | Email demo |
| `DJANGO_SUPERUSER_PASSWORD` | `Demo123!` | **Cambiar después del deploy** |

### 🔑 Generar SECRET_KEY Segura

**En tu terminal local:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Output (ejemplo):**
```
django-insecure-7k8h#2@j$s9f!a%b^d&e*g(h+i-j_k~l1m2n3o4p5q6r7s8t9u0v
```

**Copiar ese valor completo y pegarlo en `SECRET_KEY`.**

---

## 🗄️ PASO 4: CONFIGURAR BASE DE DATOS (OPCIONAL)

### Opción A: SQLite (Demo Rápida) ✅ RECOMENDADO PARA DEMO

**No hacer nada.** El proyecto usará SQLite por defecto.

**Pros:**
- ✅ Gratis
- ✅ Sin configuración
- ✅ Deploy rápido

**Contras:**
- ❌ Se resetea cada deploy (datos se pierden)
- ❌ No apto para producción real

### Opción B: PostgreSQL (Producción) 🔥 RECOMENDADO PARA PRODUCCIÓN

1. En Render Dashboard: **"New +"** → **"PostgreSQL"**
2. Configurar:
   - **Name:** `spa-wellness-db`
   - **Database:** `spa_wellness`
   - **User:** `spa_admin`
   - **Region:** Mismo que tu Web Service
   - **Instance Type:** `Free`
3. Click **"Create Database"**
4. Esperar ~2 minutos (estado: Available)
5. En la página de la DB, copiar **"Internal Database URL"**
6. Volver a tu Web Service → Environment Variables
7. Agregar:
   - **Key:** `DATABASE_URL`
   - **Value:** `<pegar-internal-database-url>`

**✅ Verificar:** Variable `DATABASE_URL` debe empezar con `postgresql://`

---

## ▶️ PASO 5: DEPLOY

### 5.1 Iniciar Deploy

1. Scroll al final de la configuración
2. Click **"Create Web Service"**
3. Render comenzará automáticamente el deploy

### 5.2 Monitorear Build

Verás un log en tiempo real. Busca estos mensajes:

```
==> Cloning from https://github.com/TU_USUARIO/spa-wellness-booking...
==> Downloading cache...
==> Installing dependencies...
📦 Instalando dependencias...
✅ Dependencias instaladas
📁 Recolectando archivos estáticos...
✅ Static files recolectados
🗄️  Ejecutando migraciones...
✅ Migraciones completadas
==> Build successful 🎉
==> Starting service...
==> Your service is live 🎉
```

**Tiempo estimado:** 3-5 minutos

### 5.3 Si el Build FALLA

**Errores comunes:**

| Error | Solución |
|-------|----------|
| `Permission denied: ./build.sh` | Ejecutar `chmod +x build.sh` localmente y hacer commit |
| `Module 'psycopg2' not found` | Verificar que `psycopg2-binary` esté en `requirements.txt` |
| `SECRET_KEY not set` | Verificar variable de entorno `SECRET_KEY` |
| `ALLOWED_HOSTS` error | Agregar `.onrender.com` a `ALLOWED_HOSTS` |

**Solución general:**
```bash
# Ver logs completos en Render → tu servicio → "Logs"
# Corregir el error
git add .
git commit -m "Fix: [descripción del error]"
git push
# Render hace auto-redeploy
```

---

## 👤 PASO 6: CREAR SUPERUSUARIO

### Opción A: Automático (Recomendado)

Si configuraste las variables `DJANGO_SUPERUSER_*`, ejecuta:

```bash
# En Render Shell (ver paso 6.2)
python create_superuser.py
```

### Opción B: Manual

1. En Render Dashboard → Tu servicio → **"Shell"** (pestaña superior)
2. Esperar que cargue la terminal
3. Ejecutar:

```bash
python manage.py createsuperuser
```

4. Completar:
   - Username: `admin`
   - Email: `admin@demo.com`
   - Password: `Demo123!` (mínimo 8 caracteres)
   - Password (again): `Demo123!`

**✅ Output esperado:**
```
Superuser created successfully.
```

---

## ✅ PASO 7: VERIFICAR DEPLOYMENT

### 7.1 Obtener URL

En Render Dashboard, verás la URL de tu app:

```
https://spa-wellness-booking.onrender.com
```

**Copiar esa URL.**

### 7.2 Verificar HTTPS

```bash
# En tu terminal local
curl -I https://spa-wellness-booking.onrender.com

# Debe devolver:
HTTP/2 200
strict-transport-security: max-age=31536000; includeSubDomains
x-frame-options: DENY
x-content-type-options: nosniff
```

**✅ HTTPS activo:** El candado 🔒 debe aparecer en el navegador.

### 7.3 Verificar Páginas Clave

| Página | URL | Estado Esperado |
|--------|-----|-----------------|
| Home | `/` | ✅ 200 OK |
| Servicios | `/services/` | ✅ 200 OK |
| Login | `/login/` | ✅ 200 OK |
| Dashboard (no autenticado) | `/dashboard/` | 🔒 Redirect a login |
| Admin | `/admin/` | ✅ 200 OK (login form) |

**Probar en navegador:**
```
https://spa-wellness-booking.onrender.com/
https://spa-wellness-booking.onrender.com/services/
https://spa-wellness-booking.onrender.com/login/
https://spa-wellness-booking.onrender.com/admin/
```

### 7.4 Login en Admin

1. Ir a `https://spa-wellness-booking.onrender.com/admin/`
2. Username: `admin`
3. Password: `Demo123!` (o el que configuraste)
4. Click **"Log in"**

**✅ Esperado:** Dashboard de Django Admin con menú lateral.

### 7.5 Verificar Static Files

**CSS debe cargar correctamente:**
```
https://spa-wellness-booking.onrender.com/static/css/base.css
```

**✅ Esperado:** Código CSS completo (no 404).

### 7.6 Crear Reserva de Prueba

1. Ir a `/services/`
2. Seleccionar un servicio
3. Click **"Reservar"**
4. Completar formulario
5. Confirmar reserva

**✅ Esperado:** 
- Formulario se envía sin errores
- Redirect a "Mis Reservas"
- Reserva visible en lista

---

## 📊 PASO 8: MONITOREO Y LOGS

### 8.1 Ver Logs en Tiempo Real

1. Render Dashboard → Tu servicio
2. Click en **"Logs"** (pestaña superior)
3. Ver stream en tiempo real

**Logs útiles:**
```
INFO 2026-01-28 django.request GET /services/ 200
ERROR 2026-01-28 django.request Internal Server Error: /booking/123/
INFO 2026-01-28 bookings User 5 created booking 42
```

### 8.2 Métricas

En **"Metrics"** tab:
- CPU usage
- Memory usage
- Request count
- Response time

**Free tier límites:**
- ✅ 750 horas/mes (siempre encendido)
- ✅ 100 GB bandwidth
- ⚠️ Se duerme después de 15 min inactividad (primer request tarda ~30s)

### 8.3 Health Checks

Render hace health checks automáticos a `/` cada 5 minutos.

**Si el servicio está caído:**
- Status: ❌ Failed
- Render lo reinicia automáticamente

---

## 🔧 PASO 9: CONFIGURACIONES POST-DEPLOY

### 9.1 Actualizar CSRF_TRUSTED_ORIGINS

Ahora que conoces tu URL exacta:

1. Render Dashboard → Environment Variables
2. Editar `CSRF_TRUSTED_ORIGINS`
3. Cambiar a: `https://tu-servicio-exacto.onrender.com`
4. Click **"Save Changes"**
5. Render hace redeploy automático

### 9.2 Dominio Personalizado (Opcional)

Si tienes un dominio (ej: `www.spawellness.com`):

1. Render Dashboard → Tu servicio → **"Settings"**
2. Sección **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Ingresar: `www.spawellness.com`
5. Render te da un CNAME record
6. Ir a tu proveedor de dominio (GoDaddy, Namecheap, etc.)
7. Agregar CNAME:
   - **Name:** `www`
   - **Value:** `tu-servicio.onrender.com`
8. Esperar propagación DNS (5-30 min)
9. Actualizar variables:
   - `ALLOWED_HOSTS`: `www.spawellness.com,.onrender.com`
   - `CSRF_TRUSTED_ORIGINS`: `https://www.spawellness.com`

### 9.3 Cambiar Password del Admin

**CRÍTICO PARA PRODUCCIÓN:**

1. Login en `/admin/`
2. Click en tu username (arriba derecha)
3. Click **"Change password"**
4. Ingresar password actual y nueva contraseña segura
5. Click **"Change my password"**

---

## 🐛 TROUBLESHOOTING

### Error: "Application failed to respond"

**Causa:** Gunicorn no arranca o crashea.

**Solución:**
```bash
# En Render Shell
gunicorn config.wsgi:application --bind 0.0.0.0:10000 --log-level debug

# Ver logs detallados
# Corregir el error en código local
git add .
git commit -m "Fix gunicorn startup"
git push
```

### Error: "DisallowedHost at /"

**Causa:** `ALLOWED_HOSTS` no incluye el dominio de Render.

**Solución:**
1. Environment Variables → `ALLOWED_HOSTS`
2. Cambiar a: `.onrender.com,localhost,127.0.0.1`
3. Save Changes

### Error: "CSRF verification failed"

**Causa:** `CSRF_TRUSTED_ORIGINS` incorrecto.

**Solución:**
1. Verificar que incluya `https://` (no `http://`)
2. Verificar que sea exactamente tu URL de Render
3. Ejemplo correcto: `https://spa-wellness-booking.onrender.com`

### Error: Static files no cargan (CSS roto)

**Causa:** `collectstatic` no se ejecutó o WhiteNoise mal configurado.

**Solución:**
```bash
# En Render Shell
python manage.py collectstatic --noinput

# Verificar STORAGES en settings.py
# Debe tener: whitenoise.storage.CompressedManifestStaticFilesStorage
```

### Error: Base de datos se resetea cada deploy

**Causa:** Usando SQLite sin volumen persistente.

**Solución:** Migrar a PostgreSQL (ver Paso 4, Opción B).

### Servicio se duerme (slow first request)

**Causa:** Free tier de Render duerme después de 15 min inactividad.

**Solución (opciones):**
1. **Aceptarlo:** Primer request tarda ~30s, luego normal
2. **Ping externo:** Usar UptimeRobot (gratis) para hacer ping cada 5 min
3. **Upgrade a Starter plan:** $7/mes, siempre activo

---

## 📋 CHECKLIST POST-DEPLOY

### Seguridad

- [ ] `DEBUG=False` verificado
- [ ] `SECRET_KEY` única y segura (50+ caracteres)
- [ ] `ALLOWED_HOSTS` correcto
- [ ] `CSRF_TRUSTED_ORIGINS` con `https://`
- [ ] HTTPS activo (candado 🔒 en navegador)
- [ ] Headers de seguridad presentes (X-Frame-Options, CSP, etc.)
- [ ] Password del admin cambiada

### Funcionalidad

- [ ] Home `/` carga correctamente
- [ ] Servicios `/services/` muestran lista
- [ ] Login `/login/` funciona
- [ ] Admin `/admin/` accesible
- [ ] Dashboard `/dashboard/` solo para staff
- [ ] Crear reserva funciona end-to-end
- [ ] Static files (CSS/JS) cargan
- [ ] Formularios CSRF funcionan

### Base de Datos

- [ ] Migraciones aplicadas (`python manage.py migrate`)
- [ ] Superusuario creado
- [ ] (Opcional) PostgreSQL conectada

### Monitoreo

- [ ] Logs visibles en Render
- [ ] Métricas activas
- [ ] Health checks pasando

---

## 🎉 DEPLOY EXITOSO

**Si todos los checks están ✅, tu aplicación está LIVE:**

```
🌐 URL: https://spa-wellness-booking.onrender.com
🔐 Admin: https://spa-wellness-booking.onrender.com/admin/
👤 User: admin
🔑 Pass: Demo123! (CAMBIAR INMEDIATAMENTE)
```

---

## 🔄 ACTUALIZACIONES FUTURAS

Cada vez que hagas cambios:

```bash
# 1. Hacer cambios en código local
# 2. Probar localmente
python manage.py runserver

# 3. Commit y push
git add .
git commit -m "Feature: descripción del cambio"
git push

# 4. Render hace auto-deploy (3-5 min)
# 5. Verificar en https://tu-app.onrender.com
```

**Render redeploya automáticamente en cada push a `main`.**

---

## 📞 SOPORTE

**Render Documentation:** https://render.com/docs
**Django Documentation:** https://docs.djangoproject.com/

**Errores comunes:** Ver sección Troubleshooting arriba.

---

**¡DEPLOYMENT COMPLETO! 🚀**
