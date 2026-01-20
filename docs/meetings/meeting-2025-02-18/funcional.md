# Documento funcional – Persistencia de carrito (2025-02-18)

## Descripción General

Se detecta que los usuarios pierden el carrito de la compra en determinadas situaciones (cierre de sesión, cambio de dispositivo o navegador, cierre de la app en mobile). Esto genera abandono y frustración, ya que los usuarios esperan que el carrito persista como ocurre en otros e-commerce. Se decide modificar la lógica para que el carrito se asocie al usuario cuando esté logueado y se recupere al iniciar sesión.

- **HU:**  
- **Figma:**  

---

## Lógica Funcional

Actualmente, el carrito se crea sin asociarse a ningún usuario y se guarda únicamente en el frontend mediante un `cartId`. Si se pierde la sesión, el carrito se pierde y no hay forma de recuperarlo.  
La nueva lógica será:

- Persistir el carrito por `userId` cuando el usuario esté logueado.
- Al hacer login, recuperar el carrito activo del usuario.
- Mantener el funcionamiento actual para usuarios guest.
- Solo se permitirá un carrito activo por usuario (no se realizará merge de carritos por el momento).

---

## Lógica Frontend

- El frontend debe guardar el `cartId` como hasta ahora para usuarios guest.
- Al hacer login, debe solicitar al backend el carrito activo asociado al usuario y mostrarlo.
- No se realizarán cambios en la lógica de merge de carritos.

---

## Lógica Backend

- El backend debe asociar el carrito al `userId` cuando el usuario esté logueado.
- Al iniciar sesión, el backend debe buscar y devolver el carrito activo del usuario.
- No se implementará lógica de merge de carritos en esta fase.

---

## Partes Afectadas

### Tipo de Usuario

Aplica a usuarios logados y usuarios anónimos (guest).

---