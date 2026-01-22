```markdown
# Documento Funcional - Cambio en endpoint de añadir al carrito (2025-03-18)

## Descripción General

Unificación del comportamiento al añadir productos al carrito entre la web y la app mediante la creación de un único endpoint. Esto busca resolver inconsistencias en precios y promociones, además de eliminar lógica duplicada.

---

## Lógica Funcional

- Se unifica el comportamiento de añadir al carrito en un único endpoint: `POST /v2/cart/items`.
- El nuevo endpoint:
  - Recibe `productId` y `quantity`.
  - Recalcula precios y promociones.
  - Devuelve el carrito completo.
- Tanto el frontend web como la app utilizarán este nuevo endpoint.
- Se elimina el endpoint antiguo de la app (`POST /v2/cart/add`).
- Se mantiene compatibilidad temporal para el endpoint antiguo de la web (`POST /v1/cart/items`).
- No se realizan cambios en el modelo de datos.

---

## Lógica Backend

- Creación de un nuevo endpoint: `POST /v2/cart/items`.
- El nuevo endpoint:
  - Invoca al servicio de precios (Pricing Service) para recalcular precios.
  - Aplica promociones mediante el motor de promociones (Promotion Engine).
  - Devuelve el carrito completo.
- Actualización del Cart Service para incluir la nueva versión del endpoint.
- Eliminación del endpoint antiguo de la app.
- Compatibilidad temporal para el endpoint antiguo de la web.

---

## Partes Afectadas

### Dependencias con terceros

- Pricing Service: se invoca siempre en el flujo de añadir al carrito.
- Promotion Engine: se aplica en el mismo flujo.

---

## Dudas pendientes

- Definir el tiempo que se mantendrá la compatibilidad temporal para el endpoint antiguo de la web.
- Decidir si es necesario versionar el endpoint antiguo.
- Determinar el impacto en clientes antiguos de la app.

---

## Comentarios finales

- Crear una US técnica para la implementación.
- Documentar detalladamente el nuevo endpoint.
- Coordinar con el equipo de frontend para la integración.
```