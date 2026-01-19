# 03 — Eventos y colas

## 1. Propósito del documento
Este documento describe el **modelo de eventos y colas** utilizado en el sistema Cart & Checkout. Define los **topics/colas**, los **eventos publicados**, sus **productores y consumidores**, y los **contratos de evento** a nivel funcional y técnico ligero.

La mensajería se describe de forma **abstracta** (Kafka / RabbitMQ), sin dependencia de una tecnología concreta.

---

## 2. Lista de topics / colas (abstracto)

| Topic / Cola | Tipo | Dominio |
|--------------|------|--------|
| `catalog.events` | Topic | Catálogo |
| `pricing.events` | Topic | Pricing |
| `promotions.events` | Topic | Promociones |
| `cart.events` | Topic | Carrito |
| `checkout.events` | Topic | Checkout |
| `payment.events` | Topic | Pagos |

---

## 3. Eventos de ingesta

### 3.1 `catalog.product.upserted`

- **Productor**: Catalog Ingestion Service  
- **Consumidores**: Cart Service, Pricing Service  
- **Motivo**: Notificar la creación o actualización de un producto del catálogo.

**Payload ejemplo**
```json
{
  "eventId": "UUID",
  "eventType": "catalog.product.upserted",
  "occurredAt": "2026-01-10T09:00:00Z",
  "payload": {
    "sku": "SKU-12345",
    "active": true
  },
  "sourceService": "catalog-ingestion-service"
}
```

**Clave de partición / ordering:** `sku`
**Idempotency key:** `eventId`

---

### 3.2 `pricing.price.updated`

* **Productor:** Pricing Ingestion Service
* **Consumidores:** Pricing Service
* **Motivo:** Propagar cambios de precios base para su uso en cálculos de totales.

**Payload ejemplo**

```json
{
  "eventId": "UUID",
  "eventType": "pricing.price.updated",
  "occurredAt": "2026-01-10T09:05:00Z",
  "payload": {
    "sku": "SKU-12345",
    "currency": "EUR",
    "amount": 19.99
  },
  "sourceService": "pricing-ingestion-service"
}
```

**Clave de partición / ordering:** `sku`
**Idempotency key:** `eventId`

---

### 3.3 `promotions.promo.published`

* **Productor:** Promotions Ingestion Service
* **Consumidores:** Promotion Engine Service
* **Motivo:** Publicar promociones activas o modificadas.

**Payload ejemplo**

```json
{
  "eventId": "UUID",
  "eventType": "promotions.promo.published",
  "occurredAt": "2026-01-10T09:10:00Z",
  "payload": {
    "promotionId": "PROMO-2026-01",
    "active": true
  },
  "sourceService": "promotions-ingestion-service"
}
```
**Clave de partición / ordering:** `sku`
**Idempotency key:** `eventId`

---

## 4. Eventos transaccionales

### 4.1 `cart.cart.updated`

* **Productor:** Cart Service
* **Consumidores:** Checkout Service
* **Motivo:** Informar de cambios relevantes en el estado del carrito.

**Payload ejemplo**

```json
{
  "eventId": "UUID",
  "eventType": "cart.cart.updated",
  "occurredAt": "2026-01-15T10:30:00Z",
  "payload": {
    "cartId": "UUID",
    "status": "ACTIVE",
    "total": 34.98
  },
  "sourceService": "cart-service"
}
```

**Clave de partición / ordering:** `cartId`
**Idempotency key:** `eventId`

---

### 4.2 `checkout.order.created`

* **Productor:** Checkout Service
* **Consumidores:** Payment Status Service, Tracking Service
* **Motivo:** Notificar la creación de un pedido pendiente de pago.

**Payload ejemplo**

```json
{
  "eventId": "UUID",
  "eventType": "checkout.order.created",
  "occurredAt": "2026-01-15T10:45:00Z",
  "payload": {
    "orderId": "UUID",
    "amount": 34.98,
    "currency": "EUR"
  },
  "sourceService": "checkout-service"
}
```

**Clave de partición / ordering:** `orderId`
**Idempotency key:** `eventId`

---

### 4.3 `payment.status.changed`

* **Productor:** Payment Status Service
* **Consumidores:** Checkout Service
* **Motivo:** Propagar cambios en el estado del pago.

**Payload ejemplo**

```json
{
  "eventId": "UUID",
  "eventType": "payment.status.changed",
  "occurredAt": "2026-01-15T10:50:00Z",
  "payload": {
    "paymentId": "UUID",
    "orderId": "UUID",
    "status": "AUTHORIZED"
  },
  "sourceService": "payment-status-service"
}
```

**Clave de partición / ordering:** `orderId`
**Idempotency key:** `eventId`

---

## 5. Contratos de evento (schema)

Todos los eventos comparten un schema base común:

```json
{
  "eventId": "UUID",
  "eventType": "string",
  "occurredAt": "ISO-8601 UTC",
  "payload": {},
  "sourceService": "string"
}
```

**Reglas**

* `eventId` es único globalmente.
* `eventType` identifica de forma inequívoca el evento.
* `payload` contien solo la información mínima necesaria.
* No se incluyen datos sensibles.


---

# 6. Estrategias de reintento / DLQ (alto nivel)

* Los consumidores deben ser **idempotentes**.
* Los fallos transitorios se reintentan automáticamente.
* Tras superar el número máximo de reintentos, el mensaje se envía a una **Dead Letter Queue (DLQ)**.
* Los mensajes en DLQ requieren análisis manual o reprocesado controlado.
* El reprocesado debe respetar la idempotencia basada en `eventId`.