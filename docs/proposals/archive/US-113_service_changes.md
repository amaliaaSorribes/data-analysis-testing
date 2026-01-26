```markdown
# Propuesta de actualización - US-113

## Resumen de la US
La User Story US-113 introduce la funcionalidad de gestionar una lista de favoritos desde el carrito. Los usuarios logueados pueden añadir productos a favoritos, consultar la lista, mover productos entre el carrito y la lista de favoritos, y eliminar productos de favoritos. La lista de favoritos se integra con el Pricing Service para mostrar precios actualizados.

## Análisis de impacto
La implementación de esta US afecta principalmente a la documentación del `cart-service`, ya que se han añadido nuevos endpoints y funcionalidades relacionadas con la gestión de favoritos. También se requiere una mención en el `pricing_service` debido a la integración para obtener precios actualizados. Otros servicios no se ven afectados.

## Cambios propuestos

### 20_cart_service.md

#### Cambio 1: Actualización de la sección "Responsabilidad y límites"
**Sección afectada:** Responsabilidad y límites  
**Tipo de cambio:** Modificar  

**Justificación:**  
La funcionalidad de favoritos amplía las responsabilidades del `cart-service`, ya que ahora también gestiona la lista de favoritos y las operaciones relacionadas con esta.

**Contenido propuesto:**
```
El **Cart Service** es el **owner del carrito y de la sesión de compra**, así como de la gestión de la lista de favoritos del usuario. Gestiona el ciclo de vida del carrito, los ítems que contiene, los cálculos “en sesión” necesarios para mostrar totales al usuario antes del checkout, y las operaciones de favoritos, como añadir, listar, eliminar y mover productos entre el carrito y la lista de favoritos.
```

**Ubicación:**  
Reemplazar el primer párrafo de la sección "Responsabilidad y límites".

---

#### Cambio 2: Adición de nuevos endpoints
**Sección afectada:** Endpoints (nueva sección)  
**Tipo de cambio:** Añadir  

**Justificación:**  
Se han añadido nuevos endpoints al `cart-service` para gestionar la lista de favoritos. Es necesario documentarlos para que los desarrolladores y equipos relacionados puedan utilizarlos correctamente.

**Contenido propuesto:**
```
## Endpoints

### POST `/v1/favorites`
Añadir un producto a la lista de favoritos.

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

### GET `/v1/favorites`
Listar todos los productos en la lista de favoritos del usuario.

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

### DELETE `/v1/favorites/{productId}`
Eliminar un producto de la lista de favoritos.

- **Response**:
  ```json
  {
    "message": "Product removed from favorites successfully"
  }
  ```

### POST `/v1/carts/{cartId}/items/{productId}/move-to-favorites`
Mover un producto del carrito a la lista de favoritos.

- **Response**:
  ```json
  {
    "message": "Product moved to favorites successfully"
  }
  ```
```

**Ubicación:**  
Añadir al final del archivo `20_cart_service.md`.

---

### 21_pricing_service.md

#### Cambio 1: Actualización de la sección "Responsabilidad"
**Sección afectada:** Responsabilidad  
**Tipo de cambio:** Modificar  

**Justificación:**  
La lista de favoritos requiere precios actualizados de los productos, lo que implica una integración directa con el `pricing_service`. Esto debe ser reflejado en su responsabilidad.

**Contenido propuesto:**
```
El **Pricing Service** es responsable del **cálculo de precios base y totales** a partir de los ítems de un carrito, una lista de líneas o una lista de favoritos. Aplica las **reglas de pricing** vigentes teniendo en cuenta impuestos, redondeos, moneda y canal.
```

**Ubicación:**  
Reemplazar el primer párrafo de la sección "Responsabilidad".

---

## Recomendaciones
1. Asegurarse de que los equipos de frontend y backend estén alineados respecto a los contratos de los nuevos endpoints.
2. Verificar que el Pricing Service esté preparado para manejar solicitudes de precios desde la lista de favoritos sin afectar el rendimiento.
3. Actualizar las pruebas automatizadas para cubrir los nuevos endpoints y flujos relacionados con la lista de favoritos.

## Comandos de aplicación
```bash
# Revisar propuesta
cat docs/proposals/US-113_service_changes.md

# Aprobar y aplicar cambios
python agents/doc_updater/apply_proposal.py US-113 --approve

# Rechazar propuesta
python agents/doc_updater/apply_proposal.py US-113 --reject
```
```