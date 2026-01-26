```markdown
# US-113 - Add Favorites List to Cart

---

## Identificación

- **ID:** US-113
- **Fecha:** 2025-02-18  
- **Servicio:** cart-service

---

## User Story

Como usuario logueado quiero guardar productos como favoritos desde el carrito para poder gestionarlos y comprarlos más adelante.

---

## Descripción

Se implementará una funcionalidad que permitirá a los usuarios logueados guardar productos como favoritos directamente desde el carrito. Los usuarios podrán añadir productos a la lista de favoritos, consultar la lista en una nueva página o sección, mover productos entre el carrito y la lista de favoritos, y eliminar productos de la lista de favoritos. La lista de favoritos mostrará el precio actualizado de los productos, integrándose con el Pricing Service. No habrá límite en la cantidad de productos que se puedan añadir a la lista de favoritos.

---

## Cambios

### Qué se añadió

- Nueva entidad `favorites` en el backend para gestionar la lista de favoritos.
- Nuevos endpoints para añadir, listar, eliminar y mover productos a favoritos.
- Integración con el Pricing Service para obtener precios actualizados.
- Nueva página o sección en el frontend para mostrar y gestionar la lista de favoritos.
- Botón "Guardar para más tarde" o "Mover a favoritos" en cada producto del carrito.

---

## Impacto en APIs

### Nuevo endpoint

1. **POST /v1/favorites**: Añadir un producto a favoritos.
   - **Request**:
     ```json
     {
       "productId": "string"
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Product added to favorites successfully"
     }
     ```

2. **GET /v1/favorites**: Listar todos los favoritos del usuario.
   - **Response**:
     ```json
     [
       {
         "productId": "string",
         "productName": "string",
         "price": "number",
         "fechaDeAñadido": "string"
       }
     ]
     ```

3. **DELETE /v1/favorites/{productId}**: Eliminar un producto de favoritos.
   - **Response**:
     ```json
     {
       "message": "Product removed from favorites successfully"
     }
     ```

4. **POST /v1/carts/{cartId}/items/{productId}/move-to-favorites**: Mover un producto del carrito a favoritos.
   - **Response**:
     ```json
     {
       "message": "Product moved to favorites successfully"
     }
     ```
```

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-26/funcional.md)
