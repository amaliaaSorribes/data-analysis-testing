```markdown
# Documento Funcional - Implementación de Lista de Favoritos en el Carrito (2025-02-18)

## Descripción General

Se implementará una nueva funcionalidad que permitirá a los usuarios logueados guardar productos como favoritos directamente desde el carrito. Esto responde a una necesidad detectada en los usuarios que añaden productos al carrito pero no finalizan la compra de inmediato. La funcionalidad incluirá la posibilidad de mover productos entre el carrito y la lista de favoritos, así como consultar y gestionar los productos guardados en favoritos.

- **HU:** {completar enlace}  
- **Figma:** {completar enlace}

---

## Lógica Funcional

- Se creará una nueva entidad separada del carrito para gestionar los favoritos.
- Los usuarios logueados podrán:
  - Añadir productos a la lista de favoritos desde el carrito.
  - Consultar la lista de favoritos en una nueva página o sección.
  - Mover productos entre el carrito y la lista de favoritos.
  - Eliminar productos de la lista de favoritos.
- La lista de favoritos mostrará el precio actualizado de los productos, con integración al Pricing Service.
- No habrá límite en la cantidad de productos que se pueden añadir a la lista de favoritos.
- En esta fase, no se implementará la sincronización de favoritos entre dispositivos.

---

## Lógica Frontend

- En el carrito, se añadirá un botón "Guardar para más tarde" o "Mover a favoritos" en cada producto.
- Se desarrollará una nueva página o sección para mostrar la lista de favoritos del usuario.
- La lista de favoritos deberá mostrar:
  - Nombre del producto.
  - Precio actualizado (consultado a través del Pricing Service).
  - Fecha en que el producto fue añadido a favoritos.
- Se integrará con los nuevos endpoints proporcionados por el backend para realizar las acciones necesarias (añadir, listar, eliminar, mover productos).

---

## Lógica Backend

- Se extenderá el Cart Service para incluir la gestión de favoritos.
- Se creará una nueva colección en MongoDB llamada `favorites` que almacenará:
  - `userId`: Identificador del usuario.
  - `productId`: Identificador del producto.
  - `fechaDeAñadido`: Fecha en que el producto fue añadido a favoritos.
  - Campo opcional para notas del usuario.
- Se integrará con el Pricing Service para obtener el precio actualizado de los productos al consultar la lista de favoritos.
- Los endpoints a implementar serán:
  - **POST /v1/favorites**: Añadir un producto a favoritos.
  - **GET /v1/favorites**: Listar todos los favoritos del usuario.
  - **DELETE /v1/favorites/{productId}**: Eliminar un producto de favoritos.
  - **POST /v1/carts/{cartId}/items/{productId}/move-to-favorites**: Mover un producto del carrito a favoritos.

---

## Nuevos servicios

- **POST /v1/favorites**
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

- **GET /v1/favorites**
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

- **DELETE /v1/favorites/{productId}**
  - **Response**:
    ```json
    {
      "message": "Product removed from favorites successfully"
    }
    ```

- **POST /v1/carts/{cartId}/items/{productId}/move-to-favorites**
  - **Response**:
    ```json
    {
      "message": "Product moved to favorites successfully"
    }
    ```

---

## Partes Afectadas

### Site afectados

No especificado.

---

### Dependencias con terceros

- Integración con el Pricing Service para obtener precios actualizados.

---

### Analítica

No especificado.

---

### Contingencias

No especificado.

---

### Tipo de Usuario

Aplica únicamente a usuarios logueados.

---

### Método de Envio

No especificado.

---

### Determinar tipo de mercancia

No especificado.

---

### Determinar ventanas de flujo afectadas

No especificado.
```