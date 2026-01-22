# Notas reunión – Cambio en endpoint de añadir al carrito

Fecha: 2025-03-18  
Asistentes: Backend, Frontend, Producto  
Tema: Unificar comportamiento de add-to-cart

---

- Se detecta comportamiento distinto entre web y app al añadir productos
- En web se usa POST /v1/cart/items
- En app se usa POST /v2/cart/add
- Esto genera inconsistencias en precios y promos

---

## Situación actual

- Dos endpoints distintos
- Lógica duplicada
- A veces el precio calculado no coincide
- Promociones se aplican de forma diferente

---

## Propuesta técnica

- Unificar en un solo endpoint:
  - POST /v2/cart/items
- El endpoint:
  - recibe productId y quantity
  - recalcula precios y promociones
  - devuelve el carrito completo
- Frontend web y app usarían el mismo endpoint

---

## Impacto en servicios

- Cart Service:
  - nueva versión del endpoint
- Pricing Service:
  - se invoca siempre en add-to-cart
- Promotion Engine:
  - se aplica en el mismo flujo

---

## Decisiones

- Se elimina el endpoint antiguo de app
- Se mantiene compatibilidad temporal para web
- No se cambia el modelo de datos

---

## Dudas pendientes

- Cuánto tiempo mantener compatibilidad
- Si hay que versionar el endpoint antiguo
- Qué pasa con clientes antiguos de la app

---

## Comentarios finales

- Crear US técnica
- Documentar bien el endpoint nuevo
- Coordinar con frontend
