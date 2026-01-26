# US-112 - Real-time stock validation during checkout

---

## Identificación

- **ID:** US-112
- **Fecha:** 2026-01-26
- **Servicio:** cart-service

---

## User Story

Como usuario que realiza una compra quiero que el sistema valide en tiempo real la disponibilidad de stock durante el checkout para evitar comprar productos sin stock y así reducir cancelaciones y mejorar mi experiencia.

---

## Descripción

Se requiere implementar una validación de stock en tiempo real durante el proceso de checkout. El frontend enviará la lista de SKUs y cantidades al backend, que consultará el sistema de inventario mediante una API síncrona. Si algún producto no tiene stock suficiente, se notificará al usuario y se bloqueará la compra de ese producto. Si la API de inventario no responde, se permitirá la compra en modo degradado mostrando una advertencia. Todas las validaciones quedarán registradas para auditoría.

---

## Cambios

### Qué se añadió

- Validación de stock en tiempo real durante checkout.
- Nuevo endpoint POST /v1/catalog/validate-stock en el Catalog Service.
- Integración síncrona con la API de inventario (REST).
- Circuit breaker y timeout de 3 segundos para la consulta a inventario.
- Caché de 30 segundos para validaciones (Redis).
- Registro de validaciones en la colección stock_validations con TTL de 7 días.
- Modo degradado en caso de caída de la API de inventario.

---

## Impacto en APIs

### Nuevo endpoint

- **POST /v1/catalog/validate-stock**
  - **Request:**  
    `{ items: [{ sku, quantity }] }`
  - **Response:**  
    `{ items: [{ sku, available: bool, currentStock: number }] }`


---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-26/funcional.md)
