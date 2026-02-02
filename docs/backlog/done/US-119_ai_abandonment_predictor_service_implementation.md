```markdown
# US-119 - AI Abandonment Predictor Service Implementation

---

## Identificación

- **ID:** US-119
- **Fecha:** 2025-02-18
- **Servicio:** AI Abandonment Predictor Service

---

## User Story

Como **propietario de e-commerce** quiero **predecir y reducir el abandono de carritos en tiempo real** para **incrementar la conversión y optimizar las ventas**.

---

## Descripción

Se requiere implementar un servicio de predicción de abandono de carritos basado en inteligencia artificial. El sistema debe analizar eventos de comportamiento del usuario en tiempo real y asignar un "abandonment score" (0.0-1.0). Según el score y la razón predicha del abandono, se activarán intervenciones personalizadas como descuentos dinámicos, envío gratuito, pruebas sociales o mensajes de urgencia. Estas intervenciones estarán sujetas a reglas de negocio específicas, como un máximo de una intervención por sesión y un límite de descuento del 15%. Además, el modelo de machine learning deberá reentrenarse semanalmente con nuevos datos.

---

## Cambios

### Qué se añadió

- Creación de un nuevo servicio llamado **AI Abandonment Predictor Service**.
- Implementación de un modelo de machine learning para calcular el "abandonment score" y predecir razones de abandono.
- Activación de intervenciones personalizadas basadas en el score y la razón predicha.
- Reglas de negocio para limitar las intervenciones y optimizar su efectividad.
- Reentrenamiento semanal del modelo con datos actualizados.

---

## Impacto en APIs

### Nuevo endpoint

1. **POST /ai/abandonment/track**  
   Registrar eventos de comportamiento del usuario en tiempo real.

2. **GET /ai/abandonment/score/{userId}**  
   Obtener el abandono predicho y la razón más probable.

3. **POST /ai/abandonment/intervene**  
   Disparar una intervención personalizada para reducir el abandono.

4. **GET /ai/abandonment/insights/{userId}**  
   Consultar razones predichas de abandono y recomendaciones de intervención.
```

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-31/funcional.md)
