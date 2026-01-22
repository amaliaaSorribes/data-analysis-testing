# Estructura acumulada (visión completa del sistema)

`/docs/indice.md`

### Qué contiene

* Resumen del sistema (10–15 líneas)
* Cómo leer la documentación (acumulada vs releases)
* Tabla/lista de ficheros con:
    * 2–3 líneas de summary
    * link al `.md` correspondiente
    * tags (ej: `#cart`, `#checkout`, `#ingestion`, `#mongo`, `#rest`, `#events`)
* “Glosario rápido” (5–10 términos)

### Secciones

* `# Índice`
* `## Visión general`
* `## Documentación acumulada`
* `## Documentación por releases`
* `## Glosario breve`

---

`/docs/00_overview_cart_checkout.md`

### Qué contiene

* Contexto del retailer y objetivos del sistema
* Dominios: catálogo / pricing / promos / cart / checkout / shipping / payment
* Arquitectura textual (microservicios + colas + Mongo)
* Principios: idempotencia en ingestión, consistencia eventual, ownership de datos
* Matriz “microservicio → colecciones Mongo → eventos → APIs”

### Secciones

* `# Overview`
* `## Alcance`
* `## Arquitectura` (alto nivel)
* `## Microservicios` (lista y responsabilidades)
* `## Flujos principales` (happy path)
* `## Consideraciones` (sesión, consistencia, errores)
* `## Mapa de datos` (MongoDB)
* `## Mapa de eventos/colas`

---

`/docs/01_glosario_y_convenciones.md`

### Qué contiene

* Convenciones de endpoints (naming, versionado `/v1`, códigos de error)
* Convenciones de IDs (cartId, orderId, customerId)
* Convenciones de fechas/moneda
* Convenciones de eventos (nombres, payload mínimo)
* Reglas de compatibilidad (breaking/non-breaking)

### Secciones

* `# Glosario y convenciones`
* `## Convenciones REST`
* `## Convenciones Mongo`
* `## Convenciones de eventos`
* `## Estándares de errores`

---

`/docs/02_modelo_datos_mongo.md`

### Qué contiene

* Catálogo de colecciones (una por dominio)
* Para cada colección:
    * propósito
    * esquema JSON orientativo
    * índices
    * campos clave
    * TTL si aplica (carritos expiran)
    * ejemplos de documentos

### Colecciones típicas

* `products`
* `prices`
* `promotions`
* `carts`
* `orders`
* `delivery_options`
* `payments`
* `outbox_events` (si queréis simular outbox)

### Secciones

* `# Modelo de datos MongoDB`
* `## products`
* `## prices`
* `...`
* `## carts`
* `## orders`
* `## Índices y consideraciones`

---

`/docs/03_eventos_y_colas.md`

### Qué contiene

* Lista de topics/colas (Kafka/Rabbit “abstracto”)
* Para cada evento:
    * nombre
    * productor/consumidor
    * motivo (por qué existe)
    * payload ejemplo
    * claves de partición / ordering (si aplica)
    * idempotency key / eventId

### Eventos típicos

* `catalog.product.upserted`
* `pricing.price.updated`
* `promotions.promo.published`
* `cart.cart.updated`
* `checkout.order.created`
* `payment.status.changed`

### Secciones

* `# Eventos y colas`
* `## Eventos de ingesta`
* `## Eventos transaccionales`
* `## Contratos de evento (schema)`
* `## Estrategias de reintento / DLQ (alto nivel)`

---

`/docs/10_catalog_ingestion_service.md`

### Qué contiene

* Microservicio de ingesta de catálogo
* Cola/topic que consume
* Transformaciones y validaciones
* Escritura en `products`
* Estrategia idempotente
* Observabilidad (métricas/logs “conceptuales”)

### Secciones

* `# Catalog Ingestion Service`
* `## Responsabilidad`
* `## Entradas (cola/eventos)`
* `## Proceso (validación, normalización)`
* `## Persistencia (Mongo: products)`
* `## Errores y reintentos`
* `## Ejemplos`
* `## No-objetivos`

---

`/docs/11_pricing_ingestion_service.md`

### Qué contiene

* Ingesta de precios base por canal/tienda/moneda
* Consistencia: último precio válido
* Escritura en `prices`
* Cómo se versionan precios (effectiveFrom/effectiveTo)

### Secciones

* iguales a las del ingestion anterior, adaptadas a pricing

---

`/docs/12_promotions_ingestion_service.md`

### Qué contiene

* Ingesta de promociones (reglas, cupones, bundles)
* Normalización de reglas
* Escritura en `promotions`
* Versionado y activación

