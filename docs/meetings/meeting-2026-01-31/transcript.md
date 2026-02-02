# Transcript - Reunión de Producto
**Fecha:** 2026-01-31  
**Participantes:** Product Manager, Tech Lead, Data Scientist, ML Engineer  

---

## Contexto

El equipo de data science propone usar IA para predecir qué usuarios están a punto de abandonar el carrito y tomar acciones proactivas.

## Discusión

**Data Scientist:**  
Analizando los datos, hemos identificado patrones que predicen con 85% de precisión cuándo un usuario va a abandonar el carrito. Podríamos intervenir antes de que lo hagan.

**Product Manager:**  
Interesante. ¿Qué patrones son esos?

**Data Scientist:**  
Principales indicadores:
- Tiempo inactivo en página de checkout (>2 minutos)
- Múltiples intentos de aplicar código de descuento
- Varias modificaciones de cantidad en corto tiempo
- Comparación de precios (abrir múltiples tabs)
- Abandono previo en sesiones anteriores
- Precio total superior a su ticket promedio

**ML Engineer:**  
Podemos crear un modelo de ML que asigne un "abandonment score" en tiempo real. Cuando supere cierto umbral, activamos intervenciones.

**Tech Lead:**  
¿Qué tipo de intervenciones?

**Product Manager:**  
Basado en el motivo predicho:
- Si es precio alto: ofrecer descuento dinámico o plan de pagos
- Si es envío caro: ofrecer envío gratis con código
- Si es indecisión: mostrar reviews positivas o "últimas unidades"
- Si es comparación de precios: garantía de mejor precio

**Data Scientist:**  
Exacto. El modelo también identificaría la razón más probable del abandono para personalizar la intervención.

**Tech Lead:**  
Arquitectura técnica:

### Nuevo servicio:
- **AI Abandonment Predictor Service**

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

### Reglas de negocio:
1. Score > 0.7 = riesgo alto de abandono
2. Máximo una intervención por sesión
3. Descuentos dinámicos máximo 15%
4. No intervenir si usuario ya tiene descuento aplicado
5. A/B testing de intervenciones
6. Reentrenar modelo semanalmente con nuevos datos

**ML Engineer:**  
Necesitaríamos trackear eventos en tiempo real:
- Mouse movement y scroll behavior
- Tiempo en cada campo del checkout
- Clics en botón "atrás"
- Cambios de tab del navegador
- Interacciones con calculadora de envío

**Product Manager:**  
¿Esto no es demasiado invasivo para la privacidad?

**Tech Lead:**  
Todo se procesa de forma anónima y agregada. No guardamos información personal identificable en el modelo. GDPR compliant.

**Data Scientist:**  
También queremos dashboard de analytics:
- Tasa de abandono predicha vs real
- Efectividad de cada tipo de intervención
- ROI de las intervenciones (descuentos dados vs ventas salvadas)
- Evolución del score durante la sesión

**Product Manager:**  
¿Cuánto tiempo para entrenar el modelo inicial?

**ML Engineer:**  
Con los datos históricos de los últimos 3 meses, 2 semanas para:
- Feature engineering
- Entrenar modelo
- Validar precisión
- Implementar en producción

## Decisiones finales

1. Implementar AI Abandonment Predictor Service
2. Score de abandono en tiempo real (0-1)
3. Intervenciones personalizadas según razón predicha
4. Máximo una intervención por sesión
5. A/B testing para medir efectividad
6. Dashboard de analytics y métricas
7. Reentrenamiento semanal del modelo
8. Privacy-first approach (GDPR compliant)

## Próximos pasos

- Crear User Story en backlog
- Preparar dataset de entrenamiento
- Diseñar feature engineering pipeline
- Implementar tracking de eventos
- Crear dashboard de métricas
- Definir intervenciones y sus reglas
