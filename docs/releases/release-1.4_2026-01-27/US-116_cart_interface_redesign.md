# US-116 - Cart Interface Redesign

---

## Identificación

- **ID:** US-116
- **Fecha:** 2026-01-27
- **Servicio:** cart-service

---

## User Story

Como usuario quiero una interfaz de carrito rediseñada y optimizada para dispositivos móviles para poder visualizar claramente la información relevante, modificar cantidades fácilmente y finalizar mi compra de forma sencilla.

---

## Descripción

Se requiere un rediseño completo de la vista de carrito aplicando un sistema de diseño moderno y consistente. El objetivo es mejorar la jerarquía visual, destacar el botón de "Finalizar compra" como CTA principal, optimizar la experiencia en dispositivos móviles y asegurar la accesibilidad conforme a WCAG 2.1. El rediseño incluye feedback visual interactivo al modificar cantidades, cards visuales para cada ítem, sección de resumen sticky, animaciones sutiles, indicadores de descuentos, badges de promociones, opción de "guardar para después", sugerencias de productos relacionados y actualización en tiempo real del subtotal. Los nuevos componentes deben documentarse en Storybook y se debe realizar A/B testing antes del despliegue completo.

---

## Cambios

### Qué se añadió

- Nuevo componente CartView con diseño actualizado.
- Cards visuales para cada ítem del carrito.
- Sección de resumen de compra destacada y sticky.
- Animaciones sutiles al modificar cantidades.
- Indicadores visuales de descuentos aplicados.
- Botón CTA principal destacado ("Finalizar compra").
- Thumbnails de productos ampliados.
- Visualización de precio original y con descuento.
- Actualización en tiempo real del subtotal.
- Badges para ofertas/promociones.
- Opción "guardar para después".
- Sugerencias de productos relacionados.
- Interfaz responsive.
- Cumplimiento de accesibilidad WCAG 2.1.
- Documentación en Storybook.
- A/B testing previo al rollout.

---

## Impacto en APIs

### Nuevo endpoint

No se especifican nuevos endpoints en el documento funcional.

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-27/funcional.md)
