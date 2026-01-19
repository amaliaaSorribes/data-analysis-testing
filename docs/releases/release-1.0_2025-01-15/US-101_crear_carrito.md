# US-101 – Crear carrito

---

## Identificación

- **ID:** US-101  
- **Fecha:** 2025-01-15  
- **Servicio:** cart-service  

---

## User Story

Como cliente, quiero visualizar un carrito de compras,
para poder añadir productos y gestionarlos antes de finalizar la compra.

---

## Descripción

Actualmente el sistema no cuenta con una entidad de carrito persistente.
Se requiere crear un carrito vacío para un usuario o sesión, que luego pueda ser
utilizado para añadir productos y proceder al checkout.

---

## Cambios

### Qué se añadió

- Endpoint para crear carrito
- Persistencia del carrito en MongoDB
- Evento de dominio al crear el carrito

---

## Impacto en APIs

### Nuevo endpoint

```http
POST /api/v1/cart
