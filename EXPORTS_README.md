# Export Reports - Sistema de Reservas SPA

## Descripción

El sistema incluye funcionalidad para exportar reportes en múltiples formatos: PDF y Excel. Los administradores pueden descargar reportes de ingresos y reservas para análisis y auditoría.

## Reportes Disponibles

### 1. Reporte de Ingresos PDF
- **URL:** `/dashboard/export/revenue/pdf/`
- **Formato:** PDF (reportlab)
- **Contenido:**
  - Ingresos totales, hoy y este mes
  - Tabla de ingresos por servicio
  - Formato profesional con colores y bordes
- **Acceso:** Botón en `/dashboard/revenue/`

### 2. Reporte de Ingresos Excel
- **URL:** `/dashboard/export/revenue/excel/`
- **Formato:** XLSX (openpyxl)
- **Contenido:**
  - Tabla resumida de ingresos
  - Tabla detallada por servicio
  - Formato con colores, bordes y números formateados
- **Acceso:** Botón en `/dashboard/revenue/`

### 3. Reporte de Reservas PDF
- **URL:** `/dashboard/export/bookings/pdf/`
- **Formato:** PDF (reportlab)
- **Contenido:**
  - Listado de últimas 100 reservas
  - Columnas: Usuario, Servicio, Fecha, Estado, Monto
  - Tabla formateada con colores
- **Acceso:** Botón en `/dashboard/bookings/`

### 4. Reporte de Reservas Excel
- **URL:** `/dashboard/export/bookings/excel/`
- **Formato:** XLSX (openpyxl)
- **Contenido:**
  - Listado de últimas 200 reservas
  - Columnas: Usuario, Servicio, Fecha, Estado, Monto
  - Formato con estilos profesionales
- **Acceso:** Botón en `/dashboard/bookings/`

## Estructura de Archivos

```
dashboard/
├── exports.py           # Vistas de exportación
├── views.py            # Vistas principales del dashboard
├── urls.py             # URLs con rutas de exportación
└── templates/
    ├── index.html
    ├── bookings_management.html (actualizado con botones)
    ├── revenue_report.html (actualizado con botones)
    ├── services_stats.html
    └── users_stats.html
```

## Funciones Disponibles

### PDF Exports

#### export_revenue_pdf(request)
```python
from dashboard.exports import export_revenue_pdf

# Ruta: /dashboard/export/revenue/pdf/
# Retorna: HttpResponse con PDF descargable
# Nombre archivo: reporte-ingresos.pdf
```

**Contenido:**
- Resumen de ingresos (total, hoy, este mes)
- Tabla de ingresos por servicio

#### export_bookings_pdf(request)
```python
from dashboard.exports import export_bookings_pdf

# Ruta: /dashboard/export/bookings/pdf/
# Retorna: HttpResponse con PDF descargable
# Nombre archivo: reporte-reservas.pdf
```

**Contenido:**
- Listado de últimas 100 reservas
- Información: usuario, servicio, fecha, estado, monto

### Excel Exports

#### export_revenue_excel(request)
```python
from dashboard.exports import export_revenue_excel

# Ruta: /dashboard/export/revenue/excel/
# Retorna: HttpResponse con XLSX descargable
# Nombre archivo: reporte-ingresos.xlsx
```

**Contenido:**
- Hoja "Ingresos"
- Resumen de ingresos
- Tabla de ingresos por servicio

#### export_bookings_excel(request)
```python
from dashboard.exports import export_bookings_excel

# Ruta: /dashboard/export/bookings/excel/
# Retorna: HttpResponse con XLSX descargable
# Nombre archivo: reporte-reservas.xlsx
```

**Contenido:**
- Hoja "Reservas"
- Listado de últimas 200 reservas

## Características Implementadas

