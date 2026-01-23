# US-109 - Improve error messages in checkout

---

## Identificación

- **ID:** US-109
- **Fecha:** 2025-03-05
- **Servicio:** cart-service

---

## User Story

Como usuario del checkout quiero ver mensajes de error claros y específicos cuando ocurre un fallo para entender el motivo y saber cómo proceder.

---

## Descripción

Actualmente, los mensajes de error en el checkout son genéricos y no informan al usuario sobre la causa del fallo. Se propone mostrar mensajes específicos según el motivo del error, diferenciando al menos entre error de pago, falta de stock y error técnico genérico. Los mensajes deben ser simples, claros y no incluir detalles técnicos.

---

## Cambios

### Qué se añadió

- Se añaden mensajes de error específicos en el checkout para los casos de error de pago, falta de stock y error técnico genérico.

---

## Impacto en APIs

### Nuevo endpoint

No aplica (no se especifican nuevos endpoints en el documento funcional).

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings\meeting-2025-03-05\funcional.md)
