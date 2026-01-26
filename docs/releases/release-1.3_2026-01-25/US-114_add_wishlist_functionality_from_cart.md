# US-114 - Add Wishlist Functionality from Cart

---

## Identificación

- **ID:** US-114  
- **Fecha:** 2025-02-18  
- **Servicio:** cart-service  

---

## User Story

Como usuario quiero mover productos desde mi carrito a una lista de deseos para guardarlos y comprarlos más tarde.

---

## Descripción

Se implementará una funcionalidad que permita a los usuarios mover productos desde el carrito a una lista de deseos (wishlist) mediante un botón "Guardar para después". Los productos movidos a la wishlist se eliminarán automáticamente del carrito. La wishlist será persistente y tendrá un límite máximo de 50 productos. Para usuarios logueados, se asociará a su `userId`, mientras que para usuarios guest se asociará al `cartId` actual con un flag especial. Al loguearse un usuario guest, su wishlist se fusionará con la wishlist asociada a su cuenta.  

---

## Cambios

### Qué se añadió

- Botón "Guardar para después" en la vista del carrito.  
- Lógica para mover productos del carrito a la wishlist y actualizar ambos.  
- Persistencia de la wishlist en una nueva colección de MongoDB llamada `wishlists`.  
- Validaciones para el límite de productos en la wishlist.  
- Lógica para fusionar wishlists de usuarios guest con las de usuarios logueados.  

---

## Impacto en APIs

### Nuevo endpoint

1. **POST /v1/wishlist/items**  
   - Añadir un producto a la wishlist.  
   - Si el producto proviene del carrito, eliminarlo automáticamente del carrito.  
   - Respuesta: carrito actualizado y wishlist actualizada.  

2. **GET /v1/wishlist**  
   - Obtener la wishlist del usuario.  

3. **DELETE /v1/wishlist/items/{sku}**  
   - Eliminar un producto de la wishlist.  

4. **POST /v1/wishlist/move-to-cart**  
   - Mover un producto de la wishlist al carrito.  

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-27/funcional.md)
