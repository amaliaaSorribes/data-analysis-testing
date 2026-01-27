# Notas reunión – timeouts en procesamiento de pagos

Fecha: 2026-01-28  
Asistentes: Producto, Backend, Payments Team, QA  
Tema: Usuarios experimentan timeouts durante el procesamiento de pagos

---

- 28 casos reportados este mes de timeouts en checkout
- Usuario ingresa datos de pago → espera indefinida
- Timeout después de 30 segundos
- No queda claro si el pago se procesó o no
- Usuarios intentan pagar de nuevo → doble cargo en algunos casos
- Abandono del 18% en este paso

---

## Situación actual

- Payment Service tiene timeout de 30 segundos
- Pasarela de pago externa a veces tarda más
- Frontend no muestra feedback durante la espera
- Sin manejo de estados intermedios
- No hay retry automático

---

## Problema identificado

- Timeout demasiado agresivo para pagos
- Ejemplo:
  1. Usuario completa datos de pago
  2. Click en "Pagar ahora"
  3. Frontend envía request a Payment Service
  4. Payment Service llama a pasarela externa
  5. Pasarela tarda 35 segundos en responder
  6. Timeout en segundo 30
  7. Usuario ve error genérico
  8. No sabe si pagó o no
  9. Algunos reintentan → doble cargo

---

## Impacto

- Abandono en paso final: 18%
- Reclamaciones por dobles cargos: 12 casos/mes
- Tiempo de soporte resolviendo casos
- Pérdida de confianza en el sistema
- Ventas perdidas estimadas: 8.500€/mes

---

## Solución propuesta

- Aumentar timeout a 90 segundos
- Implementar processing state intermedio
- Guardar intento de pago con status "pending"
- Webhook de confirmación desde pasarela
- Polling desde frontend para verificar estado
- Evitar dobles cargos con idempotency keys

---

## Cambios técnicos necesarios

- Modificar Payment Service:
  - Aumentar timeout HTTP a 90 segundos
  - Crear estado "processing" en base de datos
  - Generar idempotency key por intento
  - Endpoint: GET /v1/payments/{paymentId}/status
  - Webhook: POST /v1/payments/webhook para confirmaciones
- Frontend:
  - Mostrar loading state con mensaje informativo
  - Polling cada 3s para verificar estado
  - Deshabilitar botón de pago tras primer click
  - Mensaje: "Procesando pago, por favor espera..."
- Base de datos:
  - Nueva colección: payment_attempts
  - Campos: paymentId, status, idempotencyKey, timestamp

---

## Flujo propuesto

1. Usuario click "Pagar ahora"
2. Frontend genera idempotency key
3. Envía POST /v1/payments con key
4. Payment Service crea registro "processing"
5. Llama a pasarela externa
6. Frontend inicia polling de estado
7. Pasarela confirma pago (via webhook o response)
8. Payment Service actualiza a "completed"
9. Frontend detecta cambio y muestra éxito
10. Si usuario recarga → mismo estado, no duplica

---

## Consideraciones

- Idempotency key único por sesión + carrito
- Webhook debe validar firma de pasarela
- Logs detallados de cada intento
- Monitoreo de tiempos de respuesta de pasarela
- Plan B si pasarela está caída
- Mensaje claro al usuario durante espera
