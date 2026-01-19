# Pricing Ingestion Service

## Responsabilidad
Este microservicio es responsable de la **ingesta de precios base** provenientes de sistemas externos. Gestiona precios por **producto, canal, tienda y moneda**, asegurando que el sistema disponga siempre del **último precio válido** según su vigencia temporal.

El servicio normaliza la información recibida y la persiste en la colección MongoDB `prices`, actuando como **fuente de verdad** del pricing base dentro del sistema Cart & Checkout.

---

## Entradas (cola / eventos)

### Cola / Topic consumido
- **Nombre**: `pricing.events`
- **Tipo**: Topic (mensajería asíncrona, abstracto Kafka/RabbitMQ)

### Eventos consumidos
- `pricing.price.updated`

### Productor del evento
- Sistema externo de pricing / ERP (simulado)

---

## Proceso (validación, normalización)

Al recibir un evento de precios, el servicio ejecuta el siguiente flujo:

1. **Validación**
   - Presencia de campos obligatorios (`sku`, `amount`, `currency`)
   - Validación de valores numéricos (precio > 0)
   - Validación de fechas de vigencia

2. **Normalización**
   - Conversión de moneda a formato ISO 4217
   - Normalización de identificadores de canal y tienda
   - Ajuste de formatos de fecha a ISO 8601

3. **Gestión de consistencia**
   - Identificación del precio vigente actual
   - Cierre del precio anterior ajustando `effectiveTo`
   - Preparación del nuevo precio como vigente

---

## Persistencia (Mongo: prices)

### Colección
- **Nombre**: `prices`

### Operación
- Inserción de nuevos documentos de precio
- Actualización del precio vigente anterior cuando aplica

### Campos gestionados
- `sku`
- `channel`
- `storeId`
- `currency`
- `amount`
- `effectiveFrom`
- `effectiveTo`
- `createdAt`
- `updatedAt`
- `version`

El esquema detallado se describe en `02_modelo_datos_mongo.md`.

---

## Versionado de precios (effectiveFrom / effectiveTo)

El versionado de precios se basa en **ventanas de vigencia temporal**:

- Cada documento de precio tiene:
  - `effectiveFrom`: inicio de validez
  - `effectiveTo`: fin de validez
- Solo **un precio** puede estar vigente para una combinación:
  - `sku + channel + storeId + currency`

Cuando llega un nuevo precio:
1. Se localiza el precio vigente actual
2. Se actualiza su `effectiveTo`
3. Se inserta el nuevo precio con `effectiveFrom` actual

Este enfoque garantiza trazabilidad histórica y consistencia.

---

## Estrategia idempotente

El servicio garantiza **idempotencia** mediante:

- Uso de `eventId` como clave de deduplicación
- Validación de eventos ya procesados
- Inserciones controladas basadas en vigencia
- Reprocesamiento seguro sin duplicar precios

Procesar el mismo evento más de una vez **no genera precios duplicados ni solapados**.

---

## Errores y reintentos

### Errores funcionales
- Precio inválido (importe negativo o cero)
- Fechas de vigencia inconsistentes
- Evento mal formado

Acción:
- Rechazo del evento
- Envío a DLQ según la política definida

### Errores técnicos
- Fallos de persistencia en MongoDB
- Timeout en consumo de eventos

Acción:
- Reintentos automáticos
- Envío a DLQ tras superar el umbral de reintentos

---

## Observabilidad

### Métricas (conceptuales)
- Eventos de precios consumidos
- Precios creados
- Precios actualizados
- Eventos rechazados
- Tiempo medio de procesamiento

### Logs (conceptuales)
- Recepción del evento
- Resultado de validaciones
- Actualización de vigencias
- Errores y reintentos

---

## Ejemplos

### Evento de entrada
```json
{
  "eventId": "UUID",
  "eventType": "pricing.price.updated",
  "occurredAt": "2026-01-10T09:05:00Z",
  "payload": {
    "sku": "SKU-12345",
    "channel": "online",
    "storeId": "STORE-001",
    "currency": "EUR",
    "amount": 19.99,
    "effectiveFrom": "2026-01-15T00:00:00Z"
  },
  "sourceService": "external-pricing-system"
}
```
### Documento persistido (prices)
```json
{
  "sku": "SKU-12345",
  "channel": "online",
  "storeId": "STORE-001",
  "currency": "EUR",
  "amount": 19.99,
  "effectiveFrom": "2026-01-15T00:00:00Z",
  "effectiveTo": "2026-12-31T23:59:59Z",
  "version": 1
}
```

---

## No-objetivos

Este microservicio **NO** es responsable de:

* Cálculo de totales de carrito
* Aplicación de promociones
* Exposición de APIs REST
* Gestión de pedidos o pagos