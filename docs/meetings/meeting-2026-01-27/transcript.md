# Notas reunión – problema tiempos de respuesta en soporte

Fecha: 2026-01-27  
Asistentes: Customer Success, Soporte, Producto, Tech Lead  
Tema: Tiempos de espera en soporte demasiado largos

---

- Tiempo medio de respuesta: 36 horas
- 60% son preguntas repetitivas (tracking, cancelaciones, pagos)
- Soporte saturado sin contexto del usuario
- No hay sistema de auto-respuestas

---

## Problema identificado

- Usuario abre ticket → espera días
- Soporte responde manualmente preguntas frecuentes
- Sin contexto: no saben qué compró, cuándo, estado de envío
- No escala con crecimiento

---

## Tickets más comunes

- "¿Dónde está mi pedido?" → 30%
- "¿Cómo cancelo pedido?" → 20%  
- "El pago falló" → 15%
- "Cambiar dirección envío" → 10%

---

## Solución propuesta

- Nuevo servicio: Support Ticket Service
- Al crear ticket → consulta automática pedidos/pagos/envíos del usuario
- Enriquece ticket con contexto
- Auto-respuestas para preguntas frecuentes
- Si no puede resolver → escala a humano con contexto completo

---

## Cambios técnicos

- Nuevo endpoint: POST /v1/support/tickets
  - Request: { userId, subject, message, category }
  - Backend consulta orders, payments, tracking
  - Response: ticket + auto-respuesta si aplica

- Nueva colección: support_tickets
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
