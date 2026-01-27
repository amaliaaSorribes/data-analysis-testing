# US-105 – Actualizar cantidad de ítems del carrito

---

## Identificación

- **ID:** US-105  
- **Fecha:** 2025-02-12  
- **Servicio:** cart-service  

---

## User Story

Como cliente, quiero modificar la cantidad de productos en mi carrito,
para ajustar mi pedido según mis necesidades.

---

## Descripción

Permitir actualizar la cantidad de un ítem existente en el carrito, sumando o restando, 
recalculando los totales de forma automática.

No permitir restar un artículo cuya cantidad es 1.

---

## Cambios

- Endpoint para actualizar cantidad
- Validación de cantidades mayores a cero
- Recalculo de subtotal y descuentos

---

## Impacto en APIs

```http
PUT /api/v1/cart/{cartId}/items/{productId}
