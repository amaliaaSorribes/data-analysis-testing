# Checkout Service

## Responsabilidad
El **Checkout Service** es responsable de la **orquestación del proceso de checkout**. Coordina las **validaciones finales** del carrito antes de la creación del pedido, asegurando que los **precios**, **promociones** y **opciones de entrega** son coherentes y vigentes.

Este servicio es el **punto de transición** entre el carrito en sesión y el pedido persistente.

---

## Modelo (orders)

### Colección
- **Nombre**: `orders`

### Descripción
La colección `orders` almacena los pedidos creados durante el checkout, incluyendo su estado y los datos necesarios para el proceso de pago.

### Campos principales
- `orderId`
- `cartId`
- `items`
- `amount`
- `currency`
- `status`
- `createdAt`
- `updatedAt`

El esquema detallado se describe en `02_modelo_datos_mongo.md`.

---

## Endpoints

### POST `/v1/checkout/validate` — Validar checkout
Realiza las validaciones finales antes de crear el pedido.

**Validaciones**
- Precios vigentes
- Promociones aplicables
- Opciones de entrega válidas
- Estado del carrito

**Response (200)**
```json
{
  "valid": true
}
```

---

### POST `/v1/checkout/orders` — Crear pedido

Crea un pedido en estado **PENDING_PAYMENT**.

**Request**

```json
{
  "cartId": "UUID"
}
```

**Response(201)**

```json
{
  "orderId": "UUID",
  "status": "PENDING_PAYMENT"
}
```

---

### GET `/v1/checkout/orders/{orderId}` — Obtener pedido

Devuelve la información del pedido.

**Response (200)**

```json
{
  "orderId": "UUID",
  "status": "PENDING_PAYMENT",
  "amount": 48.38,
  "currency": "EUR"
}
```

---

## Estados y transiciones

Los pedidos pueden encontrarse en los siguientes estados:

* `DRAFT` → pedido creado internamente, no visible
* `PENDING_PAYMENT` → pendiente de pago
* `PAID` → pago confirmado
* `FAILED` → pago fallido

### Transiciones permitidas

* `DRAFT` → `PENDING_PAYMENT`
* `PENDING_PAYMENT` → `PAID`
* `PENDING_PAYMENT` → `FAILED`

---

## Errores

**Errores funcionales**

* `404 CART_NOT_FOUND`
* `409 CART_INVALID_STATE`
* `422 VALIDATION_FAILED`

**Ejemplo**

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Final validation failed for checkout"
  }
}
```

**Errores funcionales**

* `500 INTERNAL_ERROR`
* `503 SERVICE_UNAVAILABLE`
