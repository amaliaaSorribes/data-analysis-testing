# US-108 - Persist cart by userId

---

## Identificación

- **ID:** US-108
- **Fecha:** 2025-02-18
- **Servicio:** cart-service

---

## User Story

Como usuario logueado quiero que mi carrito de la compra se asocie a mi cuenta y se recupere automáticamente al iniciar sesión para no perder mis productos y continuar mi compra en cualquier dispositivo.

---

## Descripción

Actualmente, el carrito de la compra solo se guarda en el frontend mediante un `cartId` y no se asocia a ningún usuario, lo que provoca que se pierda al cerrar sesión, cambiar de dispositivo o cerrar la app. Se propone modificar la lógica para que, cuando el usuario esté logueado, el carrito se asocie a su `userId` y se recupere automáticamente al iniciar sesión. Para usuarios guest, el funcionamiento actual se mantiene. No se realizará merge de carritos en esta fase.

---

## Cambios

### Qué se añadió

- Persistencia del carrito por `userId` para usuarios logueados.
- Recuperación automática del carrito activo al iniciar sesión.
- Mantener el funcionamiento actual para usuarios guest.
- Solo un carrito activo por usuario logueado (sin lógica de merge).

---

## Impacto en APIs

### Nuevo endpoint

- Endpoint para recuperar el carrito activo asociado a un `userId` al hacer login.

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2025-02-18/funcional.md)
