# ⚡ COMANDOS RÁPIDOS PARA RENDER

## 🔑 Generar SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📦 Git Push
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

## 🔍 Verificar Deploy Local Antes de Push
```bash
# Activar venv
source venv/bin/activate

# Simular producción
export DEBUG=False
export SECRET_KEY="test-key-for-local-testing-only"
export ALLOWED_HOSTS="localhost,127.0.0.1"

# Colectar static files
python manage.py collectstatic --noinput

# Ejecutar con Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000

# En otro terminal, probar
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/services/
```

## 🗄️ Comandos PostgreSQL (si usas DB externa)
```bash
# En Render Shell
python manage.py migrate
python manage.py createsuperuser
python create_superuser.py  # Automático
```

## 📊 Ver Logs en Render
1. Dashboard → Tu servicio → "Logs"
2. O usar Render CLI:
```bash
# Instalar CLI
npm install -g render-cli

# Login
render login

# Ver logs
render logs -s spa-wellness-booking --tail
```

## 🔄 Forzar Redeploy Manual
1. Dashboard → Tu servicio → "Manual Deploy"
2. Seleccionar branch: `main`
3. Click "Deploy"

## 🧪 Probar Endpoints Críticos
```bash
# Reemplazar con tu URL de Render
URL="https://spa-wellness-booking.onrender.com"

# Home
curl -I $URL/

# Servicios
curl -I $URL/services/

# Admin (debe retornar 200 con login form)
curl -I $URL/admin/

# Dashboard (debe redirigir a login)
curl -I $URL/dashboard/

# Static CSS (debe retornar 200)
curl -I $URL/static/css/base.css
```

## 🔐 Variables de Entorno (Render Dashboard)

| Variable | Valor Ejemplo | Requerida |
|----------|---------------|-----------|
| `PYTHON_VERSION` | `3.12.0` | ✅ |
| `DEBUG` | `False` | ✅ |
| `SECRET_KEY` | `<generar>` | ✅ |
| `ALLOWED_HOSTS` | `.onrender.com` | ✅ |
| `CSRF_TRUSTED_ORIGINS` | `https://tu-app.onrender.com` | ✅ |
| `DATABASE_URL` | `postgresql://...` | ⚠️ Solo si usas PostgreSQL |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | ⚠️ Opcional |
| `DJANGO_SUPERUSER_EMAIL` | `admin@demo.com` | ⚠️ Opcional |
| `DJANGO_SUPERUSER_PASSWORD` | `Demo123!` | ⚠️ Opcional |

## 🐛 Debug Rápido

### Ver configuración Django en producción:
```bash
# En Render Shell
python manage.py diffsettings
```

### Verificar migraciones pendientes:
```bash
python manage.py showmigrations
```

### Test de health check:
```bash
python manage.py check --deploy
```

## 📁 Estructura de Archivos para Render

```
/
├── build.sh                  ← Build script (ejecutable)
├── Procfile                  ← Opcional (Render usa Start Command)
├── render.yaml               ← Configuración automática
├── requirements.txt          ← Dependencias
├── create_superuser.py       ← Script para superuser
├── config/
│   ├── settings.py           ← Configuración producción
│   └── wsgi.py               ← WSGI app
├── manage.py
├── .env.example              ← Template (NO committear .env)
└── .gitignore                ← Excluir .env, logs/, db.sqlite3
```

## 🚨 Errores Comunes y Soluciones Rápidas

### 1. "Application failed to respond"
```bash
# Verificar Start Command en Render:
gunicorn config.wsgi:application

# Ver logs detallados
render logs -s spa-wellness-booking --tail
```

### 2. "DisallowedHost"
```bash
# En Environment Variables, ALLOWED_HOSTS debe incluir:
.onrender.com,localhost,127.0.0.1
```

### 3. "CSRF verification failed"
```bash
# CSRF_TRUSTED_ORIGINS debe ser HTTPS:
https://spa-wellness-booking.onrender.com

# NO usar http:// en producción
```

### 4. Static files 404
```bash
# En Render Shell:
python manage.py collectstatic --noinput --clear

# Verificar MIDDLEWARE en settings.py tiene:
# 'whitenoise.middleware.WhiteNoiseMiddleware'
```

### 5. Database reset en cada deploy
```bash
# Causa: SQLite sin persistencia
# Solución: Usar PostgreSQL
# En Render: New → PostgreSQL → Copiar DATABASE_URL
```

## 📈 Monitoreo Post-Deploy

```bash
# Health check cada 5 minutos
watch -n 300 curl -I https://tu-app.onrender.com/

# Logs en tiempo real (Render CLI)
render logs -s spa-wellness-booking --tail --follow
```

## 🔄 Workflow Típico de Desarrollo

```bash
# 1. Desarrollo local
python manage.py runserver

# 2. Probar cambios
# ... hacer pruebas ...

# 3. Commit
git add .
git commit -m "Feature: nueva funcionalidad"

# 4. Push (trigger auto-deploy)
git push origin main

# 5. Esperar 3-5 min

# 6. Verificar en producción
curl https://tu-app.onrender.com/

# 7. Si falla, ver logs y corregir
render logs -s spa-wellness-booking --tail
```

## ✅ Checklist Pre-Push

- [ ] `python manage.py check` sin errores
- [ ] `python manage.py test` pasa (si hay tests)
- [ ] `python manage.py collectstatic` funciona
- [ ] `.env` NO está en git (verificar `.gitignore`)
- [ ] `DEBUG=False` probado localmente
- [ ] Commit message descriptivo

## 🎯 URLs Importantes

- **Render Dashboard:** https://dashboard.render.com/
- **Tu App:** https://spa-wellness-booking.onrender.com
- **Django Admin:** https://spa-wellness-booking.onrender.com/admin/
- **API Docs (si tienes):** https://spa-wellness-booking.onrender.com/api/docs/

---

**¡Todo listo para deploy! 🚀**
