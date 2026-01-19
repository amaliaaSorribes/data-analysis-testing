# US-104 – Proceder al checkout

---

## Identificación

- **ID:** US-104  
- **Fecha:** 2025-01-29  
- **Servicio:** cart-service  

---

## User Story

Como cliente, quiero finalizar mi carrito y proceder al checkout,
para completar el proceso de compra.

---

## Descripción

Finalizar el carrito y bloquear modificaciones futuras,
dejándolo listo para el flujo de pago.

---

## Cambios

- Endpoint de checkout
- Cambio de estado del carrito
- Emisión de evento de checkout

---

## Impacto en APIs

```http
POST /api/v1/cart/{cartId}/checkout