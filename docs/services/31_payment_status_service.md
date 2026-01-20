# Payment Status Service

## Responsabilidad
El **Payment Status Service** es responsable de la **gestión del estado del pago** asociado a un pedido. Permite consultar el estado mediante **polling**, recibir **callbacks simulados** del proveedor de pagos (PSP) y mantener la persistencia del estado del pago.

Este servicio actúa como **fuente de verdad del estado de pago**, enlazando cada pago con su pedido correspondiente.

---

## Endpoints

### GET `/v1/payments/{paymentId}` — Obtener estado de pago
Devuelve el estado actual de un pago específico.

**Response (200)**
```json
{
  "paymentId": "UUID",
  "orderId": "UUID",
  "status": "AUTHORIZED",
  "amount": 48.38,
  "currency": "EUR"
}
```

---

### GET `/v1/orders/{orderId}/payment-status` — Obtener estado de pago por pedido

Devuelve el estado del pago asociado a un pedido.

**Response (200)**

```json
{
  "orderId": "UUID",
  "paymentId": "UUID",
  "status": "AUTHORIZED"
}
```

---

### POST `/v1/payments/webhook` — Webhook de pago (simulado)

Endpoint que simula la recepción de eventos de un proveedor de pagos (PSP).

**Request**

```json
{
  "paymentId": "UUID",
  "orderId": "UUID",
  "status": "PAID",
  "provider": "PSP_SIMULATED"
}
´´´

**Response(200)***

```json
{
  "received": true
}

```

---

## Modelo (payments)

### Colección

* **Nombre:** `payments`

### Descripción

La colección `payments` almacena el estado del pago y su relación con un pedido.

### Campos principales

* `paymentId`
* `orderId`
* `status`
* `amount`
* `currency`
* `provider`
* `createdAt`
* `updatedAt`

El esquema detallado se describe en `02_modelo_datos_mongo.md`.

---

### Eventos

`payment.status.changed`

Evento publicado cuando cambia el estado de un pago.

**Motivo**

* Notificar a otros servicios (por ejemplo, Checkout Service) de cambios en el estado del pago.

**Payload ejemplo**

```json
{
  "eventId": "UUID",
  "eventType": "payment.status.changed",
  "occurredAt": "2026-01-15T11:00:00Z",
  "payload": {
    "paymentId": "UUID",
    "orderId": "UUID",
    "status": "PAID"
  },
  "sourceService": "payment-status-service"
}