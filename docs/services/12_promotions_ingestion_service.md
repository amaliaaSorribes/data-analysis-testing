# Promotions Ingestion Service

## 1. Objetivo del servicio
El **Promotions Ingestion Service** es un microservicio asíncrono responsable de recibir, validar, normalizar y persistir las promociones comerciales definidas en sistemas externos del retailer.

Este servicio actúa como **puerta de entrada** del dominio de promociones dentro del ecosistema de Cart & Checkout, asegurando que las reglas promocionales estén disponibles y actualizadas para su posterior aplicación durante el cálculo de precios y el checkout.

---

## 2. Alcance funcional
Dentro del Sistema de Cart & Checkout, este servicio cubre:

- Ingesta de promociones desde sistemas upstream
- Normalización de reglas promocionales
- Control de versiones y vigencia temporal
- Persistencia en base de datos NoSQL
- Publicación opcional de eventos de confirmación

### Fuera de alcance
- Aplicación de promociones a carritos
- Cálculo de descuentos
- Validación de cupones en tiempo real

---

## 3. Arquitectura y dependencias

### Tipo de servicio
- Microservicio **asíncrono**
- Orientado a eventos
- Stateless

### Dependencias externas
- Sistema central de promociones
- Broker de mensajería (Kafka / RabbitMQ)

### Dependencias internas
- MongoDB
- Promotion Engine Service (consumidor downstream)

---

## 4. Entrada de datos (Eventos)

### Evento consumido
- **Nombre**: `promotions.promo.published`
- **Productor**: Sistema central de promociones
- **Frecuencia**: Event-driven (alta/modificación/baja lógica)

### Payload de entrada (ejemplo)
```json
{
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
}
