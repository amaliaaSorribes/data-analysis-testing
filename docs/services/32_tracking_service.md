# Tracking Service

## Responsabilidad
El **Tracking Service** es responsable del **seguimiento del paquete** durante el proceso logístico posterior al checkout. Proporciona información del **estado logístico** de un pedido o envío, permitiendo al usuario consultar el progreso de la entrega.

La fuente de datos es **simulada**, y la persistencia es **opcional**.

---

## Endpoints

### GET `/v1/tracking/{trackingId}` — Obtener tracking por ID
Devuelve el estado logístico asociado a un identificador de tracking.

**Response (200)**
```json
{
  "trackingId": "TRK-123456",
  "orderId": "UUID",
  "status": "IN_TRANSIT",
  "lastUpdate": "2026-01-18T14:30:00Z"
}
```

---

### GET `/v1/orders/{orderId}/tracking` — Obtener tracking por pedido

Devuelve la información de tracking asociada a un pedido.

**Response (200)**

```json
{
  "orderId": "UUID",
  "trackingId": "TRK-123456",
  "status": "DELIVERED"
}
```

---

## Estados

Los estados logísticos típicos son:

* `SHIPPED` — Pedido enviado
* `IN_TRANSIT` — En tránsito
* `DELIVERED` — Entregado
* `EXCEPTION` — Incidencia logística

### Fuente de datos y persistencia

* La información de tracking proviene de una **fuente simulada** (sistema logístico externo).
* La persistencia es **opcional**:
    * Puede almacenarse en una colección dedicada, o
    * Consultarse en tiempo real a la fuente externa simulada.
* Cuando se persiste, el vínculo con `orderId` es obligatorio.

---

## Ejemplos

### Ejemplo: estado en tránsito

**Entrada**

```bash
GET /v1/tracking/TRK-123456
```

**Salida**
```json
{
  "trackingId": "TRK-123456",
  "status": "IN_TRANSIT"
}

```
