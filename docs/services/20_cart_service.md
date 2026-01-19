# Cart Service

## 1. Objetivo del servicio
El **Cart Service** es el microservicio owner del **carrito de compra y de la sesión de compra del cliente**. Gestiona el ciclo de vida del carrito desde su creación hasta que se bloquea para iniciar el proceso de checkout.

Este servicio centraliza la lógica de:
- Gestión de productos en el carrito
- Cantidades y estado del carrito
- Persistencia de la sesión de compra
- Coordinación con servicios de pricing, promociones y entrega

---

## 2. Alcance funcional
Dentro del Sistema de Cart & Checkout, el Cart Service cubre:

- Creación del carrito
- Añadir, actualizar y eliminar productos
- Gestión de cantidades
- Recuperación del estado del carrito
- Expiración de carritos inactivos
- Bloqueo del carrito previo al checkout

### Fuera de alcance
- Cálculo definitivo de precios
- Aplicación final de promociones
- Creación del pedido
- Procesamiento de pagos

---

## 3. Arquitectura y dependencias

### Tipo de servicio
- Microservicio **síncrono**
- Orientado a APIs REST
- Stateless

### Dependencias internas
- **MongoDB**: colección `carts`
- **Pricing Service** (consulta de precios)
- **Promotion Engine Service** (descuentos orientativos)
- **Delivery Options Service** (costes y disponibilidad)

---

## 4. Modelo de datos

### Colección MongoDB
- **Nombre**: `carts`
- **Owner**: Cart Service

### Esquema del documento (orientativo)
```json
{
  "_id": "CART-123456",
  "customerId": "CUST-789",
  "status": "ACTIVE",
  "currency": "EUR",
  "items": [
    {
      "sku": "SKU-001",
      "name": "Producto ejemplo",
      "quantity": 2,
      "unitPrice": 25,
      "totalPrice": 50
    }
  ],
  "pricing": {
    "subtotal": 50,
    "discounts": 0,
    "taxes": 5,
    "total": 55
  },
  "delivery": {
    "type": "HOME",
    "cost": 4.99
  },
  "createdAt": "2026-01-16T09:00:00Z",
  "updatedAt": "2026-01-16T09:10:00Z",
  "expiresAt": "2026-01-16T11:00:00Z"
}
