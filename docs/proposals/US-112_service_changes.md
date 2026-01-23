```markdown
# Propuesta de actualización - US-112

## Resumen de la US
La US-112 introduce un nuevo endpoint unificado `POST /v2/cart/items` en el Cart Service para gestionar la adición de productos al carrito, eliminando inconsistencias en precios y promociones. Este endpoint reemplaza al antiguo endpoint de la app (`POST /v2/cart/add`) y mantiene compatibilidad temporal con el endpoint antiguo de la web (`POST /v1/cart/items`). No se realizan cambios en el modelo de datos.

## Análisis de impacto
La documentación del Cart Service debe actualizarse para reflejar el nuevo endpoint y los cambios en los endpoints existentes. Además, se deben mencionar las dependencias con el Pricing Service y el Promotion Engine Service. No se identifican impactos en otros servicios.

## Cambios propuestos

### 20_cart_service.md

#### Cambio 1: Actualización de la sección "Responsabilidad y límites"
**Sección afectada:** Responsabilidad y límites  
**Tipo de cambio:** Modificar  

**Justificación:**  
El nuevo endpoint introduce una dependencia explícita con el Pricing Service y el Promotion Engine Service para recalcular precios y promociones. Esto debe reflejarse en la descripción de las responsabilidades del Cart Service.

**Contenido propuesto:**
```
Este servicio es responsable de:
- Crear y mantener carritos activos
- Añadir, modificar y eliminar productos
- Aplicar reglas básicas de negocio en sesión
- Persistir el estado del carrito
- Orquestar (o simular) llamadas a servicios externos como el **Pricing Service** y el **Promotion Engine Service** para recalcular precios y promociones en tiempo real
```

**Ubicación:**  
Reemplazar la lista de responsabilidades actual en la sección "Responsabilidad y límites".

---

#### Cambio 2: Añadir descripción del nuevo endpoint
**Sección afectada:** Endpoints  
**Tipo de cambio:** Añadir  

**Justificación:**  
El nuevo endpoint `POST /v2/cart/items` debe documentarse para que los desarrolladores comprendan su propósito, parámetros y comportamiento.

**Contenido propuesto:**
```
### POST `/v2/cart/items` — Añadir productos al carrito (unificado)
Recibe un `productId` y una `quantity`, recalcula precios y promociones utilizando el Pricing Service y el Promotion Engine, y devuelve el carrito completo.

#### Parámetros
- **Body (JSON)**:
  - `productId` (string, requerido): ID del producto a añadir.
  - `quantity` (integer, requerido): Cantidad del producto.

#### Respuesta
- **200 OK**: Devuelve el carrito completo con los precios y promociones actualizados.
- **400 Bad Request**: Si los parámetros son inválidos.
- **500 Internal Server Error**: En caso de error interno.

#### Notas
- Este endpoint reemplaza al antiguo `POST /v2/cart/add`.
- Mantiene compatibilidad temporal con `POST /v1/cart/items` para la web.
```

**Ubicación:**  
Añadir al final de la sección "Endpoints".

---

#### Cambio 3: Marcar el endpoint antiguo como deprecado
**Sección afectada:** Endpoints  
**Tipo de cambio:** Deprecar  

**Justificación:**  
El endpoint `POST /v2/cart/add` ha sido eliminado y debe marcarse como deprecado en la documentación para evitar confusiones.

**Contenido propuesto:**
```
### [Deprecado] POST `/v2/cart/add` — Añadir productos al carrito (antiguo)
Este endpoint ha sido eliminado y reemplazado por `POST /v2/cart/items`. No debe ser utilizado en nuevas implementaciones.
```

**Ubicación:**  
Después de la descripción del nuevo endpoint.

---

## Recomendaciones
1. Asegurarse de que los equipos de desarrollo y QA estén informados sobre la eliminación del endpoint antiguo (`POST /v2/cart/add`) para evitar su uso en nuevas integraciones.
2. Actualizar cualquier documentación externa o tutoriales que mencionen el endpoint antiguo.

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