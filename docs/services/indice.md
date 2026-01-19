# Índice — Cart & Checkout System (Retailer)

Este repositorio contiene documentación sintética en Markdown que simula la definición funcional y de diseño técnico ligero de un sistema **Cart & Checkout** basado en **microservicios** para un retailer. La documentación está pensada para validar flujos de **ingesta**, **APIs REST**, **modelo de datos en MongoDB** y **eventos/colas**, así como para probar pipelines de **RAG** (chunking, embeddings, recuperación y grounding).

## Cómo leer esta documentación

- **Vista acumulada (`/docs`)**: describe el sistema completo por secciones (overview, glosario, datos, eventos y microservicios).
- **Vista incremental (`/releases`)**: describe la evolución del sistema por sprints/releases, organizada por user stories y cambios sobre los documentos acumulados.

> Nota: Cada fichero está diseñado para no superar las ~1000 líneas.

---

## Documentación acumulada (`/docs`)

### 00 — Vista general del sistema
**`00_overview_cart_checkout.md`**  
Resumen del dominio (retail Cart & Checkout), alcance y arquitectura a alto nivel: microservicios, flujos principales (ingesta y transaccional), límites de responsabilidad y mapa general de datos/eventos.  
Tags: `#overview` `#architecture` `#cart` `#checkout` `#microservices`  
➡️ Ver: [00_overview_cart_checkout.md](00_overview_cart_checkout.md)

### 01 — Glosario y convenciones
**`01_glosario_y_convenciones.md`**  
Glosario de términos (cart, quote, order, promotion, availability, etc.) y convenciones de la documentación: versionado de API, naming, IDs, formato de fechas/moneda, estructura de errores, y contrato de eventos.  
Tags: `#glossary` `#api` `#conventions` `#errors` `#versioning`  
➡️ Ver: [01_glosario_y_convenciones.md](01_glosario_y_convenciones.md)

### 02 — Modelo de datos (MongoDB)
**`02_modelo_datos_mongo.md`**  
Catálogo de colecciones MongoDB (por dominio) con propósito, esquemas orientativos, campos clave e índices principales. Incluye ejemplos de documentos.  
Tags: `#mongo` `#data-model` `#collections` `#schema`  
➡️ Ver: [02_modelo_datos_mongo.md](02_modelo_datos_mongo.md)

### 03 — Eventos y colas
**`03_eventos_y_colas.md`**  
Listado de topics/colas y contratos de eventos: productores/consumidores, payload mínimo y consideraciones de idempotencia y reintentos. Incluye eventos de ingesta y transaccionales.  
Tags: `#events` `#queues` `#kafka` `#rabbitmq` `#integration`  
➡️ Ver: [03_eventos_y_colas.md](03_eventos_y_colas.md)

---

## Microservicios de ingesta (async → MongoDB)

### 10 — Catalog Ingestion Service
**`10_catalog_ingestion_service.md`**  
Microservicio de ingesta de catálogo: consume eventos de catálogo, normaliza/valida, persiste en MongoDB (`products`) y publica eventos derivados cuando aplica.  
Tags: `#ingestion` `#catalog` `#mongo` `#events`  
➡️ Ver: [10_catalog_ingestion_service.md](10_catalog_ingestion_service.md)

### 11 — Pricing Ingestion Service
**`11_pricing_ingestion_service.md`**  
Microservicio de ingesta de precios: consume actualizaciones de precios, gestiona vigencias (`effectiveFrom/effectiveTo`) y persiste en MongoDB (`prices`).  
Tags: `#ingestion` `#pricing` `#mongo` `#events`  
➡️ Ver: [11_pricing_ingestion_service.md](11_pricing_ingestion_service.md)

### 12 — Promotions Ingestion Service
**`12_promotions_ingestion_service.md`**  
Microservicio de ingesta de promociones: reglas, cupones y bundles; persistencia en MongoDB (`promotions`) y versionado/activación.  
Tags: `#ingestion` `#promotions` `#mongo` `#events`  
➡️ Ver: [12_promotions_ingestion_service.md](12_promotions_ingestion_service.md)

---

## Microservicios transaccionales (web → APIs REST)

### 20 — Cart Service
**`20_cart_service.md`**  
Gestión del carrito y sesión: creación/lectura/actualización, ítems, cantidades, totales “en sesión”, bloqueo previo a pago. Endpoints REST + errores + modelo `carts`.  
Tags: `#cart` `#api` `#session` `#mongo`  
➡️ Ver: [20_cart_service.md](20_cart_service.md)

### 21 — Pricing Service
**`21_pricing_service.md`**  
Cálculo de pricing/quote: totales, impuestos, redondeos, moneda/canal. Endpoints para cotización usando `prices` + input de carrito.  
Tags: `#pricing` `#quote` `#api`  
➡️ Ver: [21_pricing_service.md](21_pricing_service.md)

### 22 — Promotion Engine Service
**`22_promotion_engine_service.md`**  
Aplicación de promociones y validación de cupones. Endpoints y reglas principales usando `promotions`.  
Tags: `#promotions` `#discounts` `#api`  
➡️ Ver: [22_promotion_engine_service.md](22_promotion_engine_service.md)

### 23 — Delivery Options Service
**`23_delivery_options_service.md`**  
Disponibilidad y coste de transporte en sesión: opciones de entrega por postal code/tienda/SLA. Endpoints y estados.  
Tags: `#delivery` `#shipping` `#availability` `#api`  
➡️ Ver: [23_delivery_options_service.md](23_delivery_options_service.md)

### 30 — Checkout Service
**`30_checkout_service.md`**  
Orquestación de checkout: validación final, creación de pedido pendiente de pago, persistencia en `orders` y estados del pedido.  
Tags: `#checkout` `#orders` `#api` `#mongo`  
➡️ Ver: [30_checkout_service.md](30_checkout_service.md)

### 31 — Payment Status Service
**`31_payment_status_service.md`**  
Estado de pago: consulta, webhook simulado del PSP y eventos de cambio de estado. Persistencia en `payments`.  
Tags: `#payments` `#status` `#api` `#events`  
➡️ Ver: [31_payment_status_service.md](31_payment_status_service.md)

### 32 — Tracking Service
**`32_tracking_service.md`**  
Seguimiento de paquete: estados logísticos y endpoints de tracking por `trackingId` u `orderId`.  
Tags: `#tracking` `#logistics` `#api`  
➡️ Ver: [32_tracking_service.md](32_tracking_service.md)

---

## Documentación incremental (`/releases`)

La carpeta `/releases` contiene la evolución por sprint (releases). Cada release incluye un `indice.md` y varios documentos por user story. Cada user story referencia qué documentos de `/docs` se han creado o modificado.

➡️ Ver: [../releases/indice_releases.md](../releases/indice_releases.md)

---

## Contactos y ownership (sintético)

- Ownership funcional: Equipo Cart & Checkout
- Ownership técnico: Plataforma de microservicios Retail

> Este repositorio es sintético y no contiene información real de negocio.
