# Notas reunión – usuarios añaden productos sin stock al carrito

Fecha: 2026-01-27  
Asistentes: Producto, Backend, Frontend, QA  
Tema: Usuarios pueden añadir al carrito productos que no tienen stock disponible

---

- Frontend muestra productos con stock agotado
- Usuario puede añadir al carrito sin validación previa
- Stock se valida solo en checkout
- Genera frustración y pérdida de tiempo
- 12 tickets reportados esta semana

---

## Situación actual

- Catálogo muestra productos sin verificar stock disponible
- Frontend no valida stock antes de permitir "añadir al carrito"
- Cart Service acepta cualquier producto sin validar
- Stock se verifica solo al finalizar compra
- Usuario descubre el problema tarde en el proceso

---

## Problema identificado

- No hay validación de stock al añadir producto
- Ejemplo:
  1. Producto sin stock aparece en catálogo
  2. Usuario hace click "Añadir al carrito"
  3. Sistema acepta y añade al carrito
  4. Usuario continúa navegando/comprando
  5. En checkout → error "producto sin stock"
  6. Usuario debe remover item y reintentar

---

## Impacto

- Abandono de carrito: +15%
- Experiencia de usuario negativa
- Tiempo perdido del usuario
- Tickets de soporte innecesarios
- Pérdida de confianza en la plataforma

---

## Solución propuesta

- Validar stock disponible antes de añadir al carrito
- Modificar endpoint POST /v1/carts/{cartId}/items
- Consultar stock real del SKU antes de añadir
- Rechazar operación si no hay stock
- Mostrar mensaje claro al usuario

---

## Cambios técnicos necesarios

- Modificar Cart Service:
  - Antes de añadir item → consultar Catalog Service
  - Verificar stock disponible del SKU
  - Si stock = 0 o stock < cantidad solicitada → devolver error 409
  - Incluir stock disponible en response
- Integración con Catalog Service:
  - GET /v1/catalog/stock/{sku}
  - Response: { sku, available, quantity }
- Response de add-to-cart:
  - Si sin stock: { error: "out_of_stock", available: 0 }
  - Si stock insuficiente: { error: "insufficient_stock", requested: 5, available: 2 }

---

## Flujo propuesto

1. Usuario click "Añadir al carrito"
2. Frontend envía: POST /v1/carts/{cartId}/items con sku y quantity
3. Cart Service consulta stock a Catalog Service
4. Si stock suficiente → añade al carrito normalmente
5. Si sin stock → devuelve 409 con mensaje
6. Frontend muestra: "Este producto no está disponible"
7. Usuario ve el error inmediatamente

---

## Consideraciones

- Cache de stock: máximo 30 segundos
- Sincronización con inventario en tiempo real
- Mensaje claro y accionable para el usuario
- Sugerir productos similares con stock disponible
  - ticketId, userId, subject, message
  - category, status (pending/answered/closed)
  - context: { orders, payments, shipments }
  - autoResolved: boolean

- Integración con services existentes:
  - Orders, Payments, Tracking

---

## Auto-respuestas

- Detección por keywords
- "tracking" → consulta envío, responde estado
- "cancelar" → verifica si permite, da instrucciones
- "pago error" → consulta payment status
- Si no hay confianza → escala a humano

---

## Endpoints

- POST /v1/support/tickets → crear ticket
- GET /v1/support/tickets/{ticketId} → ver detalle
- GET /v1/support/tickets/user/{userId} → historial

---

## Beneficios

- 60% menos tickets a humanos
- Respuesta inmediata para FAQs
- Soporte con contexto completo
- Mejor experiencia usuario

---

## Decisiones finales

- Implementar Support Ticket Service
- Tickets enriquecidos con contexto
- Auto-respuestas para tracking/cancelación/pagos
- Siempre opción de escalar a humano
