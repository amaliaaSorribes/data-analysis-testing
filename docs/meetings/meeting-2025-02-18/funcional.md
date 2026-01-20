# 999. Documento funcional – Persistencia de carrito por usuario

## Descripción General

Actualmente, los usuarios pierden el carrito de compra en determinadas situaciones (cierre de sesión, cambio de dispositivo o navegador, o al volver tras varios días). Esto genera abandono y frustración, especialmente en mobile. El objetivo es persistir el carrito asociado al usuario logueado, de modo que se recupere automáticamente al iniciar sesión.

---

## Lógica Funcional

- El carrito debe asociarse al `userId` cuando el usuario está logueado.
- Al hacer login, se debe recuperar el carrito activo asociado al usuario.
- Solo puede haber un carrito activo por usuario (no se realizará merge de carritos en esta fase).
- Los carritos de usuarios no logueados (guest carts) seguirán funcionando como hasta ahora.
- Si el usuario pierde la sesión, el carrito se recuperará al volver a iniciar sesión.

---

## Lógica Frontend

- El frontend debe solicitar el carrito asociado al usuario tras el login.
- Si el usuario no está logueado, se mantiene la lógica actual de carrito anónimo.
- No se realizan cambios en la gestión de carritos para usuarios no logueados.

---

## Lógica Backend

- El backend debe asociar el carrito al `userId` cuando el usuario está logueado.
- Al recibir una petición de login, el backend debe buscar y devolver el carrito activo del usuario.
- No se implementa lógica de merge de carritos en esta fase.
- Los carritos de usuarios anónimos no se asocian a ningún usuario.

---

## Partes Afectadas

### Tipo de Usuario

- Aplica a usuarios logados y anónimos (con diferencias en la persistencia del carrito).

---