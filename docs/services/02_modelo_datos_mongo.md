# 02 — Modelo de Datos MongoDB

## Propósito
Este documento describe el **modelo de datos en MongoDB** del sistema Cart & Checkout. Presenta un **catálogo de colecciones**, una por dominio funcional, detallando su propósito, estructura orientativa, campos clave, índices y consideraciones como TTL o versionado.

Cada colección tiene un **microservicio owner** responsable de su evolución.

---

## products
**Owner**: Catalog Ingestion Service  
**Dominio**: Catálogo

### Propósito
Almacenar la información normalizada de los productos disponibles para la venta.

### Esquema JSON orientativo
```json
{
  "_id": "ObjectId",
  "sku": "SKU-12345",
  "name": "Product name",
  "description": "Product description",
  "category": "electronics",
  "attributes": {
    "brand": "BrandX",
    "color": "black"
  },
  "active": true,
  "createdAt": "2026-01-01T10:00:00Z",
  "updatedAt": "2026-01-10T12:00:00Z",
  "version": 3
}
```
### Campos clave

* `sku`
* `active`

### Índices

* `{ sku: 1}` (unique)
* `{ active: 1}`

---

## prices

**Owner:** Pricing Ingestion Service
**Dominio:** Pricing

### Propósito

Persistir precios base por producto, canal, moneda y vigencia temporal.

### Esquema JSON orientativo

```json
{
  "_id": "ObjectId",
  "sku": "SKU-12345",
  "channel": "online",
  "currency": "EUR",
  "amount": 19.99,
  "effectiveFrom": "2026-01-01T00:00:00Z",
  "effectiveTo": "2026-12-31T23:59:59Z",
  "createdAt": "2026-01-01T10:00:00Z",
  "updatedAt": "2026-01-05T09:00:00Z",
  "version": 1
}
```

### Campos clave

* `sku`
* `channel`
* `currency`
* `effectiveFrom`, `effectiveTo`

### Índices

* `{ sku: 1, channel: 1, currency: 1, effectiveFrom: 1 }`

---

## promotions

**Owner:** Promotions Ingestion Service
**Dominio:** Promociones

### Propósito

Definir promociones, cupones y reglas de descuento aplicables.

### Esquema JSON orientativo

```json
{
  "_id": "ObjectId",
  "promotionId": "PROMO-2026-01",
  "type": "PERCENTAGE",
  "value": 10,
  "conditions": {
    "minAmount": 50
  },
  "couponCode": "SAVE10",
  "active": true,
  "validFrom": "2026-01-01T00:00:00Z",
  "validTo": "2026-01-31T23:59:59Z",
  "createdAt": "2025-12-20T10:00:00Z",
  "updatedAt": "2026-01-01T08:00:00Z",
  "version": 2
}
```

### Campos clave

* `promotionId`
* `active`
* `validFrom`, `validTo`

### Índices

* `{ promotionId: 1 } (unique)`
* `{ active: 1, validFrom: 1, validTo: 1 }`

---

## Carts

**Owner:** Cart Service
**Dominio:** Carrito

### Propósito

Persistir el estado del carrito durante la sesión de compra.

### Esquema JSON orientativo

```json
{
  "_id": "ObjectId",
  "cartId": "UUID",
  "items": [
    {
      "sku": "SKU-12345",
      "quantity": 2,
      "unitPrice": 19.99
    }
  ],
  "currency": "EUR",
  "subtotal": 39.98,
  "discounts": 5.00,
  "total": 34.98,
  "status": "ACTIVE",
  "expiresAt": "2026-01-15T11:00:00Z",
  "createdAt": "2026-01-15T10:00:00Z",
  "updatedAt": "2026-01-15T10:30:00Z",
  "version": 5
}
```

### Campos clave

* `cartId`
* `status`
* `expiresAt`

### Índices

* `{ cartId: 1 } (unique)`
* `{ expiresAt: 1 } (TTL)`

### TTL

