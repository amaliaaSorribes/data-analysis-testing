# US-111 - Unified Add-to-Cart Endpoint

---

## Identificación

- **ID:** US-111
- **Fecha:** 2025-03-18
- **Servicio:** cart-service

---

## User Story

Como usuario de web y app quiero que el proceso de añadir productos al carrito utilice el mismo endpoint y lógica para asegurar consistencia en precios y promociones.

---

## Descripción

Actualmente, existen dos endpoints distintos para añadir productos al carrito en web y app, lo que genera inconsistencias en precios y promociones. Se propone unificar ambos canales en un solo endpoint (`POST /v2/cart/items`) que reciba `productId` y `quantity`, recalcule precios y promociones, y devuelva el carrito completo. El frontend de web y app deberá consumir este nuevo endpoint. El endpoint antiguo de app se elimina y se mantiene compatibilidad temporal para el endpoint de web.

---

## Cambios

### Qué se añadió

- Creación de un nuevo endpoint unificado `POST /v2/cart/items` para añadir productos al carrito desde web y app.
- Integración obligatoria con Pricing Service para recálculo de precios.
- Integración obligatoria con Promotion Engine para aplicación de promociones.
- Eliminación del endpoint antiguo de app.
- Compatibilidad temporal con el endpoint antiguo de web.

---

## Impacto en APIs

### Nuevo endpoint

- `POST /v2/cart/items`
  - **Request:** `{ "productId": <string>, "quantity": <int> }`
  - **Response:** Carrito completo actualizado (incluyendo precios y promociones recalculados).

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings\meeting-2025-03-18\funcional.md)
