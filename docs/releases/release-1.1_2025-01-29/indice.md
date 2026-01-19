# Release 1.1

Sprint enfocado en ampliar el carrito con soporte para promociones
y habilitar el flujo de checkout.

---

## Objetivo

Permitir aplicar promociones al carrito y proceder al checkout,
dejando el carrito en estado finalizado.

---

## Historias incluidas

- **US-102 – Añadir ítem al carrito**
  - 📄 [Detalle US-102](./US-102_add_item_to_cart.md)
  - Commits relacionados:
    - `feat(cart): add item to cart`
    - `feat(cart): recalculate totals`

- **US-103 – Aplicar promoción al carrito**
  - 📄 [Detalle US-103](./US-103_apply_promo.md)
  - Commits relacionados:
    - `feat(cart): apply promo code`
    - `feat(cart): discount calculation`

- **US-104 – Proceder al checkout**
  - 📄 [Detalle US-104](./US-104_checkout_cart.md)
  - Commits relacionados:
    - `feat(cart): checkout cart`
    - `feat(cart): change cart status`

---

## Documentos afectados

> Este release no introduce ni modifica documentación acumulada externa.  
> Toda la definición técnica vive en las user stories incluidas.
