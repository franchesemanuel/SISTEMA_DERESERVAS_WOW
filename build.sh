#!/usr/bin/env bash
# Render Build Script
# Este script se ejecuta automáticamente durante el deploy en Render

set -o errexit  # Exit on error

echo "=========================================="
echo "🚀 INICIANDO BUILD EN RENDER"
echo "=========================================="

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ Dependencias instaladas"

# Colectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Static files recolectados"

# Ejecutar migraciones
echo "🗄️  Ejecutando migraciones..."
python manage.py migrate

echo "✅ Migraciones completadas"

echo "=========================================="
echo "✅ BUILD COMPLETADO EXITOSAMENTE"
echo "=========================================="
