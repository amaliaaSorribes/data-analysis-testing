# Notas reunión – problema sincronización de stock en catálogo

Fecha: 2026-01-26  
Asistentes: Producto, Negocio, Tech Lead, Backend, Operaciones  
Tema: Inconsistencias entre stock mostrado y stock real

---

- Operaciones reporta problemas recurrentes
- Usuarios compran productos que aparecen disponibles
- Al procesar el pedido → sin stock real
- Tienen que cancelar y reembolsar
- Genera mala experiencia y coste operativo

---

## Situación actual

- Sistema de catálogo recibe actualizaciones de stock vía eventos
- Eventos vienen del sistema de inventario (legacy)
- A veces hay retrasos de hasta 30 minutos
- Frontend muestra stock del catálogo (desactualizado)
- No hay validación en tiempo real al hacer checkout

---

## Problema identificado

- Ingesta de stock es asíncrona
- No hay mecanismo de validación en checkout
- Frontend confía en dato del catálogo sin re-verificar
- Picos de ventas agravan el problema
- Mismo producto vendido varias veces simultáneamente

---

## Impacto en negocio

- 15-20 cancelaciones por semana
- Coste de reembolsos y gestión
- Usuarios frustrados (baja satisfacción)
- Algunos usuarios no vuelven
- Problema especialmente grave en productos limitados / ofertas

---

## Solución propuesta

- Añadir validación de stock en tiempo real durante checkout
- Nuevo endpoint: POST /v1/catalog/validate-stock
- Recibe lista de SKUs + cantidades
- Consulta sistema de inventario directamente (API síncrona)
- Devuelve disponibilidad actualizada por producto

---

## Cambios técnicos

- Nuevo endpoint en Catalog Service:
  - POST /v1/catalog/validate-stock
  - Request: { items: [{ sku, quantity }] }
  - Response: { items: [{ sku, available: bool, currentStock: number }] }
- Integración con API de inventario (REST)
- Timeout configurado: 3 segundos máximo
- Si falla validación → mostrar error claro al usuario

---

## Flujo mejorado

1. Usuario llega a checkout
2. Frontend llama a POST /v1/catalog/validate-stock
3. Backend consulta inventario en tiempo real
4. Si todo OK → permite continuar
5. Si algún producto sin stock → bloquea y notifica

---

## Modelo de datos

- Añadir colección: stock_validations
  - Registrar cada validación para auditoría
  - Campos: timestamp, sku, requested, available, userId
  - TTL: 7 días (solo para troubleshooting)

---

## Consideraciones técnicas

- API de inventario tiene rate limit: 100 req/seg
- Implementar circuit breaker si API cae
- Cache de 30 segundos en validaciones (Redis)
- Si servicio inventario no responde → modo degradado
- Modo degradado: permitir compra con advertencia

---

## Alternativa discutida

- Opción descartada: polling cada 5 min
- Razón: no resuelve el problema real
- Mejor: validación just-in-time

---

## Decisiones finales

- Implementar validación en tiempo real
- Nuevo endpoint en catalog service
- Integración con API de inventario
- Circuit breaker y fallback
- Registrar validaciones para auditoría
- No cambiar lógica de ingesta asíncrona (se mantiene)
