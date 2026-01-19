# 01 — Glosario y Convenciones

## 1. Propósito del documento
Este documento define el **lenguaje común**, las **convenciones técnicas** y los **estándares** utilizados en la documentación del sistema Cart & Checkout. Su objetivo es asegurar consistencia entre microservicios, APIs, eventos y modelo de datos, así como facilitar la comprensión y el mantenimiento del sistema.

---

## 2. Glosario funcional

### Carrito (Cart)
Entidad que representa la selección temporal de productos de un usuario durante una sesión de compra. Puede expirar por inactividad.

### Ítem (Cart Item)
Producto individual dentro de un carrito, identificado por `sku` y asociado a una cantidad y precio en sesión.

### Sesión
Contexto temporal de interacción del usuario con el sistema. Un carrito suele estar asociado a una sesión (anónima o autenticada).

### Quote
Resultado del cálculo de precios y promociones para un conjunto de ítems en un momento dado. No implica creación de pedido.

### Promoción
Regla de negocio que modifica el precio final (descuento, bundle, cupón, etc.) bajo ciertas condiciones.

### Pedido (Order)
Entidad persistente creada tras el checkout, previa al pago o pendiente de confirmación de pago.

### Pago (Payment)
Proceso y estado asociado a la transacción económica de un pedido.

### Disponibilidad de entrega
Conjunto de opciones logísticas (método, coste, SLA) válidas para un carrito o pedido.

---

## 3. Convenciones de APIs REST

### 3.1 Versionado
- Todas las APIs se versionan mediante prefijo en la URL.
- Versión actual: `/v1`
- Ejemplo:
```http
POST /v1/carts/{cartId}/items
```

### 3.2 Naming
- Recursos en **plural**
- Paths en **kebab-case**
- Identificadores en path (`{cartId}`, `{orderId}`)

### 3.3 Verbos HTTP
- `GET`: lectura
- `POST`: creación o acción no idempotente
- `PUT`: reemplazo completo
- `PATCH`: actualización parcial
- `DELETE`: eliminación

---

## 4. Convenciones de Request / Response

### 4.1 Formato
- JSON como formato estándar
- UTF-8
- `Content-Type: application/json`

### 4.2 Ejemplo genérico de respuesta exitosa
```json
{
  "data": {},
  "metadata": {
    "requestId": "req-123456",
    "timestamp": "2026-01-15T10:30:00Z"
  }
}
```

---

## 5. Convenciones de errores

### 5.1 Códigos HTTP
- `400` Bad Request → error de validación
- `401` Unauthorized
- `403` Forbidden
- `404` Not Found
- `409` Conflict (estado inconsistente)
- `422` Unprocessable Entity (regla de negocio)
- `500` Internal Server Error
- `503` Service Unavailable

### 5.2 Formato de error
```json
{
  "error": {
    "code": "CART_ITEM_NOT_FOUND",
    "message": "The requested item does not exist in the cart",
    "details": {}
  }
}
```

---

## 6. Convenciones de IDs

- `cartId`, `orderId`, `paymentId`: UUID v4 (string)
- `sku`: string alfanumérico definido por catálogo
- `customerId`: string (cuando aplica)
- `requestId`: generado por gateway o servicio

---

## 7. Convenciones de fechas, moneda y números

- Fechas en ISO 8601 (UTC)
  - Ejemplo: `2026-01-15T10:30:00Z`

- Moneda en formato ISO 4217
  - Ejemplo: `EUR`

- Precios:
  - Decimales
  - Redondeo definido por Pricing Service

---

## 8. Convenciones de MongoDB

### 8.1 Naming

- Colecciones en `snake_case`
- Campos en `camelCase`

### 8.2 Documento base

- `_id` gestionado por MongoDB
- Campos de auditoría comunes:
  - `createdAt`
  - `updatedAt`
  - `version`

### 8.3 Ownership

Cada colección tiene un único microservicio owner, responsable de:

- Esquema
- Escrituras
- Evolución del modelo

---

## 9. Convenciones de eventos y colas

### 9.1 Naming de eventos

**Formato:**

```text
<dominio>.<entidad>.<acción>
```
### 9.2 Payload mínimo
### 9.2 Payload mínimo
Todos los eventos deben incluir:

- `eventId`
- `eventType`
- `occurredAt`
- `payload`
- `sourcesService`

### 9.3 Idempotencia
- Los consumidores deben ser idempotentes
- `eventId` se usa como clave de deduplicación

---

## 10. Convenciones de releases y cambios

- Cambios **breaking** deben documentarse explícitamente en `/releases`
- Cada user story indica:
  - endpoints afectados
  - cambios de esquema
  - eventos nuevos o modificados
- Versiones incrementales: `1.0`, `1.1`, `1.2`, etc.

---

## 11. Convenciones de documentación

- Markdown como formato único
- Encabezados jerárquicos (`#`, `##`, `###`)
- Ejemplos JSON siempre formateados
- Links cruzados entre documentos
- Longitud máxima recomendada: < 1000 líneas por fichero

---

## 12. Lecturas relacionadas

- Overview del sistema: `00_overview_cart_checkout.md`
- Modelo de datos: `02_modelo_datos_mongo.md`
- Eventos y colas: `03_eventos_y_colas.md`