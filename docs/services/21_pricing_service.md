# Pricing Service

## Responsabilidad
El **Pricing Service** es responsable del **cálculo de precios base y totales** a partir de los ítems de un carrito o de una lista de líneas. Aplica las **reglas de pricing** vigentes teniendo en cuenta impuestos, redondeos, moneda y canal.

Este servicio proporciona un **quote** temporal que se utiliza durante la sesión de compra y en la validación previa al checkout.

---

## Dependencias (Mongo: prices, llamadas)

### Persistencia
- **MongoDB**
  - Colección: `prices`
  - Contiene los precios base vigentes por producto, canal y moneda

### Dependencias externas
- Cart Service (input de ítems)
- Promotion Engine Service (opcional, si el pricing incluye descuentos)
- Delivery Options Service (no requerido para el cálculo base)

---

## Endpoints

### POST `/v1/pricing/quote` — Calcular quote
Calcula el precio total de un conjunto de ítems aplicando reglas de pricing.

**Request**
```json
{
  "currency": "EUR",
  "channel": "online",
  "items": [
    {
      "sku": "SKU-12345",
      "quantity": 2
    }
  ]
}
```
**Response (200)**
```json
{
  "subtotal": 39.98,
  "taxes": 8.40,
  "total": 48.38,
  "currency": "EUR"
}
```

---

### GET `/v1/prices/{sku}` — Obtener precio base (opcional)

Devuelve el precio base vigente de un producto para un canal y moneda.

**Response (200)**
```json
{
  "sku": "SKU-12345",
  "amount": 19.99,
  "currency": "EUR",
  "channel": "online"
}
```

---

### Reglas de pricing

* El precio base se obtiene desde la colección `prices`
* Solo se considera el **precio vigente**
* El cálculo es sensible a:
    * Canal
    * Moneda
* Los impuestos se aplican según reglas configuradas
* Los importes se redondean según la moneda
* El servicio no persiste resultados de cálculo

---

# Errores

**Errores funcionales**

* `404 PRICE_NOT_FOUND`
* `422 INVALID_CURRENCY`
* `422 INVALID_ITEMS`

**Ejemplo**

```json
{
  "error": {
    "code": "PRICE_NOT_FOUND",
    "message": "No valid price found for SKU SKU-12345"
  }
}
```
**Errores técnicos**

* `500 INTERNAL_ERROR`
* `503 SERVICE_UNAVAILABLE`

---

# Ejemplos request / response

## Quote con múltiples ítems

**Request**

```json
{
  "currency": "EUR",
  "channel": "online",
  "items": [
    { "sku": "SKU-11111", "quantity": 1 },
    { "sku": "SKU-22222", "quantity": 3 }
  ]
}
```
**Response**
```json
{
  "subtotal": 89.97,
  "taxes": 18.89,
  "total": 108.86,
  "currency": "EUR"
}
```

