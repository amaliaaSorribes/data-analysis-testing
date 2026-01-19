# US-102 – Añadir ítem al carrito

---

## Identificación

- **ID:** US-102  
- **Fecha:** 2025-01-29  
- **Servicio:** cart-service  

---

## User Story

Como cliente, quiero añadir productos a mi carrito,
para ir preparando mi compra de forma progresiva.

---

## Descripción

Se requiere permitir añadir productos a un carrito existente,
actualizando cantidades y totales de forma consistente.

---

## Cambios

- Nuevo endpoint para añadir ítems
- Recalculo de subtotal del carrito
- Validación de estado del carrito (solo OPEN)

---

## Impacto en APIs

```http
POST /api/v1/cart/{cartId}/items
