# Documento Funcional – Persistencia de Carrito (2025-02-18)

## Descripción General

Actualmente, los usuarios pierden el carrito de la compra en distintas situaciones (cierre de sesión, cambio de dispositivo o navegador, cierre de la app en mobile). Esto genera abandono y frustración, ya que los usuarios esperan que el carrito se mantenga. Se decide persistir el carrito asociado al usuario cuando está logueado y recuperarlo al hacer login, manteniendo el funcionamiento actual para usuarios guest.

- **HU:**  
- **Figma:**  

---

## Lógica Funcional

- Asociar el carrito al `userId` cuando el usuario está logueado.
- Mantener el funcionamiento actual para carritos de usuario guest.
- Al hacer login, recuperar el carrito activo del usuario.
- Solo se permite un carrito activo por usuario (no se realizará merge de carritos por el momento).
- El objetivo es simplificar la solución en esta primera fase.

---

## Lógica Frontend

- Guardar el identificador del carrito (`cartId`) como hasta ahora para usuarios guest.
- Al hacer login, solicitar al backend el carrito asociado al usuario y mostrarlo.
- Si el usuario no tiene carrito asociado, mantener el comportamiento actual.

---

## Lógica Backend

- Persistir el carrito asociado al `userId` cuando el usuario está logueado.
- Al recibir una petición de login, buscar y devolver el carrito activo del usuario.
- No implementar lógica de merge de carritos en esta fase.
- Mantener la lógica actual para carritos de usuarios guest (no logueados).

---

## Partes Afectadas

*(No hay información en el transcript para completar esta sección, por lo que se elimina)*

---

## Nuevos servicios

*(No hay información en el transcript para completar esta sección, por lo que se elimina)*

---

## Dependencias con terceros

*(No hay información en el transcript para completar esta sección, por lo que se elimina)*

---

## Analítica

*(No hay información en el transcript para completar esta sección, por lo que se elimina)*

---

## Contingencias

*(No hay información en el transcript para completar esta sección, por lo que se elimina)*

---

## Tipo de Usuario

- Aplica tanto a usuarios anónimos (guest) como a usuarios logueados.

---

## Método de Envio

*(No hay información en el transcript para completar esta sección, por lo que se elimina)*

---

## Determinar tipo de mercancia

*(No hay información en el transcript para completar esta sección, por lo que se elimina)*

---

## Determinar ventanas de flujo afectadas

*(No hay información en el transcript para completar esta sección, por lo que se elimina)*