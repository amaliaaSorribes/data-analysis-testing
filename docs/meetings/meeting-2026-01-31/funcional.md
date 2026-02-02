```markdown
# Documento Funcional - AI Abandonment Predictor Service (2025-02-18)

## Descripción General

Implementación de un servicio de predicción de abandono de carrito utilizando inteligencia artificial. El sistema asignará un "abandonment score" en tiempo real y activará intervenciones personalizadas para reducir el abandono de carritos.

---

## Lógica Funcional

El sistema se basa en un modelo de machine learning que analiza eventos de comportamiento del usuario en tiempo real. Los principales indicadores de abandono incluyen:
- Tiempo inactivo en página de checkout (>2 minutos)
- Múltiples intentos de aplicar código de descuento
- Varias modificaciones de cantidad en corto tiempo
- Comparación de precios (abrir múltiples tabs)
- Abandono previo en sesiones anteriores
- Precio total superior a su ticket promedio

El modelo asignará un score de abandono (0.0-1.0) y predirá la razón más probable del abandono. Según el motivo identificado, se activarán intervenciones específicas:
- Precio alto: ofrecer descuento dinámico o plan de pagos
- Envío caro: ofrecer envío gratis con código
- Indecisión: mostrar reviews positivas o "últimas unidades"
- Comparación de precios: garantía de mejor precio

Reglas de negocio:
1. Score > 0.7 = riesgo alto de abandono
2. Máximo una intervención por sesión
3. Descuentos dinámicos máximo 15%
4. No intervenir si usuario ya tiene descuento aplicado
5. A/B testing de intervenciones
6. Reentrenar modelo semanalmente con nuevos datos

---

## Lógica Backend

### Arquitectura técnica:
- **Nuevo servicio:** AI Abandonment Predictor Service

### Endpoints:
- **POST /ai/abandonment/track** - Registrar evento de comportamiento
- **GET /ai/abandonment/score/{userId}** - Obtener score actual
- **POST /ai/abandonment/intervene** - Disparar intervención
- **GET /ai/abandonment/insights/{userId}** - Razones predichas de abandono

### Pipeline de ML:
```
User Behavior Events → Feature Engineering → ML Model → 
Abandonment Score + Reason → Intervention Trigger → 
Action (discount/notification/UI change)
```

### Modelo de datos:
```json
{
  "userId": "string",
  "sessionId": "string",
  "abandonmentScore": 0.0-1.0,
  "predictedReason": "price|shipping|indecision|comparison|payment_issues",
  "confidence": 0.0-1.0,
  "behaviors": [
    {
      "type": "page_view|scroll|hover|click|idle",
      "timestamp": "timestamp",
      "context": {...}
    }
  ],
  "recommendedIntervention": {
    "type": "discount|free_shipping|social_proof|urgency",
    "parameters": {...}
  },
  "interventionApplied": boolean,
  "outcome": "completed|abandoned|pending"
}
```

---

## Nuevos servicios

### AI Abandonment Predictor Service

**Endpoints:**
- **POST /ai/abandonment/track**  
  **Request:**  
  ```json
  {
    "userId": "string",
    "sessionId": "string",
    "eventType": "page_view|scroll|hover|click|idle",
    "timestamp": "timestamp",
    "context": {...}
  }
  ```
  **Response:**  
  ```json
  {
    "status": "success"
  }
  ```

- **GET /ai/abandonment/score/{userId}**  
  **Response:**  
  ```json
  {
    "abandonmentScore": 0.0-1.0,
    "predictedReason": "price|shipping|indecision|comparison|payment_issues",
    "confidence": 0.0-1.0
  }
  ```

- **POST /ai/abandonment/intervene**  
  **Request:**  
  ```json
  {
    "userId": "string",
    "sessionId": "string",
    "interventionType": "discount|free_shipping|social_proof|urgency",
    "parameters": {...}
  }
  ```
  **Response:**  
  ```json
  {
    "status": "success",
    "interventionApplied": true
  }
  ```

- **GET /ai/abandonment/insights/{userId}**  
  **Response:**  
  ```json
  {
    "predictedReason": "price|shipping|indecision|comparison|payment_issues",
    "confidence": 0.0-1.0,
    "recommendedIntervention": {
      "type": "discount|free_shipping|social_proof|urgency",
      "parameters": {...}
    }
  }
  ```

---

## Analítica

Se desarrollará un dashboard de métricas que incluirá:
- Tasa de abandono predicha vs real
- Efectividad de cada tipo de intervención
- ROI de las intervenciones (descuentos dados vs ventas salvadas)
- Evolución del score durante la sesión

---

## Próximos pasos

1. Crear User Story en backlog.
2. Preparar dataset de entrenamiento.
3. Diseñar feature engineering pipeline.
4. Implementar tracking de eventos.
5. Crear dashboard de métricas.
6. Definir intervenciones y sus reglas.
```