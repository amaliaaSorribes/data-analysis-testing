# Pricing Service

## 1. Objetivo del servicio
El **Pricing Service** es el microservicio responsable de calcular los **precios base, impuestos y totales** de los productos de un carrito o de una solicitud de pricing.

Este servicio actúa como la **fuente de verdad del dominio de precios**, desacoplando el cálculo económico del resto de la lógica de carrito y checkout.

---

## 2. Alcance funcional
Dentro del Sistema de Cart & Checkout, el Pricing Service cubre:

- Cálculo de precios unitarios
- Cálculo de subtotales
- Aplicación de impuestos
- Cálculo de totales por moneda
- Respuesta de pricing orientativo en sesión

### Fuera de alcance
- Aplicación de promociones
- Gestión de catálogos
- Conversión de moneda
- Persistencia de carritos u órdenes

---

## 3. Arquitectura y dependencias

### Tipo de servicio
- Microservicio **síncrono**
- Expuesto vía APIs REST
- Stateless

### Dependencias internas
- **MongoDB**: colección `prices`
- Consumido por:
  - Cart Service
  - Checkout Service

---

## 4. Modelo de datos

### Colección MongoDB
- **Nombre**: `prices`
- **Owner**: Pricing Service

### Esquema del documento (orientativo)
```json
{
  "_id": "SKU-001",
  "sku": "SKU-001",
  "price": 25.00,
  "currency": "EUR",
  "taxRate": 0.10,
  "effectiveFrom": "2026-01-01T00:00:00Z",
  "effectiveTo": null,
  "channel": "WEB",
  "updatedAt": "2026-01-10T08:00:00Z"
}
