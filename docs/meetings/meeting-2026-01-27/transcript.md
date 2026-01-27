# Notas reunión – errores en cálculo de descuentos combinados

Fecha: 2026-01-27  
Asistentes: Producto, Backend, Marketing, QA  
Tema: Descuentos combinados se calculan incorrectamente generando pérdidas

---

- Marketing detecta descuentos mayores a los esperados
- Combinación de promociones genera cálculos erróneos
- Descuento sobre descuento no se aplica correctamente
- Pérdida económica estimada: 12.000€ este mes
- 8 casos reportados con evidencia

---

## Situación actual

- Promotion Engine aplica descuentos secuencialmente
- No hay orden de prioridad definido
- Descuentos se aplican sobre precio ya descontado
- Ejemplo: 20% + 10% debería ser 28% pero sistema aplica 30%
- No hay validación de descuento máximo permitido

---

## Problema identificado

- Cálculo incorrecto de descuentos combinados
- Ejemplo:
  1. Producto: 100€
  2. Descuento 1: 20% → 80€
  3. Descuento 2: 10% sobre 80€ → 72€
  4. Descuento real: 28% (correcto)
  5. Sistema actual: aplica 30% directo → 70€
  6. Pérdida: 2€ por producto

---

## Casos específicos reportados

- Black Friday: 20% + 10% cupón → descuento excesivo
- Productos en oferta + código de bienvenida
- Descuento por cantidad + promoción de categoría
- Miembros premium + cupón de temporada

---

## Impacto

- Pérdida económica: 12.000€ este mes
- Margen de productos comprometido
- Marketing no puede planificar campañas
- Riesgo de abuso por usuarios informados
- Clientes esperan descuentos incorrectos en futuro

---

## Solución propuesta

- Refactorizar lógica de cálculo de descuentos
- Aplicar descuentos en orden de prioridad correcto
- Calcular descuento compuesto correctamente
- Validar descuento total máximo
- Logs detallados de cada aplicación

---

## Cambios técnicos necesarios

- Modificar Promotion Engine:
  - Ordenar promociones por prioridad
  - Aplicar descuentos secuencialmente sobre precio actualizado
  - Fórmula correcta: precio_final = precio * (1 - d1) * (1 - d2)
  - Validar descuento total < 80%
- Nueva estructura de cálculo:
  - promotions: [{ type, value, priority, appliedPrice }]
  - originalPrice: number
  - finalPrice: number
  - totalDiscount: percentage
- Endpoint de validación:
  - POST /v1/promotions/calculate-preview
  - Response: desglose completo de descuentos aplicados

---

## Flujo propuesto

1. Usuario tiene promociones aplicables
2. Sistema ordena por prioridad
3. Aplica descuento 1 sobre precio original
4. Aplica descuento 2 sobre precio resultante
5. Aplica descuento N sobre precio N-1
6. Valida descuento total < máximo permitido
7. Guarda log de cada paso
8. Devuelve desglose detallado al frontend

---

## Consideraciones

- Prioridad: automática > manual > cupón
- Descuento máximo global: 80%
- Audit log completo de cálculos
- Dashboard para marketing revisar casos
- Alertas si descuento > 70%
