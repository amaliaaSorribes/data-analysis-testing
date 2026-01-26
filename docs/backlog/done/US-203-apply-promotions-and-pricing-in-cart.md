# US-203 - Apply promotions and pricing in cart

---

## Identificación

- **ID:** US-203  
- **Fecha:** 2025-03-20  
- **Servicio:** cart-service, pricing-service, promotion-engine-service  

---

## User Story

Como usuario quiero que las promociones y precios se apliquen correctamente en mi carrito para ver siempre el precio final real antes de pagar.

---

## Descripción

En determinadas situaciones, las promociones y precios no se recalculaban correctamente cuando se modificaba el carrito, provocando diferencias entre el precio mostrado y el esperado.  
Se ha unificado el cálculo de pricing y promociones en cada operación sobre el carrito.

---

## Cambios

### Qué se añadió

- Recalculo de precios y promociones al añadir, eliminar o actualizar productos del carrito.
- Integración del pricing y promotion engine en el flujo de actualización del carrito.
- Devolución del detalle de descuentos aplicados en la respuesta del carrito.

---

## Impacto en APIs

### Nuevo endpoint

No aplica. Se mantiene el contrato actual de los endpoints de carrito.
