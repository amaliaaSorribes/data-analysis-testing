# Documento funcional – Mejora mensajes de error en checkout (2025-03-05)

## Descripción General

Se busca mejorar la claridad de los mensajes de error que se muestran a los usuarios en el proceso de checkout. Actualmente, todos los errores muestran un mensaje genérico, lo que genera confusión y abandono en el último paso. El objetivo es mostrar mensajes de error más específicos y entendibles para el usuario, diferenciando al menos entre error de pago, falta de stock y error técnico genérico. El cambio solo afecta a los mensajes mostrados en checkout, sin modificar la lógica de negocio.

- **HU:**  
- **Figma:**  

---

## Lógica Funcional

- Mostrar mensajes de error más específicos en el checkout.
- Diferenciar al menos entre:
  - Error de pago.
  - Falta de stock.
  - Error técnico genérico.
- Mantener los mensajes simples y entendibles.
- No mostrar mensajes técnicos al usuario.
- El cambio es únicamente en los mensajes, no en la lógica de negocio.

---

## Partes Afectadas

### Site afectados

Solo afecta al checkout.

---

## Determinar ventanas de flujo afectadas

Afecta a todo el flujo de checkout.