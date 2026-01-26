# Documento Funcional – Support Ticket Service (2026-01-27)

## Descripción General

Se propone la implementación de un nuevo servicio de soporte (Support Ticket Service) para reducir los tiempos de respuesta y la carga manual del equipo de soporte. El objetivo es automatizar respuestas a preguntas frecuentes y enriquecer los tickets con contexto relevante del usuario (pedidos, pagos, envíos), mejorando así la experiencia del usuario y la eficiencia operativa.

- **HU:**  
- **Figma:**  

---

## Lógica Funcional

- Al crear un ticket de soporte, el sistema consultará automáticamente la información relevante del usuario (pedidos, pagos, envíos) y enriquecerá el ticket con este contexto.
- Se implementarán auto-respuestas para preguntas frecuentes detectadas por keywords (tracking, cancelaciones, pagos).
- Si la auto-respuesta no resuelve la consulta o no hay suficiente confianza, el ticket se escalará a un agente humano, incluyendo todo el contexto recopilado.
- Los tickets más comunes que se cubrirán inicialmente son: estado de pedido, cancelación de pedido, fallo en el pago y cambio de dirección de envío.
- Siempre existirá la opción de escalar a un humano.

---

## Lógica Frontend

- El frontend permitirá la creación de tickets de soporte enviando los campos: userId, subject, message, category.
- El usuario podrá consultar el detalle de un ticket y su historial.
- Las auto-respuestas se mostrarán inmediatamente si aplican.
- Si el ticket es escalado a un humano, el usuario será notificado.

---

## Lógica Backend

- Nuevo endpoint: `POST /v1/support/tickets` para la creación de tickets.
  - Request: { userId, subject, message, category }
  - El backend consultará los servicios de pedidos, pagos y envíos para enriquecer el ticket.
  - Si corresponde, generará una auto-respuesta.
- Nueva colección: `support_tickets` con los siguientes campos:
  - ticketId, userId, subject, message
  - category, status (pending/answered/closed)
  - context: { orders, payments, shipments }
  - autoResolved: boolean
- Integración con los servicios existentes de Orders, Payments y Tracking.
- Endpoints adicionales:
  - `GET /v1/support/tickets/{ticketId}` para ver el detalle del ticket.
  - `GET /v1/support/tickets/user/{userId}` para ver el historial de tickets de un usuario.

---

## Nuevos servicios

- `POST /v1/support/tickets`
  - Request: { userId, subject, message, category }
  - Response: ticket + auto-respuesta si aplica
- `GET /v1/support/tickets/{ticketId}`
- `GET /v1/support/tickets/user/{userId}`

---

## Partes Afectadas

*(No hay información explícita en el transcript sobre sites afectados, dependencias con terceros, analítica, contingencias, tipo de usuario, método de envío, tipo de mercancía o ventanas de flujo afectadas, por lo que estas secciones se eliminan del documento final.)*