# US-118 - Payment Processing Timeout Handling

---

## Identificación

- **ID:** US-118
- **Fecha:** 2026-01-28
- **Servicio:** cart-service

---

## User Story

Como usuario del checkout quiero que el procesamiento de pagos maneje adecuadamente los timeouts y evite dobles cargos para tener una experiencia de compra segura y sin incertidumbre.

---

## Descripción

Se requiere optimizar el flujo de procesamiento de pagos para manejar correctamente los timeouts y evitar incidencias como dobles cargos o abandono del proceso. La solución propuesta incluye aumentar el timeout del Payment Service a 90 segundos, implementar un estado intermedio "processing" para los intentos de pago, utilizar idempotency keys únicas por sesión y carrito, y registrar cada intento de pago. El frontend mostrará un mensaje informativo durante el procesamiento, realizará polling periódico para consultar el estado del pago y deshabilitará el botón de pago tras el primer click. Además, se implementarán un endpoint para consultar el estado del pago y un webhook para recibir confirmaciones de la pasarela de pago.

---

## Cambios

### Qué se añadió

- Aumento del timeout HTTP del Payment Service a 90 segundos.
- Estado intermedio "processing" para intentos de pago.
- Generación y almacenamiento de idempotency key única por sesión y carrito.
- Registro detallado de cada intento de pago en una nueva colección payment_attempts.
- Endpoint GET para consultar el estado del pago.
- Webhook POST para recibir confirmaciones de la pasarela.
- Polling periódico desde frontend para actualizar el estado del pago.
- Mensaje claro al usuario durante el procesamiento.
- Prevención de dobles cargos mediante idempotency key.
- Logs y monitoreo de tiempos de respuesta.

---

## Impacto en APIs

### Nuevo endpoint

- `GET /v1/payments/{paymentId}/status`: Permite consultar el estado del pago.
- `POST /v1/payments/webhook`: Recibe confirmaciones de la pasarela de pago.

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-28/funcional.md)
