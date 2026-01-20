# Delivery Options Service

## Responsabilidad
El **Delivery Options Service** es responsable de calcular la **disponibilidad de entrega en sesión** y el **coste de transporte** para un carrito o conjunto de ítems. Proporciona opciones de entrega como **recogida en tienda**, **entrega a domicilio** y **franjas horarias**, teniendo en cuenta reglas logísticas y de negocio.

Este servicio se utiliza durante la sesión de compra para informar al usuario antes del checkout.

---

## Endpoints

### POST `/v1/delivery/options` — Obtener opciones de entrega
Devuelve las opciones de entrega disponibles para un carrito o dirección.

**Request**
```json
{
  "cartId": "UUID",
  "postalCode": "28001",
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
  "options": [
    {
      "type": "HOME_DELIVERY",
      "slaDays": 2,
      "cost": 4.99
    },
    {
      "type": "STORE_PICKUP",
      "storeId": "STORE-001",
      "slaDays": 1,
      "cost": 0
    }
  ]
}
```

---

### POST `/v1/delivery/cost` — Calcular coste de transporte

Calcula el coste de una opción de entrega seleccionada.

**Request**

```json
{
  "cartId": "UUID",
  "deliveryType": "HOME_DELIVERY",
  "postalCode": "28001"
}
```

**Response (200)**
```json

{
  "deliveryType": "HOME_DELIVERY",
  "cost": 4.99,
  "currency": "EUR"
}

```

---

## Reglas (postal code, stock, SLA)

* La disponibilidad depende del **código postal**
* El *stock* se valida de forma **soft** (no se reserva)
* Las opciones pueden variar por:
    * tipo de entrega
    * volumen del carrito
    * categoría de producto
* El **SLA** (días de entrega) se calcula en base a reglas logísticas
* El coste puede ser:
    * fijo
    * variable según importe del carrito
    * gratuito a partir de un umbral

### Persistencia (opcional)

La información de entrega puede:

* Persistirse temporalmente en la colección `delivery_options`, o
* Embedderse dentro del documento `carts` como parte del estado de sesión

La persistencia es **opcional** y dependiente del flujo de negocio.

---

# Ejemplos

## Ejemplo: entrega a domicilio

**Entrada**

```json
{
  "postalCode": "28001",
  "deliveryType": "HOME_DELIVERY"
}
```

**Salida**

```json
{
  "deliveryType": "HOME_DELIVERY",
  "slaDays": 2,
  "cost": 4.99
}
```
