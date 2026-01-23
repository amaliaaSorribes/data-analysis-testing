```markdown
# US-112 - Unified Add to Cart Endpoint

---

## Identificación

- **ID:** US-112
- **Fecha:** 2025-03-18  
- **Servicio:** cart-service

---

## User Story

Como un desarrollador backend quiero unificar el comportamiento de añadir productos al carrito en un único endpoint para resolver inconsistencias en precios y promociones y eliminar lógica duplicada.

---

## Descripción

Se requiere la creación de un nuevo endpoint `POST /v2/cart/items` que unifique el comportamiento de añadir productos al carrito tanto para la web como para la app. Este endpoint deberá recibir `productId` y `quantity`, recalcular precios y promociones utilizando el Pricing Service y el Promotion Engine, y devolver el carrito completo. Además, se eliminará el endpoint antiguo de la app (`POST /v2/cart/add`) y se mantendrá compatibilidad temporal con el endpoint antiguo de la web (`POST /v1/cart/items`). No se realizarán cambios en el modelo de datos.

---

## Cambios

### Qué se añadió

- Creación del nuevo endpoint `POST /v2/cart/items`.
- Actualización del Cart Service para incluir la nueva versión del endpoint.
- Eliminación del endpoint antiguo de la app (`POST /v2/cart/add`).
- Compatibilidad temporal para el endpoint antiguo de la web (`POST /v1/cart/items`).

---

## Impacto en APIs

### Nuevo endpoint

- **Endpoint:** `POST /v2/cart/items`
- **Descripción:** Recibe `productId` y `quantity`, recalcula precios y promociones, y devuelve el carrito completo.
- **Dependencias:** 
  - Pricing Service: utilizado para recalcular precios.
  - Promotion Engine: utilizado para aplicar promociones.
```

    ---

    ## Referencias

    - Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2025-03-18/funcional.md)
    