### PDF (ReportLab)
- ✅ Estilos profesionales
- ✅ Colores temáticos (azul #007bff)
- ✅ Tablas con bordes y fondos
- ✅ Títulos y espaciado
- ✅ Múltiples páginas (automático)
- ✅ Formateo de moneda

### Excel (openpyxl)
- ✅ Estilos con colores
- ✅ Fuentes personalizadas (bold, tamaño)
- ✅ Bordes en todas las celdas
- ✅ Números formateados como moneda ($#,##0.00)
- ✅ Ancho de columnas ajustado
- ✅ Alineación centrada

## Seguridad

Todas las vistas tienen decoradores:
```python
@require_http_methods(["GET"])  # Solo GET
@login_required                  # Usuario autenticado
@user_passes_test(is_staff)     # Solo administradores
```

Los reportes solo están disponibles para usuarios staff (administradores).

## URLs Disponibles

```
GET /dashboard/export/revenue/pdf/       # Descargar PDF ingresos
GET /dashboard/export/revenue/excel/     # Descargar Excel ingresos
GET /dashboard/export/bookings/pdf/      # Descargar PDF reservas
GET /dashboard/export/bookings/excel/    # Descargar Excel reservas
```

## Uso en Templates

Botones de exportación en el dashboard:

```html
<div class="btn-group" role="group">
    <a href="{% url 'dashboard:export_revenue_pdf' %}" class="btn btn-outline-primary btn-sm">
        <i class="bi bi-file-pdf"></i> PDF
    </a>
    <a href="{% url 'dashboard:export_revenue_excel' %}" class="btn btn-outline-success btn-sm">
        <i class="bi bi-file-earmark-spreadsheet"></i> Excel
    </a>
</div>
```

## Ejemplo de Uso en Postman/cURL

```bash
# Descargar PDF de ingresos
curl -b "sessionid=YOUR_SESSION_ID" \
  http://localhost:8000/dashboard/export/revenue/pdf/ \
  -o reporte-ingresos.pdf

# Descargar Excel de reservas
curl -b "sessionid=YOUR_SESSION_ID" \
  http://localhost:8000/dashboard/export/bookings/excel/ \
  -o reporte-reservas.xlsx
```

## Datos Incluidos en Reportes

### Reporte de Ingresos
```
- Ingresos totales
- Ingresos de hoy
- Ingresos de este mes
- Desglose por servicio:
  * Nombre del servicio
  * Cantidad de reservas
  * Total de ingresos
```

### Reporte de Reservas
```
- Usuario (nombre completo o username)
- Servicio contratado
- Fecha de la reserva
- Estado (Pendiente, Confirmada, Completada, Cancelada)
- Monto total
```

## Próximos Pasos (Futuro)

1. **Más Formatos**
   - CSV export
   - JSON export
   - API REST para integración

2. **Filtrado Avanzado**
   - Reportes por rango de fechas
   - Filtrado por categoría de servicio
   - Filtrado por usuario específico

3. **Gráficos y Análisis**
   - Gráficos en PDF (usando reportlab charts)
   - Análisis de tendencias
   - Predicciones con datos históricos

4. **Automatización**
   - Reportes programados automáticos
   - Envío de reportes por email
   - Generación diaria/semanal/mensual

## Solución de Problemas

### "ImportError: No module named 'reportlab'"
```bash
pip install reportlab openpyxl
```

### "PDF no se descarga, muestra HTML"
- Verificar que el usuario es staff (`is_staff=True`)
- Verificar que está autenticado (`@login_required`)
- Revisar que las rutas están correctamente incluidas en `urls.py`

### "Excel muestra caracteres extraños"
- openpyxl maneja UTF-8 automáticamente
- Los números deben estar en formato correcto (float, no string)

### "Reporte vacío"
- Verificar que existen datos en la base de datos
- Los reportes filtran solo registros `paid=True` para ingresos
- Cambiar el query si es necesario

## Referencias

- ReportLab Documentation: https://www.reportlab.com/docs/reportlab-userguide.pdf
- openpyxl Documentation: https://openpyxl.readthedocs.io/

