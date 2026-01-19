# Payment Status Service

## 1. Objetivo del servicio
El **Payment Status Service** es el microservicio responsable de **gestionar y exponer el estado del pago** asociado a un pedido creado durante el checkout.

Este servicio actúa como el **puente entre el sistema de pagos externo y el dominio interno de pedidos**, permitiendo consultar y reaccionar ante cambios en el estado del pago.

---

## 2. Alcance funcional
Dentro del Sistema de Cart & Checkout, este servicio cubre:

- Consulta del estado del pago de un pedido
- Recepción de actualizaciones de pago (callback/eventos)
- Persistencia del estado de pago
- Publicación de eventos de cambio de estado

### Fuera de alcance
- Procesamiento del pago
- Integración directa con PSP reales
- Gestión de reembolsos
- Cálculo de importes

---

## 3. Arquitectura y dependencias

### Tipo de servicio
- Microservicio **síncrono**
- APIs REST
- Stateless

### Dependencias internas
- **MongoDB**: colección `payments`
- Checkout Service (origen del pedido)
- Sistemas de pago externos (simulados)

---

## 4. Modelo de datos

### Colección MongoDB
- **Nombre**: `payments`
- **Owner**: Payment Status Service

### Esquema del documento (orientativo)
```json
{
  "_id": "PAY-987654",
  "orderId": "ORDER-456789",
  "status": "PAID",
  "paymentMethod": "CARD",
  "amount": 54.49,
  "currency": "EUR",
  "createdAt": "2026-01-16T10:20:00Z",
  "updatedAt": "2026-01-16T10:21:30Z"
}
