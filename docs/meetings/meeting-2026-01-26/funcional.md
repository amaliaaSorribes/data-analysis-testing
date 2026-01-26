# Documento funcional – Validación de stock en tiempo real durante checkout (2026-01-26)

## Descripción General

Se implementará una validación de stock en tiempo real durante el proceso de checkout para evitar que los usuarios compren productos sin stock real disponible. El objetivo es reducir cancelaciones, mejorar la experiencia de usuario y minimizar costes operativos asociados a reembolsos y gestión de incidencias.

---

## Lógica Funcional

Durante el checkout, se validará en tiempo real la disponibilidad de los productos seleccionados por el usuario. El frontend enviará la lista de SKUs y cantidades al backend, que consultará el sistema de inventario mediante una API síncrona. Si algún producto no tiene stock suficiente, se notificará al usuario y se bloqueará la compra de ese producto. Todas las validaciones quedarán registradas para auditoría.

---

## Lógica Frontend

- Al llegar el usuario al checkout, el frontend debe llamar al endpoint POST /v1/catalog/validate-stock enviando la lista de SKUs y cantidades.
- El frontend recibirá una respuesta con la disponibilidad actualizada de cada producto.
- Si algún producto no tiene stock suficiente, el frontend debe mostrar un error claro al usuario y bloquear la compra de ese producto.
- Si el servicio de inventario no responde, se debe mostrar una advertencia y permitir la compra en modo degradado.

---

## Lógica Backend

- Crear un nuevo endpoint en el Catalog Service: POST /v1/catalog/validate-stock.
- El endpoint recibirá un request con la lista de SKUs y cantidades.
- El backend consultará la API de inventario de forma síncrona (REST) para obtener el stock actualizado.
- Configurar un timeout de 3 segundos para la consulta a inventario.
- Implementar un circuit breaker para gestionar caídas de la API de inventario.
- Implementar una caché de 30 segundos en las validaciones (Redis).
- Si la API de inventario no responde, activar modo degradado y permitir la compra con advertencia.
- Registrar cada validación en la colección stock_validations para auditoría, con los campos: timestamp, sku, requested, available, userId. TTL de 7 días.

---

## Nuevos servicios

- Nuevo endpoint en Catalog Service:
  - **POST /v1/catalog/validate-stock**
    - **Request:**  
      `{ items: [{ sku, quantity }] }`
    - **Response:**  
      `{ items: [{ sku, available: bool, currentStock: number }] }`
- Integración con API de inventario (REST).

---

## Partes Afectadas

---

### Dependencias con terceros

- Dependencia con la API de inventario (legacy) para la validación de stock en tiempo real.

---

### Contingencias

- Implementar circuit breaker para la API de inventario.
- Implementar modo degradado: si la API de inventario no responde, permitir la compra mostrando advertencia al usuario.

---