* El carrito expira automáticamente tras un periodo de inactividad.

---

## Orders

**Owner:** Checkout Service
**Dominio:** Checkout

### Propósito

Almacenar pedidos creados tras el checkout.

### Esquema JSON orientativo

```json
{
  "_id": "ObjectId",
  "orderId": "UUID",
  "cartId": "UUID",
  "amount": 34.98,
  "currency": "EUR",
  "status": "PENDING_PAYMENT",
  "createdAt": "2026-01-15T10:45:00Z",
  "updatedAt": "2026-01-15T10:45:00Z",
  "version": 1
}
```
### Campos clave

* `orderId`
* `status`

### Índices

* `{ orderId: 1 } (unique)`
* `{ status: 1 }`

---

## delivery_options

**Owner:** Delivery Options Service
**Dominio:** Entrega

### Propósito

Persistir opciones y costes de entrega calculados en sesión.

### Esquema JSON orientativo

```json
{
  "_id": "ObjectId",
  "cartId": "UUID",
  "postalCode": "28001",
  "options": [
    {
      "type": "HOME_DELIVERY",
      "cost": 4.99,
      "slaDays": 2
    }
  ],
  "createdAt": "2026-01-15T10:20:00Z",
  "version": 1
}
```

### Campos clave

* `cartId`

### Índices

* `{ cartId: 1 }`

---

# payments

**Owner:** Payment Status Service
**Dominio:** Pagos

## Propósito

Gestionar el estado del pago asociado a un pedido.

## Esquema JSON orientativo

```json
{
  "_id": "ObjectId",
  "paymentId": "UUID",
  "orderId": "UUID",
  "status": "AUTHORIZED",
  "amount": 34.98,
  "currency": "EUR",
  "createdAt": "2026-01-15T10:45:00Z",
  "updatedAt": "2026-01-15T10:50:00Z",
  "version": 2
}
```

### Campos clave

* `paymentId`
* `orderId`
* `status`

### Índices

* `{ paymentId: 1 }`
* `{ orderId: 1 }`

---

# outbox_events

**Owner:** Servicio emisor
**Dominio:** Integración

## Propósito

Soportar el patrón **outbox** para publicación fiable de eventos.

## Esquema JSON orientativo

```json
{
  "_id": "ObjectId",
  "eventId": "UUID",
  "eventType": "checkout.order.created",
  "payload": {},
  "published": false,
  "createdAt": "2026-01-15T10:45:00Z"
}
```
### Campos clave

* `eventId`
* `published`

### Índices

* `{ eventId: 1 }`
* `{ published: 1 }`

---

## stock_validations

**Owner**: cart-service  
**Dominio**: Validaciones de Stock

### Propósito
Registrar las validaciones de stock realizadas durante el proceso de checkout para auditoría y análisis.

### Esquema JSON orientativo
```json
{
  "_id": "ObjectId",
  "sku": "SKU-12345",
  "quantity": 2,
  "available": true,
  "currentStock": 5,
  "validatedAt": "2026-01-26T15:00:00Z"
}
```

### Campos clave

* `sku`
* `validatedAt`

### Índices

* `{ sku: 1, validatedAt: 1 }`

### Consideraciones

* TTL de 7 días para los documentos en esta colección.

---

## price_validations

**Owner:** Cart Service
**Dominio:** Validaciones de Precios

### Propósito

Registrar todas las validaciones de precio realizadas al añadir productos al carrito, incluyendo cambios de precio detectados.

### Esquema JSON orientativo

```json
{
  "_id": "ObjectId",
  "sku": "SKU-12345",
  "oldPrice": 19.99,
  "newPrice": 21.99,
  "priceChanged": true,
  "timestamp": "2026-01-26T15:00:00Z"
}
```

### Campos clave

* `sku`
* `priceChanged`

### Índices

* `{ sku: 1, timestamp: -1 }`

### Consideraciones

* TTL de 30 días para los documentos en esta colección.