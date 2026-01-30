# US-114 - Combined Discount Calculation Correction

---

## Identificación

- **ID:** US-114
- **Fecha:** 2026-01-27
- **Servicio:** cart-service

---

## User Story

Como usuario del sistema de promociones quiero que los descuentos combinados se apliquen correctamente, respetando prioridades y límites, para evitar pérdidas económicas y asegurar que los descuentos no excedan lo permitido.

---

## Descripción

Se requiere refactorizar la lógica de cálculo de descuentos en el Promotion Engine para que los descuentos combinados se apliquen de manera secuencial y en el orden de prioridad definido (automática > manual > cupón). Cada descuento debe aplicarse sobre el precio resultante del descuento anterior utilizando la fórmula compuesta (`precio_final = precio * (1 - d1) * (1 - d2) ...`). Además, se debe validar que el descuento total no supere el 80%, generar alertas si se supera el 70%, registrar logs detallados de cada paso y proveer un desglose completo de los descuentos aplicados. Se debe exponer un endpoint que permita validar y obtener el desglose de descuentos antes de aplicar la promoción.

---

## Cambios

### Qué se añadió

- Refactorización de la lógica de cálculo de descuentos combinados en el Promotion Engine.
- Orden de prioridad en la aplicación de promociones.
- Aplicación secuencial de descuentos sobre el precio actualizado.
- Validación de límite máximo de descuento total (80%).
- Generación de alertas si el descuento supera el 70%.
- Registro de logs detallados y audit log completo de los cálculos.
- Desglose completo de descuentos aplicados en la respuesta.
- Dashboard para marketing para revisar casos.

---

## Impacto en APIs

### Nuevo endpoint

- **POST** `/v1/promotions/calculate-preview`
  - **Request:** Información de promociones aplicables y precio original.
  - **Response:** Desglose completo de descuentos aplicados, precio final, totalDiscount.

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-27/funcional.md)
