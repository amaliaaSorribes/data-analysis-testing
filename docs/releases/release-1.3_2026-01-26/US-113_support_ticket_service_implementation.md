# US-113 - Support Ticket Service Implementation

---

## Identificación

- **ID:** US-113
- **Fecha:** 2026-01-27
- **Servicio:** cart-service

---

## User Story

Como usuario quiero crear tickets de soporte que se enriquezcan automáticamente con información relevante de mis pedidos, pagos y envíos para recibir respuestas más rápidas y precisas a mis consultas frecuentes.

---

## Descripción

Se requiere implementar un nuevo servicio de soporte que permita la creación de tickets desde el frontend, enviando los campos userId, subject, message y category. El backend consultará automáticamente los servicios de pedidos, pagos y envíos para enriquecer el ticket con contexto relevante. El sistema generará auto-respuestas para preguntas frecuentes detectadas por keywords y, si la consulta no se resuelve automáticamente, el ticket se escalará a un agente humano incluyendo todo el contexto recopilado. El usuario podrá consultar el detalle y el historial de sus tickets, y será notificado si su ticket es escalado.

---

## Cambios

### Qué se añadió

- Implementación de un nuevo servicio de soporte con lógica de enriquecimiento automático de tickets.
- Generación de auto-respuestas para preguntas frecuentes.
- Escalamiento automático a agentes humanos cuando sea necesario.
- Consulta de detalle e historial de tickets por usuario.

---

## Impacto en APIs

### Nuevo endpoint

- `POST /v1/support/tickets`  
  - Request: { userId, subject, message, category }  
  - Response: ticket + auto-respuesta si aplica

- `GET /v1/support/tickets/{ticketId}`  
  - Permite consultar el detalle de un ticket.

- `GET /v1/support/tickets/user/{userId}`  
  - Permite consultar el historial de tickets de un usuario.

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-27/funcional.md)
