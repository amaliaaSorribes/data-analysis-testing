# Documento funcional – Validación de precios en add-to-cart (2026-01-26)

## Descripción General

Se implementa una validación de precios en tiempo real al añadir productos al carrito para evitar inconsistencias entre el precio mostrado en el catálogo y el precio cobrado en el checkout. El objetivo es informar al usuario si el precio ha cambiado antes de completar la acción, mejorando la confianza y reduciendo el abandono.

- **HU:**  
- **Figma:**  

---

## Lógica Funcional

Cuando un usuario añade un producto al carrito, el sistema debe validar el precio actual del SKU consultando el servicio de precios antes de completar la operación. Si el precio ha cambiado respecto al mostrado en el frontend, se notificará al usuario, quien podrá decidir si continuar o cancelar la acción. Todas las diferencias de precio serán registradas para análisis posterior.

---

## Lógica Frontend

- Al hacer click en "añadir al carrito", el frontend enviará el precio mostrado junto con el SKU al backend.
- Si el backend detecta que el precio ha cambiado, devolverá un flag `priceChanged: true`, junto con el `oldPrice` y el `newPrice`.
- El frontend mostrará un modal informando al usuario del cambio de precio y preguntando si desea continuar.
- Si el usuario acepta, se enviará una confirmación para añadir el producto con el nuevo precio.
- Si el usuario rechaza, se cancelará la operación.
- Si el servicio de validación de precios no responde, se permitirá añadir el producto mostrando un warning genérico.

---

## Lógica Backend

- Se añade un nuevo endpoint en el Pricing Service: `POST /v1/pricing/validate`.
  - Request: `{ items: [{ sku, quantity }] }`
  - Response: `{ items: [{ sku, currentPrice, currency }] }`
- El Cart Service, antes de añadir un item, llamará a este endpoint para validar el precio actual.
- Si el precio difiere del enviado por el frontend, el Cart Service devolverá un warning con los campos:
  - `priceChanged: boolean`
  - `oldPrice: number`
  - `newPrice: number`
- Se implementa un cache de precios validados de 10 segundos (Redis).
- Si el Pricing Service no responde en 3 segundos, se permite la operación con un warning genérico.
- Se registra cada validación de precio en una nueva colección `price_validations` con los siguientes campos:
  - `timestamp`
  - `sku`
  - `frontendPrice`
  - `actualPrice`
  - `action: added / rejected`
  - `userId` (opcional)
- Los registros tendrán un TTL de 30 días.

---

## Nuevos servicios

- **Endpoint:** `POST /v1/pricing/validate`
  - **Request:**  
    ```json
    {
      "items": [
        { "sku": "string", "quantity": number }
      ]
    }
    ```
  - **Response:**  
    ```json
    {
      "items": [
        { "sku": "string", "currentPrice": number, "currency": "string" }
      ]
    }
    ```

---

## Partes Afectadas

---

### Analítica

- Registro de todas las diferencias de precio en la colección `price_validations` para análisis y detección de problemas.

---

### Contingencias

- Si el servicio de validación de precios no responde, se permite añadir el producto al carrito mostrando un warning genérico al usuario.

---