# Documento Funcional – Actualización de cantidades en carrito (2026-01-27)

## Descripción General

Se aborda la problemática reportada por usuarios al modificar las cantidades de productos en el carrito, donde se presentan errores de actualización, duplicados por clicks rápidos, aceptación de cantidades negativas y totales incorrectos. El objetivo es robustecer la validación y sincronización de cantidades, mejorando la experiencia y confianza del usuario.

---

## Lógica Funcional

- Validación estricta de cantidades tanto en frontend como en backend.
- Implementación de debouncing para evitar múltiples requests simultáneos.
- El backend debe validar que la cantidad sea mayor o igual a 1 y no supere el stock disponible.
- El frontend debe mostrar el estado de carga y realizar rollback si ocurre un error.
- El endpoint PATCH /v1/carts/{cartId}/items/{itemId} será el encargado de actualizar cantidades.
- La respuesta del backend debe incluir la cantidad actualizada y el total recalculado.
- Mensajes de error claros en caso de límites superados.
- Sincronización en tiempo real con el stock disponible.
- Logging y monitoreo de errores y requests duplicados.

---

## Lógica Frontend

- Implementar debounce de 500ms al modificar la cantidad de un producto en el carrito.
- Deshabilitar el input de cantidad durante la actualización.
- Mostrar un estado de carga mientras se procesa la petición.
- Realizar rollback a la cantidad anterior si ocurre un error.
- Consumir el endpoint PATCH /v1/carts/{cartId}/items/{itemId}.
- Actualizar la UI con la cantidad y el total recibidos en la respuesta.
- Mostrar mensajes de error claros, por ejemplo: "Stock disponible: 3 unidades".

---

## Lógica Backend

- Modificar el servicio de carrito para:
  - Validar que la cantidad sea mayor o igual a 1 y menor o igual al stock disponible.
  - Rechazar la petición si se supera el límite permitido.
  - Recalcular el total del carrito automáticamente tras la actualización.
  - Responder con un objeto que incluya: itemId, newQuantity, subtotal, cartTotal.
- Devolver error 422 con los límites permitidos si la validación falla.
- Consultar el stock disponible al validar la cantidad.
- Registrar logs de errores de validación y monitorear requests duplicados.

---

## Nuevos servicios

- Endpoint dedicado para actualización de cantidades:
  - PATCH /v1/carts/{cartId}/items/{itemId}
  - Request: cantidad deseada
  - Response: { itemId, newQuantity, subtotal, cartTotal }
  - Error 422: incluir límites permitidos y mensaje descriptivo

---

## Consideraciones

- Sincronización con stock en tiempo real.
- Mensajes de error claros para el usuario.
- Logging de errores de validación.
- Monitoreo de requests duplicados.

---