# US-117 - Cart item quantity update validation

---

## Identificación

- **ID:** US-117
- **Fecha:** 2026-01-27
- **Servicio:** cart-service

---

## User Story

Como usuario del carrito quiero actualizar la cantidad de productos de manera segura y validada para evitar errores, duplicados y asegurar que los totales sean correctos.

---

## Descripción

Se requiere robustecer la validación y sincronización de las cantidades de productos en el carrito. El sistema debe validar que la cantidad ingresada sea mayor o igual a 1 y no supere el stock disponible, tanto en frontend como en backend. Se debe implementar debouncing para evitar múltiples requests simultáneos, mostrar estados de carga, realizar rollback en caso de error y proporcionar mensajes claros al usuario. El backend debe recalcular el total del carrito tras cada actualización y responder con la información actualizada. Además, se debe monitorear y registrar errores y requests duplicados.

---

## Cambios

### Qué se añadió

- Validación estricta de cantidades en backend (mayor o igual a 1 y menor o igual al stock).
- Debouncing de 500ms en frontend para evitar requests simultáneos.
- Deshabilitar input y mostrar estado de carga durante la actualización.
- Rollback de cantidad en caso de error.
- Mensajes de error claros y descriptivos.
- Sincronización en tiempo real con el stock disponible.
- Logging y monitoreo de errores y requests duplicados.
- Recalculo automático del total del carrito tras la actualización.

---

## Impacto en APIs

### Nuevo endpoint

- **PATCH /v1/carts/{cartId}/items/{itemId}**
  - **Request:** cantidad deseada
  - **Response:** { itemId, newQuantity, subtotal, cartTotal }
  - **Error 422:** incluir límites permitidos y mensaje descriptivo

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-27/funcional.md)
