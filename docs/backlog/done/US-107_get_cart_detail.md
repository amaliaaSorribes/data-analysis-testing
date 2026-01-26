# US-107 – Obtener detalle del carrito

---

## Identificación

- **ID:** US-107  
- **Fecha:** 2025-02-12  
- **Servicio:** cart-service  

---

## User Story

Como cliente, quiero ver el detalle actualizado de mi carrito,
para revisar los productos, precios y descuentos antes de pagar.

---

## Descripción

Permitir consultar el estado actual del carrito,
incluyendo ítems, precios, descuentos y estado.

---

## Cambios

- Endpoint de lectura del carrito
- Normalización de la respuesta de totales

---

## Impacto en APIs

```http
GET /api/v1/cart/{cartId}