# Transcript - Reunión 27 Enero 2026

**Fecha:** 2026-01-27  
**Participantes:** Product Owner, Tech Lead, Backend Dev, Frontend Dev

---

## Contexto

Hemos detectado que muchos usuarios abandonan el carrito porque no pueden guardar productos para más tarde sin comprometerse a comprar. Quieren poder marcar productos como "wishlist" o "guardar para después" desde la vista del carrito.

---

## Requerimientos discutidos

### 1. Funcionalidad principal

**Product Owner:**  
"Necesitamos que desde el carrito, los usuarios puedan mover productos a una lista de deseos sin tener que eliminarlos del carrito y buscarlos de nuevo. Esto reducirá el abandono."

**Tech Lead:**  
"Propongo añadir un botón 'Guardar para después' en cada item del carrito. Esto moverá el producto del carrito a una lista wishlist persistente."

### 2. Persistencia

**Backend Dev:**  
"La wishlist debe persistir por userId para usuarios logueados. Para usuarios guest, la guardaremos en el cartId actual pero con un flag especial."

**Product Owner:**  
"Correcto, y cuando un usuario guest se loguee, su wishlist guest debe fusionarse con su wishlist de usuario."

### 3. Límites

**Frontend Dev:**  
"¿Hay límite de productos en la wishlist?"

**Product Owner:**  
"Por ahora, máximo 50 productos. Si intentan añadir más, mostramos un mensaje."

**Tech Lead:**  
"Ok, lo implementamos como una colección separada en MongoDB: `wishlists` con campos userId, items (array), y timestamps."

### 4. Endpoints necesarios

**Backend Dev:**  
"Necesitaremos:
- POST /v1/wishlist/items - Añadir producto a wishlist
- GET /v1/wishlist - Obtener wishlist del usuario
- DELETE /v1/wishlist/items/{sku} - Eliminar producto de wishlist
- POST /v1/wishlist/move-to-cart - Mover producto de wishlist a carrito"

**Product Owner:**  
"Perfecto. Y el primero debe aceptar que vengan desde el carrito, removiendo el producto del carrito automáticamente."

### 5. Servicios afectados

**Tech Lead:**  
"Esto afecta principalmente al Cart Service. Podemos extenderlo para gestionar la wishlist o crear un servicio separado."

**Backend Dev:**  
"Propongo añadirlo al Cart Service por ahora. Son operaciones relacionadas con la sesión de compra."

**Product Owner:**  
"De acuerdo. Prioridad alta, para el próximo sprint."

### 6. Frontend

**Frontend Dev:**  
"Necesito que el endpoint de añadir a wishlist me devuelva el carrito actualizado y la wishlist actualizada para refrescar la UI."

**Tech Lead:**  
"Ok, haremos que POST /v1/wishlist/items devuelva ambos objetos."

---

## Decisiones finales

1. ✅ Añadir funcionalidad de wishlist al Cart Service
2. ✅ Nueva colección MongoDB: `wishlists`
3. ✅ 4 nuevos endpoints REST
4. ✅ Máximo 50 productos por wishlist
5. ✅ Merge de wishlists en login (guest → user)
6. ✅ Al mover de carrito a wishlist, se elimina del carrito automáticamente
7. ✅ Respuestas incluyen carrito + wishlist para actualizar UI

---

## Próximos pasos

- Backend: Implementar endpoints y modelo de datos
- Frontend: Diseñar UI del botón "Guardar para después"
- QA: Casos de prueba para merge de wishlists
