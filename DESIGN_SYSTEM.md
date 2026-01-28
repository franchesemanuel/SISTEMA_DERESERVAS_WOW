# SISTEMA DE DISEÑO - SERENITY SPA

## 📋 Índice
1. [Visión General](#visión-general)
2. [Paleta de Colores](#paleta-de-colores)
3. [Tipografía](#tipografía)
4. [Componentes](#componentes)
5. [Uso en Templates](#uso-en-templates)

---

## 🎨 Visión General

### Concepto
**Estilo:** Spa wellness / Hotel boutique moderno  
**Filosofía:** Premium, limpio, elegante, tranquilo  
**Inspiración:** Minimalismo escandinavo + elegancia mediterránea  

### Características Clave
- ✅ Mobile-first responsive
- ✅ Colores naturales y tranquilos
- ✅ Tipografía combinada: serif para títulos, sans-serif para cuerpo
- ✅ Espaciado generoso y aireado
- ✅ Sombras sutiles y transiciones suaves
- ✅ Sin elementos genéricos ni sobrecargados

---

## 🎨 Paleta de Colores

### Primarios
```css
--color-primary: #2c5f5d;        /* Verde azulado profundo - confianza */
--color-primary-light: #4a8886;   /* Verde azulado medio */
--color-primary-dark: #1a3f3e;    /* Verde azulado oscuro */
```
**Uso:** Botones principales, enlaces, headers, elementos de marca

### Acentos
```css
--color-accent: #d4af37;          /* Dorado suave - elegancia premium */
--color-accent-light: #e5c766;    /* Dorado claro */
--color-accent-dark: #b8941f;     /* Dorado oscuro */
```
**Uso:** CTAs especiales, badges premium, detalles destacados

### Neutros
```css
--color-white: #ffffff;
--color-ivory: #fafaf8;           /* Fondo general */
--color-sand: #f5f3f0;            /* Cards, secciones alternas */
--color-stone: #e8e6e3;           /* Bordes, divisores */
--color-slate: #8b8985;           /* Texto secundario */
--color-charcoal: #3d3d3d;        /* Texto principal */
--color-black: #1a1a1a;           /* Títulos, texto fuerte */
```

### Estados
```css
--color-success: #4a9d7f;         /* Verde wellness - confirmaciones */
--color-warning: #d4a574;         /* Ámbar suave - advertencias */
--color-error: #c77b7b;           /* Coral suave - errores */
--color-info: #6b9eb8;            /* Azul tranquilo - info */
```

---

## ✍️ Tipografía

### Fuentes
```html
<!-- En <head> -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
```

**Playfair Display** - Títulos (serif elegante)  
**Inter** - Cuerpo y UI (sans-serif moderna)

### Escala Tipográfica
```
h1: 36px (2.25rem)  → Títulos principales
h2: 30px (1.875rem) → Secciones
h3: 24px (1.5rem)   → Subsecciones
h4: 20px (1.25rem)  → Cards, títulos pequeños
body: 16px (1rem)   → Texto general
small: 14px (.875rem) → Ayudas, labels
```

---

## 🧩 Componentes

### Botones
```html
<!-- Primario -->
<a href="#" class="btn-spa btn-spa-primary">Reservar Ahora</a>

<!-- Acento (dorado) -->
<button class="btn-spa btn-spa-accent">Ver Servicios</button>

<!-- Outline -->
<button class="btn-spa btn-spa-outline">Cancelar</button>

<!-- Ghost (transparente) -->
<button class="btn-spa btn-spa-ghost">Ver más</button>

<!-- Tamaños -->
<button class="btn-spa btn-spa-primary btn-spa-sm">Pequeño</button>
<button class="btn-spa btn-spa-primary">Normal</button>
<button class="btn-spa btn-spa-primary btn-spa-lg">Grande</button>
```

### Cards
```html
<div class="card-spa">
    <div class="card-spa-header">
        <h3 class="card-spa-title">Masaje Relajante</h3>
        <p class="card-spa-subtitle">60 minutos de pura relajación</p>
    </div>
    
    <div class="card-spa-body">
        <p>Descripción del servicio...</p>
    </div>
    
    <div class="card-spa-footer">
        <button class="btn-spa btn-spa-outline btn-spa-sm">Detalles</button>
        <button class="btn-spa btn-spa-primary btn-spa-sm">Reservar</button>
    </div>
</div>
```

### Formularios
```html
<form class="form-spa">
    <div class="form-group-spa">
        <label class="form-label-spa" for="email">Email</label>
        <input type="email" id="email" class="form-input-spa" placeholder="tu@email.com">
        <p class="form-helper-spa">Usaremos este email para confirmaciones</p>
    </div>
    
    <div class="form-group-spa">
        <label class="form-label-spa" for="message">Mensaje</label>
        <textarea id="message" class="form-textarea-spa" placeholder="Tu mensaje..."></textarea>
    </div>
    
    <button type="submit" class="btn-spa btn-spa-primary">Enviar</button>
</form>
```

### Alerts
```html
<!-- Success -->
<div class="alert-spa alert-spa-success">
    <div>
        <strong>✓</strong>
        <span>Reserva confirmada exitosamente</span>
    </div>
    <button type="button" class="alert-spa-close">×</button>
</div>

<!-- Error -->
<div class="alert-spa alert-spa-error">
    <div>
        <strong>✕</strong>
        <span>Ocurrió un error. Inténtalo de nuevo.</span>
    </div>
    <button type="button" class="alert-spa-close">×</button>
</div>

<!-- Warning -->
<div class="alert-spa alert-spa-warning">
    <div>
        <strong>⚠</strong>
        <span>Tu sesión expirará pronto</span>
    </div>
</div>

<!-- Info -->
<div class="alert-spa alert-spa-info">
    <div>
        <strong>ℹ</strong>
        <span>Información importante</span>
    </div>
</div>
```

### Badges
```html
<span class="badge-spa badge-spa-primary">Nuevo</span>
<span class="badge-spa badge-spa-accent">Premium</span>
<span class="badge-spa badge-spa-success">Confirmado</span>
<span class="badge-spa badge-spa-warning">Pendiente</span>
```

---

## 📱 Uso en Templates Django

### Estructura Base
```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Mi Página{% endblock %}

{% block content %}
<div class="container-spa">
    <h1>Título de la Página</h1>
    
    <!-- Tu contenido aquí -->
    
</div>
{% endblock %}
```

### Ejemplo de Página Completa
```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Servicios - Serenity Spa{% endblock %}

{% block content %}
<div class="container-spa">
    <!-- Hero Section -->
    <div class="text-center mb-8">
        <h1>Nuestros Servicios</h1>
        <p class="text-lg" style="color: var(--color-slate); max-width: 600px; margin: 0 auto;">
            Descubre nuestra selección de tratamientos diseñados para tu bienestar
        </p>
    </div>
    
    <!-- Grid de Cards -->
    <div class="row g-4">
        {% for service in services %}
        <div class="col-md-6 col-lg-4">
            <div class="card-spa">
                <div class="card-spa-header">
                    <h3 class="card-spa-title">{{ service.name }}</h3>
                    <p class="card-spa-subtitle">{{ service.duration }} min · ${{ service.price }}</p>
                </div>
                
                <div class="card-spa-body">
                    <p>{{ service.description|truncatewords:20 }}</p>
                </div>
                
                <div class="card-spa-footer">
                    <a href="{% url 'services:detail' service.id %}" class="btn-spa btn-spa-outline btn-spa-sm">
                        Ver detalles
                    </a>
                    <a href="{% url 'bookings:create' service.id %}" class="btn-spa btn-spa-primary btn-spa-sm">
                        Reservar
                    </a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

---

## 🎯 Mejores Prácticas

### ✅ DO (Hacer)
- Usar clases con prefijo `-spa` para componentes personalizados
- Mantener espaciado generoso (usar variables de spacing)
- Combinar tipografías: Playfair para h1-h3, Inter para body
- Usar colores de la paleta definida
- Mobile-first: diseñar primero para móvil
- Transiciones sutiles (250-350ms)
- Sombras suaves para profundidad

### ❌ DON'T (Evitar)
- Usar clases Bootstrap genéricas para componentes principales
- Colores fuera de la paleta (excepto blanco/negro puro)
- Múltiples tipografías (máx. 2 familias)
- Animaciones excesivas o distractoras
- Botones sin espacio entre ellos
- Cards sin hover effects
- Formularios sin feedback visual

---

## 📐 Sistema de Espaciado

Basado en múltiplos de 8px:
```css
--space-1: 4px    /* Muy pequeño */
--space-2: 8px    /* Pequeño */
--space-3: 12px   /* Compacto */
--space-4: 16px   /* Normal */
--space-5: 24px   /* Mediano */
--space-6: 32px   /* Grande */
--space-8: 48px   /* Muy grande */
--space-10: 64px  /* Extra grande */
```

### Uso común:
- **Padding cards:** `var(--space-6)` (32px)
- **Gap entre elementos:** `var(--space-4)` (16px)
- **Margin secciones:** `var(--space-8)` (48px)
- **Padding botones:** `var(--space-3) var(--space-5)` (12px 24px)

---

## 🔄 Extensión del Sistema

### Para agregar nuevos componentes:
1. Seguir convención de nomenclatura: `.componente-spa`
2. Usar variables CSS existentes
3. Mantener consistencia visual
4. Documentar en este archivo

### Para nuevos colores:
Solo agregar si es **absolutamente necesario**. La paleta actual cubre:
- Primarios: marca, navegación
- Acentos: premium, CTAs
- Neutros: fondos, textos, bordes
- Estados: success, warning, error, info

---

## 📝 Notas Finales

### Compatibilidad
- ✅ Chrome, Firefox, Safari, Edge (últimas 2 versiones)
- ✅ iOS Safari 12+
- ✅ Android Chrome 80+

### Performance
- CSS: ~30KB (comprimido ~8KB)
- Fuentes: Google Fonts optimizadas con preconnect
- Sin dependencias JS adicionales (solo Bootstrap bundle para navbar)

### Accesibilidad
- Contraste mínimo WCAG AA cumplido
- Focus states visibles
- Labels descriptivos
- Navegación por teclado funcional

---

**Última actualización:** 28 de enero de 2026  
**Versión:** 1.0  
**Autor:** Sistema de Diseño Serenity Spa
