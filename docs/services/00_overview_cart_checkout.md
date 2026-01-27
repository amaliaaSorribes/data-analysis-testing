# 00 — Overview: Cart & Checkout System

## 1. Propósito del documento
Este documento ofrece una **visión general** del sistema **Cart & Checkout** de un retailer, describiendo su **alcance**, **arquitectura a alto nivel**, **dominios funcionales**, **microservicios** y **flujos principales**. Sirve como punto de entrada para entender el sistema antes de profundizar en los detalles de cada componente.

---

## 2. Alcance del sistema
El sistema Cart & Checkout cubre el ciclo completo desde la **ingesta de datos comerciales** (catálogo, precios y promociones) hasta la **creación del pedido pendiente de pago**, incluyendo:

- Gestión del carrito y sesión de compra, incluyendo validación de precios en tiempo real al añadir productos al carrito y actualización de cantidades de ítems existentes con recalculo automático de subtotales y descuentos.
- Cálculo de precios y aplicación de promociones, incluyendo la aplicación secuencial de descuentos combinados con validación de límites y generación de alertas.
- Disponibilidad y coste de entrega en sesión
- Orquestación del checkout
- Gestión del estado del pago
- Seguimiento del envío
- Gestión de stock en tiempo real durante el checkout

**Fuera de alcance** (explícito):
- Pasarela de pago real (PSP)
- Facturación y postventa
- Infraestructura (CI/CD, cloud, redes)

---

## 3. Contexto de negocio (retail)
El sistema está pensado para un retailer omnicanal con:
- Catálogo amplio y cambiante
- Precios dependientes de canal/tienda/moneda
- Promociones complejas (cupones, bundles, descuentos)
- Alta concurrencia en picos (campañas)
- Necesidad de mantener el carrito “vivo” en sesión

---

## 4. Arquitectura a alto nivel

### 4.1 Principios
- **Arquitectura de microservicios** por dominio
- **Separación** entre ingesta asíncrona y servicios transaccionales
- **Persistencia por ownership** (cada microservicio es dueño de sus datos)
- **Consistencia eventual** para datos de ingesta
- **APIs REST** para operaciones síncronas
- **Eventos/colas** para integración y desacoplamiento

### 4.2 Tipos de microservicios
1. **Ingesta (async)**
   - Consumen eventos desde colas
   - Normalizan/validan datos
   - Persisten en MongoDB
   - Publican eventos derivados (opcional)

2. **Transaccionales (sync)**
   - Exponen APIs REST
   - Validan precios en tiempo real al añadir productos al carrito mediante integración con Pricing Service
   - Son llamados por la web/app de compras
   - Operan en contexto de sesión
   - Orquestan cálculos y validaciones

### 4.3 Endpoints de microservicios
- **POST** `/v1/promotions/calculate-preview`: Permite validar y obtener un desglose de descuentos antes de aplicar la promoción.

---

## 5. Dominios funcionales

- **Catalog**: productos, atributos, categorías
- **Pricing**: precios base, impuestos, moneda, vigencias
- **Promotions**: reglas promocionales, cupones, bundles
- **Cart**: carrito, ítems, cantidades, totales en sesión
- **Delivery**: opciones y coste de entrega
- **Checkout**: validación final y creación del pedido
- **Payments**: estado del pago
- **Tracking**: seguimiento logístico

---

## 6. Microservicios (lista y responsabilidades)

### Ingesta

- **Catalog Ingestion Service**  
  Ingesta y persistencia del catálogo de productos.  
  📄 Documento: [`10_catalog_ingestion_service.md`](10_catalog_ingestion_service.md)

- **Pricing Ingestion Service**  
  Ingesta de precios base por canal/tienda/moneda y gestión de vigencias.  
  📄 Documento: [`11_pricing_ingestion_service.md`](11_pricing_ingestion_service.md)

- **Promotions Ingestion Service**  
  Ingesta de promociones, reglas y cupones.  
  📄 Documento: [`12_promotions_ingestion_service.md`](12_promotions_ingestion_service.md)

### Transaccionales

- **Cart Service**  
  Gestión del carrito y sesión: añadir/eliminar ítems, cantidades, totales en sesión.  
  📄 Documento: [`20_cart_service.md`](20_cart_service.md)

- **Pricing Service**  
  Cálculo de precios y totales (*quote*) a partir de los ítems del carrito.  
  📄 Documento: [`21_pricing_service.md`](21_pricing_service.md)

