# Documento Funcional – Cambio en endpoint de añadir al carrito (2025-03-18)

## Descripción General

Unificación del comportamiento de añadir productos al carrito en web y app, utilizando un único endpoint para evitar inconsistencias en precios y promociones.

---

## Lógica Funcional

Actualmente existen dos endpoints distintos para añadir productos al carrito, lo que genera lógica duplicada y diferencias en el cálculo de precios y aplicación de promociones. Se propone unificar ambos flujos en un solo endpoint (`POST /v2/cart/items`) que reciba `productId` y `quantity`, recalcule precios y promociones, y devuelva el carrito completo. Tanto el frontend web como la app deberán consumir este nuevo endpoint.

---

## Lógica Frontend

El frontend, tanto web como app, deberá llamar al nuevo endpoint unificado (`POST /v2/cart/items`) enviando `productId` y `quantity`. El backend devolverá el carrito completo con los precios y promociones recalculados.

---

## Lógica Backend

- Creación de un nuevo endpoint: `POST /v2/cart/items`.
- El endpoint recibirá `productId` y `quantity`.
- Se invocará siempre el servicio de precios (Pricing Service) y el motor de promociones (Promotion Engine) en el flujo de añadir al carrito.
- El endpoint devolverá el carrito completo.
- Se elimina el endpoint antiguo de la app.
- Se mantiene compatibilidad temporal para el endpoint web.
- No se modifica el modelo de datos.

---

## Partes Afectadas

No se especifica información sobre sites afectados.

---

## Decisiones

- Eliminación del endpoint antiguo de la app.
- Compatibilidad temporal para el endpoint web.
- No se cambia el modelo de datos.

---

## Dudas pendientes

- Definir el tiempo de mantenimiento de la compatibilidad.
- Decidir si es necesario versionar el endpoint antiguo.
- Determinar el comportamiento para clientes antiguos de la app.

---

## Comentarios finales

- Crear una US técnica.
- Documentar el nuevo endpoint.
- Coordinar con frontend.