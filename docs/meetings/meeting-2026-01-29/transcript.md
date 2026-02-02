# Transcript - Reunión de Producto
**Fecha:** 2026-01-29  
**Participantes:** Product Manager, Tech Lead, Marketing Manager, Backend Developer  

---

## Contexto

Marketing quiere implementar un programa de puntos de fidelidad donde los usuarios ganen puntos por compras y puedan canjearlos por descuentos.

## Discusión

**Marketing Manager:**  
Un programa de puntos aumentaría la retención de clientes. Por cada euro gastado, el usuario ganaría 1 punto. Cada 100 puntos equivaldrían a 1 euro de descuento.

**Product Manager:**  
Me gusta. ¿Los puntos se aplican automáticamente o el usuario decide cuándo usarlos?

**Marketing Manager:**  
El usuario decide cuándo canjearlos. Deben tener la opción de aplicar puntos durante el checkout.

**Tech Lead:**  
Necesitaríamos un servicio de loyalty points. Los puntos se calcularían y otorgarían después de confirmar la compra.

### Endpoints nuevos:
- **GET /loyalty/balance** - Consultar balance de puntos
- **GET /loyalty/history** - Historial de puntos ganados/canjeados
- **POST /loyalty/redeem** - Canjear puntos por descuento
- **GET /loyalty/redemption-value** - Calcular valor de canje

### Modelo de datos:
```json
{
  "userId": "string",
  "totalPoints": number,
  "availablePoints": number,
  "pointsHistory": [
    {
      "transactionId": "string",
      "type": "earned|redeemed|expired",
      "points": number,
      "description": "string",
      "date": "timestamp"
    }
  ],
  "tier": "bronze|silver|gold",
  "tierSince": "timestamp"
}
```

**Backend Developer:**  
¿Los puntos caducan?

**Marketing Manager:**  
Sí, después de 12 meses. También queremos niveles: Bronze (0-999 puntos), Silver (1000-4999), Gold (5000+). Cada nivel da diferentes beneficios.

**Product Manager:**  
¿Qué beneficios específicos?
- Bronze: 1 punto por euro
- Silver: 1.5 puntos por euro
- Gold: 2 puntos por euro + envío gratis

**Tech Lead:**  
Para el checkout necesitaríamos:
- Mostrar puntos disponibles
- Permitir aplicar puntos como descuento
- Validar que tenga suficientes puntos
- Actualizar balance después de la compra

### Reglas de negocio:
1. 1 punto por euro gastado (varía según tier)
2. 100 puntos = 1 euro descuento
3. Mínimo 500 puntos para canjear
4. Puntos caducan a los 12 meses
5. Puntos se otorgan solo después de completar la compra
6. No se pueden canjear puntos en productos ya con descuento superior al 50%

**Marketing Manager:**  
También queremos eventos especiales donde se ganen puntos extra. Por ejemplo, doble puntos en Black Friday.

**Tech Lead:**  
Añadimos:
- **POST /loyalty/events/multiplier** - Configurar multiplicador temporal (admin)
- Campo `multiplierActive` en el cálculo de puntos

## Decisiones finales

1. Implementar Loyalty Points Service
2. 3 tiers: Bronze, Silver, Gold
3. Puntos caducan en 12 meses
4. Mínimo 500 puntos para canjear
5. Sistema de multiplicadores para eventos especiales
6. Integración en checkout para aplicar descuentos

## Próximos pasos

- Crear User Story en backlog
- Diseñar UI de puntos en checkout
- Implementar sistema de tiers
- Configurar reglas de caducidad
