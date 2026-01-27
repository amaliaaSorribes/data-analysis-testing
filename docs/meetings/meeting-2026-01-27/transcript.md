# Notas reunión – errores al actualizar cantidades en carrito

Fecha: 2026-01-27  
Asistentes: Producto, Backend, Frontend, QA  
Tema: Usuarios reportan errores al intentar modificar cantidades de productos en el carrito

---

- 22 tickets reportados esta semana
- Al cambiar cantidad → a veces no se actualiza
- Doble-click genera duplicados
- Cantidades negativas permitidas en algunos casos
- Totales no se recalculan correctamente
- Frustración del usuario

---

## Situación actual

- Frontend permite modificar cantidad sin validación
- Backend no valida límites de cantidad
- No hay debouncing en requests
- Múltiples requests simultáneos causan inconsistencias
- Sin validación de stock disponible al aumentar

---

## Problema identificado

- Falta validación robusta de cantidades
- Ejemplo:
  1. Usuario cambia cantidad de 2 a 5
  2. Click rápido genera múltiples requests
  3. Backend procesa ambos
  4. Cantidad final incorrecta: 10 en lugar de 5
  5. Total calculado mal
  6. Usuario debe recargar página

---

## Impacto

- Errores en pedidos: usuarios reciben cantidades incorrectas
- Abandono por falta de confianza: +12%
- Tickets de soporte innecesarios
- Reputación del sistema afectada

---

## Solución propuesta

- Validación estricta de cantidades en backend
- Debouncing en frontend
- Endpoint dedicado: PATCH /v1/carts/{cartId}/items/{itemId}
- Validar límites: mínimo 1, máximo según stock
- Response con cantidad actualizada y total recalculado
- Optimistic UI con rollback si falla

---

## Cambios técnicos necesarios

- Modificar Cart Service:
  - Validar quantity > 0 y quantity <= stock disponible
  - Rechazar si supera límite
  - Recalcular total automáticamente
  - Response: { itemId, newQuantity, subtotal, cartTotal }
- Frontend:
  - Debounce de 500ms en cambios de cantidad
  - Deshabilitar input durante update
  - Mostrar loading state
  - Rollback a cantidad anterior si error
- Validaciones:
  - Mínimo: 1
  - Máximo: stock disponible (consultar a Catalog)
  - Tipo: integer positivo

---

## Flujo propuesto

1. Usuario modifica cantidad en input
2. Frontend espera 500ms (debounce)
3. Envía PATCH /v1/carts/{cartId}/items/{itemId}
4. Backend valida cantidad
5. Si válida: actualiza y recalcula total
6. Si inválida: devuelve 422 con límites
7. Frontend actualiza UI con cantidad y total
8. Usuario ve cambio inmediato y correcto

---

## Consideraciones

- Sincronización con stock en tiempo real
- Mensajes de error claros: "Stock disponible: 3 unidades"
- Logging de errores de validación
- Monitoreo de requests duplicados
