# US-112 - Real-time price validation on add-to-cart

---

## Identificación

- **ID:** US-112
- **Fecha:** 2026-01-26
- **Servicio:** cart-service

---

## User Story

Como usuario quiero que el sistema valide el precio actual de un producto al añadirlo al carrito para asegurarme de que el precio cobrado sea el correcto y estar informado si hay cambios.

---

## Descripción

Se requiere que, al intentar añadir un producto al carrito, el cart-service valide el precio actual del SKU consultando el Pricing Service antes de completar la operación. Si el precio ha cambiado respecto al mostrado en el frontend, el usuario será notificado y podrá decidir si continuar o cancelar la acción. Todas las diferencias de precio serán registradas para análisis posterior. Si el servicio de precios no responde en 3 segundos, se permitirá la operación mostrando un warning genérico.

---

## Cambios

### Qué se añadió

- Integración del cart-service con el nuevo endpoint `POST /v1/pricing/validate` del Pricing Service para validar precios en tiempo real antes de añadir productos al carrito.
- Implementación de lógica para devolver un warning al frontend si el precio ha cambiado, incluyendo los campos `priceChanged`, `oldPrice` y `newPrice`.
- Registro de todas las validaciones de precio en la colección `price_validations` con TTL de 30 días.
- Implementación de cache de precios validados por 10 segundos (Redis).
- Manejo de contingencia para permitir la operación si el Pricing Service no responde en 3 segundos, mostrando un warning genérico.

---

## Impacto en APIs

### Nuevo endpoint

- **POST /v1/pricing/validate**  
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

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-26/funcional.md)
