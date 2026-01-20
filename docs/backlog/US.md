# US-001 - Persistencia de carrito para usuarios logueados

---

## Identificación

- **ID:** US-001
- **Fecha:** 2025-02-18  
- **Servicio:** cart-service

---

## User Story

Como usuario logueado quiero que mi carrito de la compra se mantenga y recupere automáticamente al iniciar sesión para evitar perder mis productos y mejorar mi experiencia de compra.

---

## Descripción

Actualmente, los usuarios pierden el carrito de la compra al cerrar sesión, cambiar de dispositivo/navegador o cerrar la app móvil, lo que genera frustración y abandono. Se propone persistir el carrito asociado al `userId` cuando el usuario está logueado y recuperarlo automáticamente al hacer login. Para usuarios guest, se mantiene el funcionamiento actual. Solo se permitirá un carrito activo por usuario logueado y no se realizará merge de carritos en esta fase.

---

## Cambios

### Qué se añadió

- Persistencia del carrito asociada al `userId` para usuarios logueados.
- Recuperación automática del carrito al hacer login.
- Mantener la lógica actual para usuarios guest.
- Solo un carrito activo por usuario logueado (sin merge de carritos).

---

## Impacto en APIs

### Nuevo endpoint

- Endpoint para recuperar el carrito activo asociado al `userId` al hacer login.