# Checkout Service

## 1. Objetivo del servicio
El **Checkout Service** es el microservicio responsable de **orquestar el proceso de checkout** y **generar el pedido previo al pago** a partir de un carrito válido.

Este servicio representa el **punto de no retorno funcional**: a partir de aquí el carrito deja de ser editable y se convierte en una intención de compra formal.

---

## 2. Alcance funcional
Dentro del Sistema de Cart & Checkout, el Checkout Service cubre:

- Validación final del carrito
- Revalidación de precios y promociones
- Selección definitiva de entrega
- Creación del pedido
- Gestión del estado previo al pago

### Fuera de alcance
- Procesamiento del pago
- Gestión del estado logístico
- Tracking de pedidos
- Comunicación con el cliente

---

## 3. Arquitectura y dependencias

### Tipo de servicio
- Microservicio **síncrono**
- APIs REST
- Stateless

### Dependencias internas
- **Cart Service** (bloqueo y lectura del carrito)
- **Pricing Service** (pricing definitivo)
- **Promotion Engine Service** (descuentos definitivos)
- **Delivery Options Service** (coste final de entrega)
- **MongoDB**: colección `orders`

---

## 4. Modelo de datos

### Colección MongoDB
- **Nombre**: `orders`
- **Owner**: Checkout Service

### Esquema del documento (orientativo)
```json
{
  "_id": "ORDER-456789",
  "cartId": "CART-123456",
  "customerId": "CUST-789",
  "status": "PENDING_PAYMENT",
  "currency": "EUR",
  "items": [
    {
      "sku": "SKU-001",
      "quantity": 2,
      "unitPrice": 25,
      "lineTotal": 50
    }
  ],
  "pricing": {
    "subtotal": 50,
    "discounts": 5.5,
    "taxes": 5,
    "deliveryCost": 4.99,
    "total": 54.49
  },
  "delivery": {
    "type": "HOME",
    "postalCode": "28001",
    "estimatedDays": 2
  },
  "createdAt": "2026-01-16T10:15:00Z",
  "updatedAt": "2026-01-16T10:15:00Z"
}
