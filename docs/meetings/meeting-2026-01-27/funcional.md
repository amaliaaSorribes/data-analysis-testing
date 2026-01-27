# Documento funcional – Corrección cálculo de descuentos combinados (2026-01-27)

## Descripción General

Corrección del cálculo de descuentos combinados en el sistema de promociones. Actualmente, la aplicación secuencial y sin prioridad de los descuentos genera pérdidas económicas y descuentos mayores a los previstos. Se busca refactorizar la lógica para aplicar correctamente los descuentos compuestos, establecer un orden de prioridad y validar un descuento máximo permitido.

---

## Lógica Funcional

- Refactorizar la lógica de cálculo de descuentos para aplicar descuentos combinados correctamente.
- Ordenar las promociones por prioridad antes de su aplicación.
- Aplicar cada descuento sobre el precio resultante del descuento anterior.
- Utilizar la fórmula: `precio_final = precio * (1 - d1) * (1 - d2) ...`
- Validar que el descuento total no supere el 80%.
- Registrar logs detallados de cada aplicación de descuento.
- Proveer un desglose completo de los descuentos aplicados.
- Prioridad de aplicación: automática > manual > cupón.
- Alertar si el descuento supera el 70%.
- Dashboard para marketing para revisar casos.
- Audit log completo de los cálculos.

---

## Lógica Backend

- Modificar el Promotion Engine para:
  - Ordenar promociones por prioridad.
  - Aplicar descuentos secuencialmente sobre el precio actualizado.
  - Implementar la fórmula correcta para descuentos compuestos.
  - Validar que el descuento total sea menor al 80%.
  - Estructura de cálculo:
    - `promotions: [{ type, value, priority, appliedPrice }]`
    - `originalPrice: number`
    - `finalPrice: number`
    - `totalDiscount: percentage`
- Implementar logs detallados de cada paso del cálculo.
- Generar alertas si el descuento supera el 70%.
- Endpoint de validación:
  - `POST /v1/promotions/calculate-preview`
  - La respuesta debe incluir el desglose completo de descuentos aplicados.

---

## Nuevos servicios

- Endpoint de validación de promociones:
  - **URL:** `/v1/promotions/calculate-preview`
  - **Método:** POST
  - **Request:** Información de promociones aplicables y precio original.
  - **Response:** Desglose completo de descuentos aplicados, precio final, totalDiscount.

---

## Partes Afectadas

*(No hay información explícita sobre sites afectados, dependencias con terceros, analítica, contingencias, tipo de usuario, método de envío, tipo de mercancía ni ventanas de flujo afectadas en el transcript, por lo que estas secciones se eliminan.)*