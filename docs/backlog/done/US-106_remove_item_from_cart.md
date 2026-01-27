# US-106 – Eliminar ítem del carrito

---

## Identificación

- **ID:** US-106  
- **Fecha:** 2025-02-12  
- **Servicio:** cart-service  

---

## User Story

Como cliente, quiero eliminar productos de mi carrito,
para quitar aquellos que ya no deseo comprar.

---

## Descripción

Permitir eliminar un ítem del carrito tanto de forma visual como del total de la compra.

---

## Cambios

- Endpoint para eliminar ítem
- Recalculo de totales tras eliminación

---

## Impacto en APIs

```http
DELETE /api/v1/cart/{cartId}/items/{productId}