# US-111 - Unified Add-to-Cart Endpoint

---

## Identificación

- **ID:** US-111
- **Fecha:** 2025-03-18
- **Servicio:** cart-service

---

## User Story

Como desarrollador de frontend quiero consumir un único endpoint para añadir productos al carrito para asegurar la consistencia en precios y promociones entre web y app.

---

## Descripción

Actualmente existen dos endpoints distintos para añadir productos al carrito, lo que genera lógica duplicada y diferencias en el cálculo de precios y aplicación de promociones. Se propone unificar ambos flujos en un solo endpoint (`POST /v2/cart/items`) que reciba `productId` y `quantity`, recalcule precios y promociones, y devuelva el carrito completo. Tanto el frontend web como la app deberán consumir este nuevo endpoint. El endpoint antiguo de la app será eliminado y se mantendrá compatibilidad temporal para el endpoint web. No se modifica el modelo de datos.

---

## Cambios

### Qué se añadió

- Creación de un nuevo endpoint: `POST /v2/cart/items` que recibe `productId` y `quantity`, invoca el servicio de precios y el motor de promociones, y devuelve el carrito completo.
- Eliminación del endpoint antiguo de la app.
- Compatibilidad temporal para el endpoint web.

---

## Impacto en APIs

### Nuevo endpoint

- `POST /v2/cart/items`
  - Request: `{ productId, quantity }`
  - Response: Carrito completo con precios y promociones recalculados.

    ---

    ## Referencias

    - Documento funcional: [`funcional.md`](../../docs/meetings\meeting-2025-03-18\funcional.md)
    