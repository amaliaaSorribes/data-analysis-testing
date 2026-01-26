# Documento Funcional - Wishlist desde el Carrito (2025-02-18)

## Descripción General

Se implementará una funcionalidad que permita a los usuarios mover productos desde el carrito a una lista de deseos (wishlist) sin necesidad de eliminarlos del carrito. Esto tiene como objetivo reducir el abandono del carrito y mejorar la experiencia del usuario al permitirle guardar productos para más tarde.

- **HU:** {completar enlace}  
- **Figma:** {completar enlace}

---

## Lógica Funcional

1. Desde la vista del carrito, los usuarios podrán mover productos a una wishlist mediante un botón "Guardar para después".
2. Los productos movidos a la wishlist se eliminarán automáticamente del carrito.
3. La wishlist será persistente:
   - Para usuarios logueados, se asociará a su `userId`.
   - Para usuarios guest, se asociará al `cartId` actual con un flag especial.
   - Al loguearse un usuario guest, su wishlist se fusionará con la wishlist asociada a su cuenta.
4. La wishlist tendrá un límite máximo de 50 productos. Si se intenta añadir más, se mostrará un mensaje al usuario.
5. Se creará una nueva colección en MongoDB llamada `wishlists` con los siguientes campos:
   - `userId`
   - `items` (array de productos)
   - `timestamps`

---

## Lógica Frontend

1. Añadir un botón "Guardar para después" en cada producto del carrito.
2. Al mover un producto a la wishlist:
   - El carrito debe actualizarse para reflejar la eliminación del producto.
   - La wishlist debe actualizarse para incluir el nuevo producto.
3. El endpoint `POST /v1/wishlist/items` deberá devolver tanto el carrito actualizado como la wishlist actualizada para refrescar la UI.

---

## Lógica Backend

1. Extender el Cart Service para gestionar la funcionalidad de wishlist.
2. Crear una nueva colección en MongoDB llamada `wishlists` con los campos mencionados anteriormente.
3. Implementar la lógica para fusionar wishlists de usuarios guest con las de usuarios logueados al momento del login.
4. Implementar validaciones para:
   - Verificar que no se exceda el límite de 50 productos en la wishlist.
   - Eliminar automáticamente el producto del carrito al moverlo a la wishlist.

---

## Nuevos servicios

Se implementarán los siguientes endpoints REST:

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

## Partes Afectadas

### Site afectados

No especificado.

---

### Dependencias con terceros

No aplica.

---

### Analítica

No especificado.

---

### Contingencias

No especificado.

---

### Tipo de Usuario

Aplica a usuarios anónimos (guest) y logueados.

---

### Método de Envio

No especificado.

---

### Determinar tipo de mercancia

No especificado.

---

### Determinar ventanas de flujo afectadas

Afecta a la vista del carrito.