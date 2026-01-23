# Cart Service

## Responsabilidad y límites
El **Cart Service** es el **owner del carrito y de la sesión de compra**. Gestiona el ciclo de vida del carrito, los ítems que contiene y los cálculos “en sesión” necesarios para mostrar totales al usuario antes del checkout.

Este servicio es responsable de:
- Crear y mantener carritos activos
- Añadir, modificar y eliminar productos
- Recalcular precios y aplicar promociones al añadir productos al carrito, utilizando el Pricing Service y el Promotion Engine
- Aplicar reglas básicas de negocio en sesión
- Persistir el estado del carrito
- Orquestar (o simular) llamadas a servicios externos relacionados con el carrito

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

Añade un producto al carrito o incrementa su cantidad si ya existe.

**Request**
```json
{
  "sku": "SKU-12345",
  "quantity": 1
}
```

**Reponse (200)**
```json
{
  "cartId": "UUID",
  "status": "ACTIVE",
  "items": [
    {
      "sku": "SKU-12345",
      "quantity": 1
    }
  ]
}
```

---

### POST `/v2/cart/items` — Añadir producto al carrito
**Descripción:**  
Este endpoint permite añadir un producto al carrito unificado, recalculando precios y promociones. Devuelve el carrito completo actualizado.

**Parámetros:**
- **productId** (string, requerido): ID del producto a añadir.
- **quantity** (integer, requerido): Cantidad del producto a añadir.

**Dependencias:**
- **Pricing Service:** Recalcula los precios de los productos en el carrito.
- **Promotion Engine:** Aplica promociones activas al carrito.

**Respuesta:**
- **200 OK:** Carrito actualizado con los productos añadidos, precios y promociones aplicados.
- **400 Bad Request:** Parámetros inválidos.
- **500 Internal Server Error:** Error interno en el procesamiento.

---

### POST `/v2/cart/add` — [Deprecado]
**Nota:** Este endpoint ha sido eliminado y reemplazado por `POST /v2/cart/items`. Se recomienda actualizar las integraciones existentes.

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
