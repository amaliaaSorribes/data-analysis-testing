# Notas reunión – Mejora mensajes de error en checkout

Fecha: 2025-03-05  
Asistentes: Producto, Negocio, Soporte, Tech Lead  
Tema: Mensajes de error poco claros en checkout

---

- Soporte comenta que hay bastantes tickets por errores en checkout
- Los usuarios no entienden por qué no pueden continuar
- Aparece un mensaje genérico tipo “Ha ocurrido un error”
- Negocio dice que esto genera abandono en el último paso

---

## Situación actual

- Cuando falla algo en checkout:
  - pago rechazado
  - producto sin stock
  - error de validación
- El mensaje es siempre el mismo
- No se distingue el motivo

---

## Comentarios de negocio

- El usuario debería saber qué ha pasado
- En otros e-commerce el mensaje es más claro
- Esto impacta directamente en conversión
- Especialmente importante en mobile

---

## Decisiones tomadas

- Mostrar mensajes de error más específicos
- Diferenciar al menos:
  - error de pago
  - falta de stock
  - error técnico genérico
- Mantener el mensaje simple y entendible
- No mostrar mensajes técnicos al usuario

---

## Alcance

- Solo afecta a checkout
- No se cambia la lógica de negocio
- Es solo cambio de mensajes

---

## Comentarios finales

- No hace falta entrar en detalle técnico ahora
- Que producto defina los textos
- Crear una US para este cambio
