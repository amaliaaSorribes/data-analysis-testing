# US-103 – Aplicar promoción al carrito

---

## Identificación

- **ID:** US-103  
- **Fecha:** 2025-01-29  
- **Servicio:** cart-service  

---

## Descripción

Como cliente, quiero aplicar un código promocional a mi carrito,
para obtener un descuento en el total de mi compra.

---

## Descripción

Permitir aplicar un código promocional al carrito
que modifique el subtotal con el descuento correspondiente.

---

## Cambios

- Endpoint para aplicar promo
- Cálculo de descuento
- Persistencia del código aplicado

---

## Impacto en APIs

```http
POST /api/v1/cart/{cartId}/promotions