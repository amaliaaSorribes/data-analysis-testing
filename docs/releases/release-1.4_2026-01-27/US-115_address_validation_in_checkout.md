# US-115 - Address validation in checkout

---

## Identificación

- **ID:** US-115
- **Fecha:** 2026-01-27
- **Servicio:** cart-service

---

## User Story

Como usuario quiero que mi dirección de envío sea validada automáticamente durante el checkout para evitar errores y asegurar la correcta entrega de mi pedido.

---

## Descripción

Se integrará un servicio externo de validación de direcciones en el flujo de checkout. Al ingresar la dirección, el sistema validará el código postal mediante una API externa, autocompletará ciudad y provincia, y marcará los campos de dirección como obligatorios. La dirección será confirmada con el usuario antes de finalizar el pedido y solo se permitirá avanzar si la dirección es válida. Si la dirección es inválida, se mostrarán mensajes de error y sugerencias para corrección. La dirección validada y normalizada se guardará en el sistema.

---

## Cambios

### Qué se añadió

- Integración de un servicio externo de validación de direcciones en el checkout.
- Validación en tiempo real y autocompletado de ciudad/provincia según código postal.
- Confirmación y normalización de la dirección antes de procesar el pago.
- Mensajes de error y sugerencias en caso de dirección inválida.
- Almacenamiento de direcciones validadas por usuario.

---

## Impacto en APIs

### Nuevo endpoint

- **POST /v1/addresses/validate**
  - Request: `{ street, number, city, postalCode, province }`
  - Response: `{ valid: boolean, suggestions: [], normalized: {} }`

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-27/funcional.md)
