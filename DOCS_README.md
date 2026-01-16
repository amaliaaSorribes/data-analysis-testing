# 00_overview_cart_checkout.md

## Qué contiene
- Contexto del retailer y objetivos del sistema
- Dominios: catálogo / pricing / promos / cart / checkout / shipping / payment
- Arquitectura textual (microservicios + colas + Mongo)
- Principios: idempotencia en ingestión, consistencia eventual, ownership de datos
- Matriz “microservicio → colecciones Mongo → eventos → APIs”

## Secciones
# Overview
## Alcance
## Arquitectura (alto nivel)
## Microservicios (lista y responsabilidades)
## Flujos principales (happy path)
## Consideraciones (sesión, consistencia, errores)
## Mapa de datos (MongoDB)
## Mapa de eventos/colas

---

# 01_glosario_y_convenciones.md

## Qué contiene
- Convenciones de endpoints (naming, versionado /v1, códigos de error)
- Convenciones de IDs (cartId, orderId, customerId)
- Convenciones de fechas/moneda
- Convenciones de eventos (nombres, payload mínimo)
- Reglas de compatibilidad (breaking/non-breaking)

## Secciones
# Glosario y convenciones
## Convenciones REST
## Convenciones Mongo
## Convenciones de eventos
## Estándares de errores

---

# 02_modelo_datos_mongo.md

## Qué contiene
- Catálogo de colecciones (una por dominio)
- Para cada colección:
  - propósito
  - esquema JSON orientativo
  - índices
  - campos clave
  - TTL si aplica (carritos expiran)
  - ejemplos de documentos
- Colecciones típicas:
  - products
  - prices
  - promotions
  - carts
  - orders
  - delivery_options
  - payments
  - outbox_events (simulado)

## Secciones
# Modelo de datos MongoDB
## products
## prices
## promotions
## carts
## orders
## delivery_options
## payments
## outbox_events
## Índices y consideraciones

---

# 03_eventos_y_colas.md

## Qué contiene
- Lista de topics/colas (Kafka/Rabbit “abstracto”)
- Para cada evento:
  - nombre
  - productor/consumidor
  - motivo (por qué existe)
  - payload ejemplo
  - claves de partición / ordering (si aplica)
  - idempotency key / eventId
- Eventos típicos:
  - catalog.product.upserted
  - pricing.price.updated
  - promotions.promo.published
  - cart.cart.updated
  - checkout.order.created
  - payment.status.changed

## Secciones
# Eventos y colas
## Eventos de ingesta
## Eventos transaccionales
## Contratos de evento (schema)
## Estrategias de reintento / DLQ (alto nivel)

---

# 10_catalog_ingestion_service.md

## Qué contiene
- Microservicio de ingesta de catálogo
- Cola/topic que consume
- Transformaciones y validaciones
- Escritura en products
- Estrategia idempotente
- Observabilidad (métricas/logs “conceptuales”)

## Secciones
# Catalog Ingestion Service
## Responsabilidad
## Entradas (cola/eventos)
## Proceso (validación, normalización)
## Persistencia (Mongo: products)
## Errores y reintentos
## Ejemplos
## No-objetivos

---

# 11_pricing_ingestion_service.md

## Qué contiene
- Ingesta de precios base por canal/tienda/moneda
- Consistencia: último precio válido
- Escritura en prices
- Cómo se versionan precios (effectiveFrom/effectiveTo)

## Secciones
- Idem a Catalog Ingestion Service adaptado a pricing

---

# 12_promotions_ingestion_service.md

## Qué contiene
- Ingesta de promociones (reglas, cupones, bundles)
- Normalización de reglas
- Escritura en promotions
- Versionado y activación

## Secciones
- Idem a Catalog Ingestion Service adaptado a promociones

---

# 20_cart_service.md

## Qué contiene
- Owner del carrito y la sesión
- Endpoints REST completos con verbos + E/S + errores
- Reglas de negocio: cantidad, límites, stock soft-check
- Persistencia en carts
- Interacciones: Pricing/Promos/Delivery para quote en sesión

## Secciones
# Cart Service
## Responsabilidad y límites
## Modelo de datos (carts)
## Endpoints
- POST /v1/carts
- GET /v1/carts/{cartId}
- POST /v1/carts/{cartId}/items
- PATCH /v1/carts/{cartId}/items/{sku}
- DELETE /v1/carts/{cartId}/items/{sku}
- POST /v1/carts/{cartId}/merge
- POST /v1/carts/{cartId}/lock
## Errores
## Consideraciones de sesión / expiración

---

# 21_pricing_service.md

## Qué contiene
- Cálculo de precio base y total
- Reglas: impuestos, redondeos, moneda, canal
- API para “quote” del carrito o líneas
- Fuente de verdad: prices + input del carrito

## Secciones
# Pricing Service
## Responsabilidad
## Dependencias (Mongo: prices)
## Endpoints
- POST /v1/pricing/quote
- GET /v1/prices/{sku} (opcional)
## Errores
## Ejemplos request/response

---

# 22_promotion_engine_service.md

## Qué contiene
- Aplicación de descuentos/promos
- Tipos de promos
- API para aplicar promos a un carrito o quote
- Fuente de verdad: promotions

## Secciones
# Promotion Engine Service
## Responsabilidad
## Endpoints
- POST /v1/promotions/apply
- POST /v1/promotions/validate-coupon
## Modelo de datos (promotions)
## Casos de error
## Ejemplos

---

# 23_delivery_options_service.md

## Qué contiene
- Disponibilidad de entrega en sesión
- Cálculo de coste de transporte
- API para devolver opciones
- Persistencia opcional en delivery_options o embebido en carts

## Secciones
# Delivery Options Service
## Endpoints
- POST /v1/delivery/options
- POST /v1/delivery/cost
## Reglas (postal code, stock, SLA)
## Ejemplos

---

# 30_checkout_service.md

## Qué contiene
- Orquestación “checkout”
- Validaciones finales: precios, promos, delivery
- Creación de pedido “pendiente de pago”
- Persistencia en orders
- Estado del pedido: draft / pending_payment / paid / failed

## Secciones
# Checkout Service
## Responsabilidad
## Modelo (orders)
## Endpoints
- POST /v1/checkout/validate
- POST /v1/checkout/orders
- GET /v1/checkout/orders/{orderId}
## Estados y transiciones
## Errores

---

# 31_payment_status_service.md

## Qué contiene
- Gestión del estado del pago
- APIs para consultar estado
- Recepción de eventos del PSP (simulado)
- Persistencia en payments (link a orderId)

## Secciones
# Payment Status Service
## Endpoints
- GET /v1/payments/{paymentId}
- GET /v1/orders/{orderId}/payment-status
- POST /v1/payments/webhook
## Modelo (payments)
## Eventos (payment.status.changed)

---

# 32_tracking_service.md

## Qué contiene
- Seguimiento del paquete (estado logístico)
- API para tracking
- Fuente de datos (simulada) y persistencia opcional
- Estados típicos: shipped / in_transit / delivered / exception

## Secciones
# Tracking Service
## Endpoints
- GET /v1/tracking/{trackingId}
- GET /v1/orders/{orderId}/tracking
## Estados
## Ejemplos
