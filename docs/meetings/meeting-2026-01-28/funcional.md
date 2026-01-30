# Documento funcional – Timeouts en procesamiento de pagos (2026-01-28)

## Descripción General

Se aborda la problemática de timeouts durante el procesamiento de pagos en el checkout, que genera incertidumbre en los usuarios, dobles cargos y abandono del proceso de compra. Se propone una serie de mejoras para optimizar la experiencia y evitar incidencias relacionadas con los tiempos de espera y la duplicidad de pagos.

- **HU:**  
- **Figma:**  

---

## Lógica Funcional

- Aumentar el timeout del Payment Service a 90 segundos para adaptarse a los tiempos de respuesta de la pasarela externa.
- Implementar un estado intermedio "processing" para los intentos de pago.
- Guardar cada intento de pago con estado "pending" y asociar una idempotency key única.
- Utilizar un webhook para recibir confirmaciones de la pasarela de pago.
- El frontend realizará polling periódico para consultar el estado del pago.
- Se previene el doble cargo utilizando idempotency keys.
- Mensaje claro e informativo al usuario durante el procesamiento del pago.
- Registro detallado de cada intento y monitoreo de tiempos de respuesta.

---

## Lógica Frontend

- Mostrar un estado de carga ("loading") con mensaje informativo: "Procesando pago, por favor espera...".
- Iniciar polling cada 3 segundos para consultar el estado del pago mediante el endpoint GET /v1/payments/{paymentId}/status.
- Deshabilitar el botón de pago tras el primer click para evitar múltiples envíos.
- Generar y enviar una idempotency key única por sesión y carrito al iniciar el pago.
- Detectar el cambio de estado a "completed" para mostrar el éxito al usuario.
- Si el usuario recarga la página, se mantiene el estado y no se duplica el intento de pago.

---

## Lógica Backend

- Modificar el Payment Service para aumentar el timeout HTTP a 90 segundos.
- Crear un nuevo estado "processing" en la base de datos para los intentos de pago.
- Generar y almacenar una idempotency key por cada intento de pago.
- Implementar el endpoint GET /v1/payments/{paymentId}/status para consulta de estado.
- Implementar el webhook POST /v1/payments/webhook para recibir confirmaciones de la pasarela.
- Validar la firma de la pasarela en el webhook.
- Registrar logs detallados de cada intento de pago.
- Monitorear los tiempos de respuesta de la pasarela.
- Nueva colección en base de datos: payment_attempts con los campos paymentId, status, idempotencyKey, timestamp.

---

## Nuevos servicios

- Endpoint GET /v1/payments/{paymentId}/status: permite consultar el estado del pago.
- Webhook POST /v1/payments/webhook: recibe confirmaciones de la pasarela de pago.

---

## Consideraciones

- Idempotency key única por sesión y carrito.
- Mensaje claro al usuario durante la espera.
- Plan B si la pasarela está caída.

---

## Flujo propuesto

1. Usuario hace click en "Pagar ahora".
2. Frontend genera idempotency key.
3. Envía POST /v1/payments con la key.
4. Payment Service crea registro "processing".
5. Llama a la pasarela externa.
6. Frontend inicia polling de estado.
7. Pasarela confirma pago (vía webhook o response).
8. Payment Service actualiza a "completed".
9. Frontend detecta cambio y muestra éxito.
10. Si usuario recarga, se mantiene el mismo estado y no se duplica el intento.

---

## Partes Afectadas

*(No hay información suficiente en el transcript para completar las siguientes secciones, por lo que se eliminan del documento final)*