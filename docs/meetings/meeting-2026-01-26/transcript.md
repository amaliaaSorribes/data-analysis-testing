# Notas reunión – error inconsistencia precios en checkout

Fecha: 2026-01-26  
Asistentes: Producto, Soporte, Tech Lead, Backend, QA  
Tema: Usuarios ven un precio en catálogo pero se cobra otro en checkout

---

- Soporte reporta 8 tickets esta semana sobre precios incorrectos
- Usuario ve precio X en pantalla de producto
- Al llegar a checkout → precio diferente (generalmente más alto)
- Genera desconfianza y abandono
- Algunos usuarios reclaman por email

---

## Situación actual

- Pricing Ingestion Service recibe actualizaciones de precios
- Guarda en colección `prices` de MongoDB
- Pricing Service consulta esa colección al calcular totales
- Pero frontend cachea precios del catálogo
- No hay re-validación de precios al añadir al carrito

---

## Problema identificado

- Hay una ventana temporal donde precios están desincronizados
- Ejemplo:
  1. Usuario entra a producto → ve precio 19.99€
  2. Mientras navega → llega actualización de precio a 24.99€
  3. Usuario añade al carrito → sigue mostrando 19.99€
  4. Al hacer checkout → calcula con precio nuevo 24.99€
  5. Diferencia genera confusión

---

## Casos específicos reportados

- Producto en oferta termina oferta mientras está en carrito
- Precios cambian por cambio de moneda
- Errores de redondeo entre catálogo y pricing
- Cache del frontend desactualizado

---

## Impacto

- Confianza del usuario baja
- Tasa de abandono en checkout: +12%
- Reclamaciones de soporte
- Pérdida de ventas

---

## Solución propuesta

- Re-validar precios en tiempo real al añadir producto al carrito
- Nuevo endpoint: POST /v1/pricing/validate
- Consulta precio actual del SKU antes de añadir
- Si precio cambió → notificar al usuario
- Usuario decide si continuar o no

---

## Cambios técnicos necesarios

- Nuevo endpoint en Pricing Service:
  - POST /v1/pricing/validate
  - Request: { items: [{ sku, quantity }] }
  - Response: { items: [{ sku, currentPrice, currency }] }
- Modificar Cart Service:
  - Antes de añadir item → llamar a pricing/validate
  - Comparar precio recibido vs precio del frontend
  - Si difieren: devolver warning
- Añadir campo en response de add-to-cart:
  - priceChanged: boolean
  - oldPrice: number
  - newPrice: number

---

## Flujo propuesto

1. Usuario click "añadir al carrito"
2. Frontend envía: POST /v1/carts/{cartId}/items con precio mostrado
3. Cart Service llama a POST /v1/pricing/validate
4. Si precio coincide → añade normalmente
5. Si precio cambió → devuelve status 200 con flag priceChanged: true
6. Frontend muestra modal: "El precio cambió de X a Y, ¿continuar?"
7. Usuario acepta → segundo request confirmando
8. Usuario rechaza → cancela operación

---

## Consideraciones

- No bloquear operación, solo informar
- Cache de precios validados: 10 segundos (Redis)
- Si pricing service no responde → permitir añadir con warning genérico
- Logs de todas las diferencias de precio para análisis

---

## Modelo de datos

- Nueva colección: price_validations
  - timestamp
  - sku
  - frontendPrice
  - actualPrice
  - action: added / rejected
  - userId (opcional)
- TTL: 30 días
- Para analytics y detección de problemas

---

## Alternativas descartadas

- Invalidar cache del frontend cada minuto → demasiado agresivo
- Bloquear añadir al carrito si precio cambió → mala UX
- No hacer nada → problema persiste

---

## Decisiones finales

- Implementar validación de precios en add-to-cart
- Nuevo endpoint en pricing service
- Informar al usuario de cambios, no bloquear
- Registrar validaciones para análisis
- Timeout de 3 segundos en validación
