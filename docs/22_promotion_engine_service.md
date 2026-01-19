# Promotion Engine Service

## 1. Objetivo del servicio
El **Promotion Engine Service** es el microservicio responsable de **evaluar y aplicar promociones activas** sobre un carrito o un pricing quote, devolviendo los descuentos aplicables y el total resultante.

Este servicio centraliza toda la lógica de negocio relacionada con promociones, desacoplándola del carrito, pricing y checkout.

---

## 2. Alcance funcional
Dentro del Sistema de Cart & Checkout, el Promotion Engine Service cubre:

- Evaluación de promociones activas
- Aplicación de descuentos sobre importes
- Validación de condiciones promocionales
- Cálculo del total con descuento
- Respuesta de descuentos en sesión

### Fuera de alcance
- Ingesta de promociones
- Persistencia de carritos
- Cálculo de impuestos
- Gestión de cupones de pago externos

---

## 3. Arquitectura y dependencias

### Tipo de servicio
- Microservicio **síncrono**
- APIs REST
- Stateless

### Dependencias internas
- **MongoDB**: colección `promotions`
- Consumido por:
  - Cart Service
  - Checkout Service

---

## 4. Modelo de datos

### Colección MongoDB
- **Nombre**: `promotions`
- **Owner**: Promotions Ingestion Service

> Nota: Este servicio solo consume la colección; no la modifica.

### Campos relevantes
- `type`
- `value`
- `conditions`
- `stackable`
- `active`
- `startDate` / `endDate`

---

## 5. Tipos de promociones soportadas

| Tipo        | Descripción |
|------------|-------------|
| PERCENTAGE | Descuento porcentual sobre subtotal |
| FIXED      | Descuento de importe fijo |
| CONDITIONAL| Descuento condicionado a importe mínimo |

---

## 6. Endpoints REST

### Aplicar promociones
**POST** `/v1/promotions/apply`

#### Request
```json
{
  "currency": "EUR",
  "subtotal": 55.00
}