### Secciones

* idem

---

`/docs/20_cart_service.md`

### Qué contiene

* El “owner” del carrito y la sesión
* Endpoints REST completos con verbos + E/S + errores
* Reglas de negocio: cantidad, límites, stock soft-check, etc.
* Persistencia en `carts`
* Interacciones: Llama a Pricing/Promos/Delivery para “quote” en sesión (o lo simula)

### Secciones

* `# Cart Service`
* `## Responsabilidad y límites`
* `## Modelo de datos (carts)`
* `## Endpoints`
    * `POST /v1/carts` (crear carrito)
    * `GET /v1/carts/{cartId}`
    * `POST /v1/carts/{cartId}/items` (añadir producto)
    * `PATCH /v1/carts/{cartId}/items/{sku}` (incrementar/decrementar)
    * `DELETE /v1/carts/{cartId}/items/{sku}`
    * `POST /v1/carts/{cartId}/merge` (si queréis)
    * `POST /v1/carts/{cartId}/lock` (si queréis simular “freeze before payment”)
* `## Errores (códigos + ejemplos)`
* `## Consideraciones de sesión / expiración`

> **Nota:** Aquí “viven”: añadir_producto, incrementar_cantidad, etc. (como endpoints/secciones, no como ficheros sueltos).

---

`/docs/21_pricing_service.md`

### Qué contiene

* Cálculo de precio base y total
* Reglas: impuestos, redondeos, moneda, canal
* API para “quote” del carrito o de líneas
* Fuente de verdad: `prices` + input del carrito

### Secciones

* `# Pricing Service`
* `## Responsabilidad`
* `## Dependencias` (Mongo: `prices`, llamadas)
* `## Endpoints`
    * `POST /v1/pricing/quote` (entrada: items, salida: totales)
    * `GET /v1/prices/{sku}` (opcional)
* `## Errores`
* `## Ejemplos request/response`

---

`/docs/22_promotion_engine_service.md`

### Qué contiene

* Aplicación de descuentos/promos
* Tipos de promos
* API para aplicar promos a un carrito (o a un quote)
* Fuente de verdad: `promotions`

### Secciones

* `# Promotion Engine Service`
* `## Responsabilidad`
* `## Endpoints`
    * `POST /v1/promotions/apply`
    * `POST /v1/promotions/validate-coupon`
* `## Modelo de datos (promotions)`
* `## Casos de error`
* `## Ejemplos`

---

`/docs/23_delivery_options_service.md`

### Qué contiene

* Disponibilidad de entrega en sesión (tienda, domicilio, franjas)
* Cálculo de coste de transporte
* API para devolver opciones
* Persistencia opcional en `delivery_options` o embebido en `carts`

### Secciones

* `# Delivery Options Service`
* `## Endpoints`
    * `POST /v1/delivery/options`
    * `POST /v1/delivery/cost`
* `## Reglas (postal code, stock, SLA)`
* `## Ejemplos`

---

`/docs/30_checkout_service.md`

### Qué contiene

* Orquestación “checkout”
* Validaciones finales: precios, promos, delivery
* Creación de pedido “pendiente de pago”
* Persistencia en `orders`
* Estado del pedido (draft/pending_payment/paid/failed)

### Secciones

* `# Checkout Service`
* `## Responsabilidad`
* `## Modelo (orders)`
* `## Endpoints`
    * `POST /v1/checkout/validate`
    * `POST /v1/checkout/orders` (crear pedido)
    * `GET /v1/checkout/orders/{orderId}`
* `## Estados y transiciones`
* `## Errores`

---

`/docs/31_payment_status_service.md`

### Qué contiene

* Gestión del estado del pago (polling/callback)
* APIs para consultar estado
* Recepción de eventos del PSP (simulado)
* Persistencia en `payments` (y link a orderId)

### Secciones

* `# Payment Status Service`
* `## Endpoints`
    * `GET /v1/payments/{paymentId}`
    * `GET /v1/orders/{orderId}/payment-status`
    * `POST /v1/payments/webhook` (simulado)
* `## Modelo (payments)`
* `## Eventos (payment.status.changed)`

---

`/docs/32_tracking_service.md`

### Qué contiene

* Seguimiento del paquete (estado logístico)
* API para tracking
* Fuente de datos (simulada) y persistencia (opcional)
* Estados típicos: shipped/in_transit/delivered/exception

### Secciones

* `# Tracking Service`
* `## Endpoints`
    * `GET /v1/tracking/{trackingId}`
    * `GET /v1/orders/{orderId}/tracking`
* `## Estados`
* `## Ejemplos`