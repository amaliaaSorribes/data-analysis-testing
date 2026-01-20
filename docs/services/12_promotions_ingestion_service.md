# Promotions Ingestion Service

## Responsabilidad
El **Promotions Ingestion Service** es un microservicio asíncrono responsable de la **ingesta de promociones comerciales** (reglas, cupones y bundles) provenientes de sistemas externos del retailer.

Su función principal es **validar, normalizar, versionar y activar** promociones, persistiendo la información en la colección MongoDB `promotions`. El servicio actúa como **fuente de verdad** del dominio de promociones dentro del ecosistema Cart & Checkout.

---

## Entradas (cola / eventos)

### Cola / Topic consumido
- **Nombre**: `promotions.events`
- **Tipo**: Topic (mensajería asíncrona, abstracto Kafka / RabbitMQ)

### Eventos consumidos
- `promotions.promo.published`

### Productor del evento
- Sistema central de promociones (simulado)

---

## Proceso (validación, normalización)

Al recibir un evento de promociones, el servicio ejecuta el siguiente flujo:

### 1. Validación
- Presencia de campos obligatorios (`promoId`, `type`, `value`)
- Validación de fechas de vigencia (`startDate`, `endDate`)
- Validación del tipo de promoción (percentage, fixed amount, bundle, coupon)
- Coherencia de condiciones promocionales

### 2. Normalización
- Normalización del identificador de promoción (`promotionId`)
- Conversión de reglas a un formato estándar interno
- Normalización de condiciones (categorías, SKUs, importes mínimos)
- Traducción de flags funcionales (ej. `stackable`)

### 3. Preparación para activación
- Cálculo del estado `active` en función de la vigencia temporal
- Preparación del versionado lógico de la promoción

---

## Persistencia (Mongo: promotions)

### Colección
- **Nombre**: `promotions`

### Operación
- Inserción de nuevas promociones
- Actualización de promociones existentes por `promotionId`
- Gestión de versiones y estado activo/inactivo

### Campos gestionados
- `promotionId`
- `type`
- `value`
- `conditions`
- `couponCode`
- `active`
- `validFrom`
- `validTo`
- `createdAt`
- `updatedAt`
- `version`

El esquema detallado se describe en `02_modelo_datos_mongo.md`.

---

## Versionado y activación

El versionado de promociones sigue estos principios:

- Cada promoción se identifica por `promotionId`
- Las modificaciones incrementan el campo `version`
- Las promociones tienen una ventana de vigencia:
  - `validFrom`
  - `validTo`
- Una promoción se considera **activa** si:
  - `active = true`
  - la fecha actual está dentro de su ventana de vigencia

El sistema permite la coexistencia de múltiples versiones históricas de una promoción, pero **solo una versión activa** por `promotionId` en un momento dado.

---

## Estrategia idempotente

El servicio garantiza **idempotencia** mediante:

- Uso de `eventId` como clave de deduplicación
- Detección de eventos ya procesados
- Operaciones de inserción/actualización seguras
- Reprocesamiento sin duplicar promociones ni versiones

Procesar el mismo evento más de una vez **no genera inconsistencias** en el estado de las promociones.

---

## Errores y reintentos

### Errores funcionales
- Promoción inválida o incompleta
- Fechas de vigencia inconsistentes
- Reglas promocionales no soportadas

Acción:
- Rechazo del evento
- Envío a DLQ según la política definida

### Errores técnicos
- Fallos de persistencia en MongoDB
- Timeout en el consumo de eventos

Acción:
- Reintentos automáticos
- Envío a DLQ tras superar el umbral configurado

---

## Observabilidad

### Métricas (conceptuales)
- Eventos de promociones consumidos
- Promociones creadas
- Promociones actualizadas
- Promociones activas/inactivas
- Eventos fallidos

### Logs (conceptuales)
- Recepción del evento
- Resultado de validación
- Normalización aplicada
- Persistencia y versionado
- Errores y reintentos

---

## Ejemplos

### Evento de entrada
```json
{
  "eventId": "UUID",
  "eventType": "promotions.promo.published",
  "occurredAt": "2026-01-10T09:10:00Z",
  "payload": {
    "promoId": "PROMO-2026-001",
    "name": "Rebajas invierno",
    "type": "PERCENTAGE",
    "value": 10,
    "conditions": {
      "minAmount": 50,
      "applicableCategories": ["HOME", "ELECTRONICS"]
    },
    "startDate": "2026-01-15",
    "endDate": "2026-02-15",
    "stackable": false
  },
  "sourceService": "central-promotions-system"
}
```
### Documento persistido (products)
```json
{
  "promotionId": "PROMO-2026-001",
  "type": "PERCENTAGE",
  "value": 10,
  "conditions": {
    "minAmount": 50,
    "applicableCategories": ["HOME", "ELECTRONICS"]
  },
  "active": true,
  "validFrom": "2026-01-15T00:00:00Z",
  "validTo": "2026-02-15T23:59:59Z",
  "version": 1
}

```

---

## No-objetivos

Este microservicio **NO** es responsable de:

* Aplicar promociones a carritos
* Calcular descuentos
* Validar cupones en tiempo real
* Exponer APIs REST
* Gestionar pedidos o pagos