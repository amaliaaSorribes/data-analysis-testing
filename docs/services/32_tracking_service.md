# Tracking Service

## 1. Objetivo del servicio
El **Tracking Service** es el microservicio responsable de **gestionar y exponer el estado logístico de un pedido** tras la confirmación del pago.

Este servicio actúa como el **puente entre el Checkout Service y la información logística del pedido**, permitiendo consultar y seguir la evolución del envío.

---

## 2. Alcance funcional
Dentro del Sistema de Cart & Checkout, este servicio cubre:

- Consulta del estado logístico de un pedido
- Recepción de eventos de pago confirmado
- Creación y actualización de tracking del pedido
- Publicación de estados logísticos actualizados

### Fuera de alcance
- Gestión logística real
- Creación de envíos físicos
- Optimización de rutas
- Notificación directa al cliente

---

## 3. Arquitectura y dependencias

### Tipo de servicio
- Microservicio **síncrono**
- APIs REST
- Stateless

### Dependencias internas
- **MongoDB**: colección `trackings`
- Payment Status Service (evento de pago confirmado)
- Proveedores logísticos simulados

---

## 4. Modelo de datos

### Colección MongoDB
- **Nombre**: `trackings`
- **Owner**: Tracking Service

### Esquema del documento (orientativo)
```json
{
  "_id": "TRACK-112233",
  "orderId": "ORDER-456789",
  "status": "IN_TRANSIT",
  "history": [
    {
      "status": "SHIPPED",
      "timestamp": "2026-01-17T08:00:00Z"
    },
    {
      "status": "IN_TRANSIT",
      "timestamp": "2026-01-17T12:00:00Z"
    }
  ],
  "updatedAt": "2026-01-17T12:00:00Z"
}
```

