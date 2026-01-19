# Promotion Engine Service

## Responsabilidad
El **Promotion Engine Service** es responsable de la **aplicación de descuentos y promociones** sobre un carrito o un *quote* de precios. Evalúa reglas promocionales activas y determina los descuentos aplicables en función de las condiciones definidas.

Este servicio **no es owner del carrito ni del pricing base**, sino que actúa como **motor de reglas** para promociones.

---

## Endpoints

### POST `/v1/promotions/apply` — Aplicar promociones
Aplica las promociones activas a un carrito o a un *quote* recibido como entrada.

**Request**
```json
{
  "cartId": "UUID",
  "currency": "EUR",
  "items": [
    {
      "sku": "SKU-12345",
      "quantity": 2,
      "unitPrice": 19.99
    }
  ],
  "subtotal": 39.98
}
```

**Response(200)**
```json
{
  "discounts": [
    {
      "promotionId": "PROMO-2026-01",
      "type": "PERCENTAGE",
      "value": 10,
      "amount": 3.99
    }
  ],
  "totalDiscount": 3.99,
  "finalTotal": 35.99
}
```

---

### POST `/v1/promotions/validate-coupon` — Validar cupón

Valida un cupón promocional sin aplicarlo al carrito.

**Request**

```json
{
  "couponCode": "SAVE10",
  "cartTotal": 39.98,
  "currency": "EUR"
}
```

**Response(200)**
```json
{

  "valid": true,
  "promotionId": "PROMO-2026-01",
  "message": "Coupon is valid"

}
```

---

## Modelo de datos (promotions)

### Fuente de verdad

* **Colección MongoDB:** `promotions`
* Gestionada por: **Promotions Ingestion Service**

### Uso

El Promotion Engine Service **consulta** la colección `promotions` para:

* Obtener promociones activas
* Evaluar condiciones
* Determinar compatibilidad y acumulabilidad

No realiza escrituras sobre esta colección.

---

### Tipos de promociones

* **PERCENTAGE:** descuento porcentual sobre el subtotal
* **FIXED_AMOUNT:** descuento fijo
* **BUNDLE:** descuentos por combinación de productos
* **COUPON:** promoción activada por código

Las reglas específicas de cada tipo se definen en el documento de la promoción.

---

## Casos de error

**Errores funcionales**

* `404 PROMOTION_NOT_FOUND`
* `422 PROMOTION_NOT_APPLICABLE`
* `422 INVALID_COUPON`
* `409 PROMOTION_EXPIRED`

**Ejemplo**

```json
{
  "error": {
    "code": "INVALID_COUPON",
    "message": "The provided coupon code is not valid"
  }
}
```

**Errores técnicos**

* `500 INTERNAL_ERROR`
* `503 SERVICE_UNAVAILABLE`

---

# Ejemplos

## Aplicación de promoción porcentual

**Entrada**

```json
{
  "cartId": "UUID",
  "subtotal": 100,
  "currency": "EUR"
}
```

**Salida**
```json
{
  "totalDiscount": 10,
  "finalTotal": 90
}
```
