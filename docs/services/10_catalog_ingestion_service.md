# Catalog Ingestion Service

## Responsabilidad
Este microservicio es responsable de la **ingesta de datos de catálogo** provenientes de sistemas externos. Su función principal es **consumir eventos de catálogo**, **validar y normalizar** la información recibida y **persistirla** en la colección MongoDB `products`.

El servicio actúa como **fuente de verdad** del catálogo normalizado dentro del ecosistema Cart & Checkout.

---

## Entradas (cola / eventos)

### Cola / Topic consumido
- **Nombre**: `catalog.events`
- **Tipo**: Topic (mensajería asíncrona, abstracto Kafka/RabbitMQ)

### Eventos consumidos
- `catalog.product.upserted`

### Productor del evento
- Sistema externo de catálogo / PIM (simulado)

---

## Proceso (validación, normalización)

Al recibir un evento de catálogo, el servicio ejecuta el siguiente flujo:

1. **Validación**
   - Presencia de campos obligatorios (`sku`, `name`)
   - Formato correcto de identificadores
   - Validación de tipos básicos (strings, booleanos)

2. **Normalización**
   - Conversión de nombres de campos a formato estándar
   - Normalización de valores categóricos
   - Eliminación de atributos no soportados

3. **Enriquecimiento (opcional)**
   - Añadir metadatos de sistema (timestamps, versión)
   - Marcar producto como activo/inactivo

---

## Persistencia (Mongo: products)

### Colección
- **Nombre**: `products`

### Operación
- **Upsert** por `sku`
- Si el producto existe, se actualiza
- Si no existe, se crea un nuevo documento

### Campos gestionados
- `sku`
- `name`
- `description`
- `category`
- `attributes`
- `active`
- `createdAt`
- `updatedAt`
- `version`

El esquema detallado de la colección se describe en `02_modelo_datos_mongo.md`.

---

## Estrategia idempotente

El servicio garantiza **idempotencia** mediante:

- Uso de `eventId` como clave de deduplicación
- Registro de eventos procesados (lógico o persistente)
- Operaciones **upsert** en MongoDB
- Reprocesamiento seguro ante reintentos

Procesar el mismo evento más de una vez **no genera duplicados ni inconsistencias**.

---

## Errores y reintentos

### Errores funcionales
- Evento inválido (schema incorrecto)
- Campos obligatorios ausentes

Acción:
- El evento se descarta o se envía a DLQ según la política.

### Errores técnicos
- Fallo de conexión a MongoDB
- Timeout en consumo de mensajes

Acción:
- Reintentos automáticos
- Envío a DLQ tras superar el umbral configurado

---

## Observabilidad

### Métricas (conceptuales)
- Número de eventos consumidos
- Número de productos creados / actualizados
- Eventos fallidos
- Tiempo medio de procesamiento

### Logs (conceptuales)
- Recepción de evento
- Resultado de validación
- Operación de persistencia
- Errores y reintentos

La observabilidad se considera **transversal**, sin definir herramientas concretas.

---

## Ejemplos

### Evento de entrada
```json
{
  "eventId": "UUID",
  "eventType": "catalog.product.upserted",
  "occurredAt": "2026-01-10T09:00:00Z",
  "payload": {
    "sku": "SKU-12345",
    "name": "Product name",
    "category": "electronics",
    "active": true
  },
  "sourceService": "external-catalog-system"
}
```
### Documento persistido (products)
```json
{
  "sku": "SKU-12345",
  "name": "Product name",
  "category": "electronics",
  "active": true,
  "version": 1
}
```

---

## No-objetivos

Este microservicio **NO** es responsable de:

* Cálculo de precios
* Aplicación de promociones
* Validación de stock en tiempo real
* Exposición de APIs REST al frontend
* Gestión de sesiones o carritos