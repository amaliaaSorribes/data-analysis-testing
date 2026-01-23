# Documento Funcional – Unificación endpoint añadir al carrito (2025-03-18)

## Descripción General

Unificación del comportamiento de añadir productos al carrito en web y app, eliminando inconsistencias en precios y promociones debidas al uso de endpoints distintos. El objetivo es que ambos canales utilicen el mismo endpoint y lógica para el proceso de add-to-cart.

---

## Lógica Funcional

Actualmente existen dos endpoints diferentes para añadir productos al carrito (uno para web y otro para app), lo que genera duplicidad de lógica y discrepancias en el cálculo de precios y aplicación de promociones. Se propone unificar ambos canales en un solo endpoint (`POST /v2/cart/items`) que reciba `productId` y `quantity`, recalcule precios y promociones, y devuelva el carrito completo. El Frontend de web y app deberán consumir este nuevo endpoint.

---

## Lógica Frontend

- El frontend de web y app deberá llamar al nuevo endpoint unificado `POST /v2/cart/items` para añadir productos al carrito.
- El endpoint recibirá `productId` y `quantity` y devolverá el carrito completo actualizado.

---

## Lógica Backend

- Creación de una nueva versión del endpoint para añadir al carrito: `POST /v2/cart/items`.
- El endpoint debe:
  - Recibir `productId` y `quantity`.
  - Invocar siempre al Pricing Service para el recálculo de precios.
  - Aplicar promociones a través del Promotion Engine en el mismo flujo.
  - Devolver el carrito completo.
- El endpoint antiguo de app se elimina.
- Se mantiene compatibilidad temporal para el endpoint de web.
- No se modifica el modelo de datos.

---

## Partes Afectadas

- Cart Service: nueva versión del endpoint.
- Pricing Service: integración en el flujo de add-to-cart.
- Promotion Engine: integración en el flujo de add-to-cart.

---

## Dudas pendientes

- Cuánto tiempo mantener la compatibilidad con el endpoint antiguo.
- Si es necesario versionar el endpoint antiguo.
- Qué ocurre con los clientes antiguos de la app.

---

## Comentarios finales

- Crear una US técnica.
- Documentar el nuevo endpoint.
- Coordinar con frontend.