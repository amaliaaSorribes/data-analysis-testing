```markdown
# Propuesta de actualización - US-114

## Resumen de la US
La User Story US-114 introduce la funcionalidad de mover productos desde el carrito a una lista de deseos (wishlist). Esto incluye la creación de una nueva colección en MongoDB (`wishlists`), nuevos endpoints para gestionar la wishlist, y lógica para fusionar wishlists de usuarios guest con las de usuarios logueados.

## Análisis de impacto
La documentación del `cart-service` necesita ser actualizada para reflejar los nuevos endpoints, responsabilidades y modelo de datos relacionados con la funcionalidad de wishlist. No se identifican impactos en otros servicios documentados.

## Cambios propuestos

### 20_cart_service.md

#### Cambio 1: Actualización de responsabilidades del servicio
**Sección afectada:** Responsabilidad y límites  
**Tipo de cambio:** Modificar  

**Justificación:**  
La funcionalidad de wishlist ahora forma parte de las responsabilidades del `cart-service`. Es necesario actualizar esta sección para incluir la gestión de la wishlist.

**Contenido propuesto:**
```
El **Cart Service** es el **owner del carrito y de la sesión de compra**, así como de la gestión de la lista de deseos (wishlist) del usuario. Gestiona el ciclo de vida del carrito, los ítems que contiene, los cálculos "en sesión" necesarios para mostrar totales al usuario antes del checkout, y las operaciones de favoritos y wishlist, como añadir, listar, eliminar y mover productos entre el carrito y la lista de deseos.

Este servicio es responsable de:
- Crear y mantener el carrito de compras.
- Gestionar la lista de deseos (wishlist), incluyendo persistencia, validaciones y operaciones entre carrito y wishlist.
```

**Ubicación:**  
Reemplazar el párrafo actual en la sección "Responsabilidad y límites", líneas 5-10.

---

#### Cambio 2: Inclusión de nuevos endpoints
**Sección afectada:** Endpoints  
**Tipo de cambio:** Añadir  

**Justificación:**  
Se han implementado nuevos endpoints relacionados con la gestión de la wishlist. Estos deben ser documentados para reflejar las capacidades del servicio.

**Contenido propuesto:**
```
### POST `/v1/wishlist/items`
Añade un producto a la wishlist. Si el producto proviene del carrito, se elimina automáticamente del carrito.

- **Body:**
  ```json
  {
    "sku": "string",
    "quantity": "integer"
  }
  ```
- **Respuesta:**
  ```json
  {
    "cart": { ... },
    "wishlist": { ... }
  }
  ```

### GET `/v1/wishlist`
Obtiene la wishlist del usuario actual.

- **Respuesta:**
  ```json
  {
    "wishlist": [
      {
        "sku": "string",
        "quantity": "integer",
        "addedAt": "timestamp"
      }
    ]
  }
  ```

### DELETE `/v1/wishlist/items/{sku}`
Elimina un producto específico de la wishlist.

- **Respuesta:**
  ```json
  {
    "wishlist": { ... }
  }
  ```

### POST `/v1/wishlist/move-to-cart`
Mueve un producto de la wishlist al carrito.

- **Body:**
  ```json
  {
    "sku": "string",
    "quantity": "integer"
  }
  ```
- **Respuesta:**
  ```json
  {
    "cart": { ... },
    "wishlist": { ... }
  }
  ```
```

**Ubicación:**  
Añadir al final de la sección "Endpoints", después de los endpoints existentes.

---

#### Cambio 3: Inclusión de la colección `wishlists` en el modelo de datos
**Sección afectada:** Modelo de datos  
**Tipo de cambio:** Añadir  

**Justificación:**  
La nueva colección `wishlists` debe ser documentada para describir su propósito, estructura y relación con el servicio.

**Contenido propuesto:**
```
### Colección
- **Nombre**: `wishlists`

### Descripción
La colección `wishlists` almacena las listas de deseos de los usuarios. Cada documento representa la wishlist de un usuario o sesión de carrito (para usuarios guest).

### Campos principales
- **_id**: Identificador único de la wishlist.
- **userId**: (Opcional) Identificador del usuario logueado. Nulo para usuarios guest.
- **cartId**: (Opcional) Identificador del carrito asociado (para usuarios guest).
- **items**: Array de productos en la wishlist.
  - **sku**: Identificador del producto.
  - **quantity**: Cantidad del producto.
  - **addedAt**: Timestamp de cuándo se añadió el producto.
- **isGuest**: Flag booleano que indica si la wishlist pertenece a un usuario guest.

### Índices
- Índice en `userId` para búsquedas rápidas de wishlists de usuarios logueados.
- Índice en `cartId` para búsquedas rápidas de wishlists de usuarios guest.
```

**Ubicación:**  
Añadir al final de la sección "Modelo de datos".

---

## Recomendaciones
1. Validar que los cambios en la documentación reflejan completamente la implementación técnica de la funcionalidad de wishlist.
2. Asegurar que los ejemplos JSON de los endpoints sean consistentes con las respuestas reales del servicio.
3. Revisar si otros servicios relacionados (como `checkout-service`) requieren referencias cruzadas a la funcionalidad de wishlist.

## Comandos de aplicación
```bash
# Revisar propuesta
cat docs/proposals/US-114_service_changes.md

# Aprobar y aplicar cambios
python agents/doc_updater/apply_proposal.py US-114 --approve

# Rechazar propuesta
python agents/doc_updater/apply_proposal.py US-114 --reject
```
```