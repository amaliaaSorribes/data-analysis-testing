# Cart Service

## Responsabilidad y límites
El **Cart Service** es el **owner del carrito y de la sesión de compra**. Gestiona el ciclo de vida del carrito, los ítems que contiene y los cálculos “en sesión” necesarios para mostrar totales al usuario antes del checkout. Ahora también valida el precio actual de los productos al añadirlos al carrito, consultando el Pricing Service. Además, integra la validación de direcciones de envío durante el proceso de checkout mediante un servicio externo. Con el rediseño de la interfaz, el servicio también soporta la visualización de precios originales y con descuento, actualiza el subtotal en tiempo real, gestiona la opción de 'guardar para después', y proporciona sugerencias de productos relacionados. Con la implementación de la US-117, el servicio ahora incluye validación estricta de cantidades, debouncing para evitar requests simultáneos, y recalculo automático del total del carrito tras cada actualización.

Este servicio es responsable de:
- Crear y mantener carritos activos
- Añadir, modificar y eliminar productos
- Aplicar reglas básicas de negocio en sesión
- Persistir el estado del carrito
- Orquestar (o simular) llamadas a servicios de pricing, promociones y entrega para obtener un *quote* en sesión

### Fuera de alcance
- Aplicación definitiva de promociones
- Cálculo final de impuestos
- Creación de pedidos
- Gestión del pago

---

## Modelo de datos (carts)

### Colección
- **Nombre**: `carts`

### Descripción
La colección `carts` almacena el estado del carrito durante la sesión de compra, incluyendo ítems, totales y metadatos de expiración.

### Campos principales
- `cartId`
- `items`
- `currency`
- `subtotal`
- `discounts`
- `total`
- `status`
- `expiresAt`
- `originalPrice`
- `savedForLater`
- `relatedProductSuggestions`

El esquema detallado se describe en `02_modelo_datos_mongo.md`.

---

## Endpoints

### POST `/v1/carts` — Crear carrito
Crea un nuevo carrito vacío asociado a una sesión.

**Response (201)**
```json
{
  "cartId": "UUID",
  "status": "ACTIVE"
}
```

---

### GET `/v1/carts/{cartId}` — Obtener carrito
Devuelve el estado actual del carrito.

**Response (201)**
```json
{
  "cartId": "UUID",
  "items": [],
  "total": 0,
  "currency": "EUR"
}
```

----

### POST `/v1/carts/{cartId}/items` — Añadir producto

Añade un producto al carrito o incrementa su cantidad si ya existe. Antes de completar la operación, valida el precio actual del producto con el Pricing Service.

**Request**
```json
{
  "sku": "SKU-12345",
  "quantity": 1
}
```

**Response (200)**
```json
{
  "cartId": "UUID",
  "status": "ACTIVE",
  "items": [
    {
      "sku": "SKU-12345",
      "quantity": 1,
      "priceChanged": false,
      "oldPrice": null,
      "newPrice": null
    }
  ]
}
```

Si el precio ha cambiado, el campo `priceChanged` será `true` y se incluirán los campos `oldPrice` y `newPrice`.

---

### PATCH `/v1/carts/{cartId}/items/{sku}` — Incrementar / decrementar cantidad

Modifica la cantidad de un producto existente en el carrito.

**Request**
```json
{
  "quantity": 2
}
```

**Reponse (200)**
```json
{
  "cartId": "UUID",
  "items": [
    {
      "sku": "SKU-12345",
      "quantity": 2
    }
  ]
}

```

---

### DELETE `/v1/carts/{cartId}/items/{sku}` — Eliminar producto

Elimina un producto del carrito.

**Response (201)**
```json
{}
```

---

### POST `/v1/carts/{cartId}/merge` — Merge de carritos (opcional)

Fusiona el carrito actual con otro carrito (por ejemplo, al autenticar un usuario).

**Request**
```json
{
  "sourceCartId": "UUID"
}
```

**Reponse (200)**
```json
{
  "cartId": "UUID",
  "merged": true
}
```

---

### POST `/v1/carts/{cartId}/lock` — Bloquear carrito (opcional)

Bloquea el carrito antes de iniciar el proceso de pago (freeze before payment).

**Response (200)**
```json
{
  "cartId": "UUID",
  "status": "LOCKED"
}
```

---

### PUT `/v1/carts/{cartId}/items/{productId}` — Actualizar cantidad de producto

Permite actualizar la cantidad de un ítem existente en el carrito. La cantidad debe ser mayor a cero. El subtotal y los descuentos se recalculan automáticamente.

**Request**
```json
{
  "quantity": 2
}
```

**Response (200)**
```json
{
  "cartId": "UUID",
  "status": "ACTIVE",
  "items": [
    {
      "sku": "SKU-12345",
      "quantity": 2,
      "subtotal": 40.00,
      "discounts": 5.00,
      "total": 35.00
    }
  ],
  "currency": "EUR"
}
```

---

### POST `/v1/addresses/validate` — Validar dirección
Valida y normaliza direcciones de envío durante el checkout.

**Request**
```json
{
  "street": "string",
  "number": "string",
  "city": "string",
  "postalCode": "string",
  "province": "string"
}
```

**Response**
```json
{
  "valid": true,
  "suggestions": [],
  "normalized": {}
}
```

---

### PATCH `/v1/carts/{cartId}/items/{itemId}` — Actualizar cantidad de un ítem
Actualiza la cantidad de un ítem en el carrito con validación de límites y recalculo del total del carrito.

**Request**
```json
{
  "quantity": "number"
}
```

**Response (200)**
```json
{
  "itemId": "UUID",
  "newQuantity": "number",
  "subtotal": "number",
  "cartTotal": "number"
}
```

**Error (422)**
```json
{
  "error": "string",
  "allowedLimits": "string"
}
```

---

### Reglas de negocio

* La cantidad mínima por ítem es 1
* La cantidad máxima por ítem está limitada (configurable)
* No se permite añadir productos inactivos
* *Soft stock check*: no se garantiza stock, solo validación lógica
* El carrito bloqueado (`LOCKED`) no admite modificaciones

---

### Interacciones con otros servicios

Para mostrar totales “en sesión”, el Cart Service:

* Llama o simula llamadas a:
    * **Pricing Service** (precio base)
    * **Promotion Engine Service** (descuentos)
    * **Delivery Options Service** (coste de envío)
* Combina los resultados para generar un *quote* temporal

Estas interacciones no generan persistencia externa.

---

## Errores

**Errores funcionales**

* `404 CART_NOT_FOUND`
* `404 ITEM_NOT_FOUND`
* `409 CART_LOCKED`
* `422 INVALID_QUANTITY`

**Ejemplo**

```json
{
  "error": {
    "code": "CART_LOCKED",
    "message": "The cart is locked and cannot be modified"
  }
}
```

**Errores técnico**

* `500 INTERNAL_ERROR`
* `503 SERVICE_UNAVAILABLE`

---

## Consideraciones de sesión / expiración

* Cada carrito tiene un `expiresAt`
* La expiración se renueva con actividad
* Carritos expirados pasan a estado `EXPIRED`
* Se elimina automáticamente mediante TTL en MongoDB
* Un carrito expirado no puede reactivarse
