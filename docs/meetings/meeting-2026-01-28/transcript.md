# Transcript - Reunión 28 Enero 2026

**Fecha:** 2026-01-28  
**Participantes:** Product Owner, Tech Lead, Backend Dev

---

## Contexto

El equipo de marketing ha solicitado poder aplicar códigos de descuento apilables en el carrito. Actualmente solo se puede aplicar un código promocional a la vez.

---

## Requerimientos discutidos

### Propuesta inicial

**Product Owner:**  
"Marketing quiere que los usuarios puedan aplicar múltiples códigos promocionales en una misma compra. Por ejemplo, un código de bienvenida + un código de fidelización."

**Tech Lead:**  
"Eso complicaría mucho la lógica de precios y promociones. Tendríamos que recalcular todo cada vez y manejar conflictos entre códigos."

**Backend Dev:**  
"Además, podría haber abusos. Si permitimos apilar códigos sin límite, los usuarios podrían obtener descuentos superiores al 100%."

### Decisión

**Product Owner:**  
"Entiendo los riesgos técnicos. Después de pensarlo, vamos a mantener la limitación de un solo código promocional por compra."

**Tech Lead:**  
"Mejor. Eso mantiene la lógica simple y predecible."

**Backend Dev:**  
"De acuerdo. No implementaremos códigos apilables."

---

## Conclusión

❌ **Se rechaza la funcionalidad de códigos promocionales apilables**

Razones:
- Complejidad técnica alta
- Riesgo de abusos
- Impacto en rendimiento del cálculo de precios
- Marketing acepta la limitación actual

No se requiere ningún desarrollo en este momento.