- **Promotion Engine Service**  
  Aplicación de promociones y validación de cupones.  
  📄 Documento: [`22_promotion_engine_service.md`](22_promotion_engine_service.md)

- **Delivery Options Service**  
  Disponibilidad y coste de entrega en sesión.  
  📄 Documento: [`23_delivery_options_service.md`](23_delivery_options_service.md)

- **Checkout Service**  
  Orquestación del checkout y creación del pedido pendiente de pago.  
  📄 Documento: [`30_checkout_service.md`](30_checkout_service.md)

- **Payment Status Service**  
  Consulta y actualización del estado del pago.  
  📄 Documento: [`31_payment_status_service.md`](31_payment_status_service.md)

- **Tracking Service**  
  Seguimiento del envío y estados logísticos.  
  📄 Documento: [`32_tracking_service.md`](32_tracking_service.md)

---

## 7. Flujos principales

### 7.1 Ingesta de datos comerciales
1. Publicación de eventos de catálogo/precios/promos
2. Consumo por servicios de ingesta
3. Validación y normalización
4. Persistencia en MongoDB
5. (Opcional) Emisión de eventos derivados

### 7.2 Compra (happy path)
1. Usuario crea o recupera un carrito
2. Añade productos y modifica cantidades
3. Sistema calcula totales (pricing + promos)
4. Usuario consulta opciones de entrega y coste
5. Usuario procede al checkout
6. Se valida el estado final del carrito
7. Se crea un pedido pendiente de pago
8. Se consulta el estado del pago
9. Se permite el seguimiento del pedido

---

## 8. Modelo de datos (visión global)
Cada microservicio es **dueño** de sus colecciones MongoDB. A alto nivel:

- `products` → catálogo
- `prices` → precios base
- `promotions` → promociones
- `carts` → carritos en sesión
- `orders` → pedidos
- `payments` → estado del pago
- `delivery_options` → opciones/costes de entrega
- `outbox_events` (opcional) → eventos publicados

Los detalles de esquema se describen en `02_modelo_datos_mongo.md`.

---

## 9. Eventos y colas (visión global)
El sistema utiliza eventos para:
- Ingesta desacoplada de datos
- Propagación de cambios relevantes
- Comunicación de estados (ej. pago)

Ejemplos:
- `catalog.product.upserted`
- `pricing.price.updated`
- `promotions.promo.published`
- `checkout.order.created`
- `payment.status.changed`

Los contratos completos se describen en `03_eventos_y_colas.md`.

---

## 10. Consideraciones transversales

- **Idempotencia**: obligatoria en ingestión
- **Versionado de APIs**: `/v1`
- **Errores estándar**: 4xx funcionales, 5xx técnicos
- **Expiración de carritos**: TTL por inactividad
- **Observabilidad**: logs y métricas conceptuales
- **Compatibilidad**: cambios breaking documentados en releases

---

## 11. Lecturas relacionadas

### Documentación base
- Glosario y convenciones: [`01_glosario_y_convenciones.md`](01_glosario_y_convenciones.md)
- Modelo de datos MongoDB: [`02_modelo_datos_mongo.md`](02_modelo_datos_mongo.md)
- Eventos y colas: [`03_eventos_y_colas.md`](03_eventos_y_colas.md)

### Servicios de ingesta
- Catalog Ingestion Service: [`10_catalog_ingestion_service.md`](10_catalog_ingestion_service.md)
- Pricing Ingestion Service: [`11_pricing_ingestion_service.md`](11_pricing_ingestion_service.md)
- Promotions Ingestion Service: [`12_promotions_ingestion_service.md`](12_promotions_ingestion_service.md)

### Servicios transaccionales
- Cart Service: [`20_cart_service.md`](20_cart_service.md)
- Pricing Service: [`21_pricing_service.md`](21_pricing_service.md)
- Promotion Engine Service: [`22_promotion_engine_service.md`](22_promotion_engine_service.md)
- Delivery Options Service: [`23_delivery_options_service.md`](23_delivery_options_service.md)
- Checkout Service: [`30_checkout_service.md`](30_checkout_service.md)
- Payment Status Service: [`31_payment_status_service.md`](31_payment_status_service.md)
- Tracking Service: [`32_tracking_service.md`](32_tracking_service.md)
