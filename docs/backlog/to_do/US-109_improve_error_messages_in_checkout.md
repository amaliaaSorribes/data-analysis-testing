# US-109 - Improve error messages in checkout

---

## Identificación

- **ID:** US-109
- **Fecha:** 2025-03-05
- **Servicio:** cart-service

---

## User Story

Como usuario del checkout quiero recibir mensajes de error claros y específicos para entender mejor el motivo del fallo y poder actuar en consecuencia.

---

## Descripción

Actualmente, los mensajes de error en el checkout son genéricos y no ayudan al usuario a identificar la causa del problema. Se propone mejorar la experiencia mostrando mensajes de error diferenciados según el tipo de fallo: error de pago, falta de stock o error técnico genérico. Los mensajes deben ser simples, entendibles y no incluir detalles técnicos. Este cambio solo afecta a los textos mostrados, sin modificar la lógica de negocio.

---

## Cambios

### Qué se añadió

- Mensajes de error específicos y claros en el checkout para los siguientes casos:
  - Error de pago.
  - Falta de stock.
  - Error técnico genérico.

---

## Impacto en APIs

### Nuevo endpoint

No aplica. No se agregan nuevos endpoints; el cambio es solo en los mensajes mostrados al usuario en el checkout.

    ---

    ## Referencias

    - Documento funcional: [`funcional.md`](../../docs/meetings\meeting-2025-03-05\funcional.md)
    