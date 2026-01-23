# Documento funcional – Mejora mensajes de error en checkout (2025-03-05)

## Descripción General

Se busca mejorar los mensajes de error que aparecen en el checkout, ya que actualmente son genéricos y no informan al usuario del motivo del fallo. El objetivo es mostrar mensajes más claros y específicos para reducir el abandono y mejorar la experiencia de usuario.

- **HU:**  
- **Figma:**  

---

## Lógica Funcional

Cuando ocurra un error en el checkout, se debe mostrar un mensaje específico según el motivo del fallo. Se diferenciarán al menos los siguientes casos:

- Error de pago
- Falta de stock
- Error técnico genérico

Los mensajes deben ser simples y entendibles, sin mostrar detalles técnicos al usuario.

---

## Partes Afectadas

### Determinar ventanas de flujo afectadas

Afecta únicamente al checkout.

---