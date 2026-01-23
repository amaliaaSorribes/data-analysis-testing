```markdown
# Propuesta de actualización - US-112

## Resumen de la US
La US-112 introduce un nuevo endpoint unificado `POST /v2/cart/items` en el Cart Service para añadir productos al carrito, recalculando precios y promociones mediante el Pricing Service y el Promotion Engine. Este cambio elimina el endpoint antiguo de la app (`POST /v2/cart/add`) y mantiene compatibilidad temporal con el endpoint antiguo de la web (`POST /v1/cart/items`).

## Análisis de impacto
La documentación del Cart Service debe actualizarse para reflejar el nuevo endpoint y los cambios en los endpoints existentes. Además, se deben mencionar las dependencias con el Pricing Service y el Promotion Engine en el contexto del nuevo endpoint.

## Cambios propuestos

### 20_cart_service.md

#### Cambio 1: Actualización de responsabilidades
**Sección afectada:** Responsabilidad y límites  
**Tipo de cambio:** Modificar

**Justificación:**  
La introducción del nuevo endpoint implica que el Cart Service ahora debe recalcular precios y aplicar promociones al añadir productos al carrito, utilizando el Pricing Service y el Promotion Engine. Esto amplía las responsabilidades del servicio.

**Contenido propuesto:**
```
Este servicio es responsable de:
- Crear y mantener carritos activos
- Añadir, modificar y eliminar productos
- Recalcular precios y aplicar promociones al añadir productos al carrito, utilizando el Pricing Service y el Promotion Engine
- Aplicar reglas básicas de negocio en sesión
- Persistir el estado del carrito
- Orquestar (o simular) llamadas a servicios externos relacionados con el carrito
```

**Ubicación:**  
Reemplazar la lista de responsabilidades existente en la sección "Responsabilidad y límites".

---

#### Cambio 2: Documentación del nuevo endpoint
**Sección afectada:** Endpoints  
**Tipo de cambio:** Añadir

**Justificación:**  
El nuevo endpoint `POST /v2/cart/items` debe documentarse para que los desarrolladores comprendan su propósito, parámetros y funcionamiento.

**Contenido propuesto:**
```
### POST `/v2/cart/items` — Añadir producto al carrito
**Descripción:**  
Este endpoint permite añadir un producto al carrito unificado, recalculando precios y promociones. Devuelve el carrito completo actualizado.

**Parámetros:**
- **productId** (string, requerido): ID del producto a añadir.
- **quantity** (integer, requerido): Cantidad del producto a añadir.

**Dependencias:**
- **Pricing Service:** Recalcula los precios de los productos en el carrito.
- **Promotion Engine:** Aplica promociones activas al carrito.

**Respuesta:**
- **200 OK:** Carrito actualizado con los productos añadidos, precios y promociones aplicados.
- **400 Bad Request:** Parámetros inválidos.
- **500 Internal Server Error:** Error interno en el procesamiento.
```

**Ubicación:**  
Añadir al final de la sección "Endpoints".

---

#### Cambio 3: Deprecación de endpoint antiguo
**Sección afectada:** Endpoints  
**Tipo de cambio:** Deprecar

**Justificación:**  
El endpoint `POST /v2/cart/add` de la app ha sido eliminado y debe indicarse como deprecado en la documentación.

**Contenido propuesto:**
```
### POST `/v2/cart/add` — [Deprecado]
**Nota:** Este endpoint ha sido eliminado y reemplazado por `POST /v2/cart/items`. Se recomienda actualizar las integraciones existentes.
```

**Ubicación:**  
Modificar la descripción del endpoint `POST /v2/cart/add` en la sección "Endpoints".

---

## Recomendaciones
1. Asegurarse de que los desarrolladores externos estén informados sobre la deprecación del endpoint `POST /v2/cart/add`.
2. Revisar la documentación del Pricing Service y el Promotion Engine para verificar que no se requieran cambios adicionales relacionados con las dependencias introducidas.

## Comandos de aplicación
```bash
# Revisar propuesta
cat docs/proposals/US-112_service_changes.md

# Aprobar y aplicar cambios
python agents/doc_updater/apply_proposal.py US-112 --approve

# Rechazar propuesta
python agents/doc_updater/apply_proposal.py US-112 --reject
```
```