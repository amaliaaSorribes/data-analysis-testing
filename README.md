# 📚 Documentación del proyecto

Este directorio contiene la documentación funcional y técnica del sistema.
La documentación está organizada por **services** y por **releases**, permitiendo
entender tanto el estado actual como la evolución del producto en el tiempo.

---

## 🧭 Estructura general

```text
docs/
├── services/
│   ├── indice.md
│   ├── 00_overview_cart_checkout.md
│   ├── 01_glosario_y_convenciones.md
│   ├── 02_modelo_datos_mongo.md
│   ├── 03_eventos_y_colas.md
│   ├── 10_catalog_ingestion_service.md
│   ├── 11_pricing_ingestion_service.md
│   ├── 12_promotions_ingestion_service.md
│   ├── 20_cart_service.md
│   ├── 21_pricing_service.md
│   ├── 22_promotion_engine_service.md
│   ├── 23_delivery_options_service.md
│   ├── 30_checkout_service.md
│   ├── 31_payment_status_service.md
│   └── 32_tracking_service.md
├── releases/
│   ├── indice_releases.md
│   ├── release-1.0_2026-01-15/
│   │   ├── indice.md
│   │   └── US-101_crear_carrito.md
│   ├── release-1.1_2026-01-29/
│   │   ├── indice.md
│   │   ├── US-102_add_item_to_cart.md
│   │   ├── US-103_apply_promo.md
│   │   └── US-104_checkout_cart.md
│   └── release-1.2_2026-02-12/
│       ├── indice.md
│       ├── US-105_update_item_quantity.md
│       ├── US-106_remove_item_from_cart.md
│       └── US-107_get_cart_detail.md
