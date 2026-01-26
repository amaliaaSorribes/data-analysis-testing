# Notas reunión – problema autenticación y sesión de usuarios

Fecha: 2026-01-26  
Asistentes: Producto, Tech Lead, Frontend, Backend, UX  
Tema: Usuarios pierden sesión y carrito al entrar a la web

---

- Soporte reporta quejas frecuentes sobre problemas de login
- Los usuarios tienen que autenticarse varias veces
- Pierden su carrito al hacer login
- La sesión se pierde constantemente
- En algunos casos no pueden acceder con credenciales válidas

---

## Situación actual

- Sistema de autenticación separado del sistema de carritos
- Cuando usuario hace login:
  - se genera token de sesión
  - se almacena en frontend
  - pero carrito tiene solo `cartId`, sin `userId`
- No hay lógica que vincule sesión con carrito
- Token JWT solo contiene `userId`
- Si usuario guest hace login → pierde su carrito

---

## Problema técnico identificado

- Usuario puede tener carrito como guest
- Luego hace login
- Sistema no sabe qué hacer con el carrito previo
- Actualmente lo pierde
- Genera frustración y abandono

---

## Solución propuesta

- Crear endpoint unificado POST /v1/auth/login
- Además de validar credenciales, gestiona asociación del carrito
- Flujo:
  1. valida credenciales
  2. verifica si hay cartId en request (guest)
  3. si existe, asocia carrito al userId
  4. si usuario ya tenía carrito activo: reemplazar
  5. devuelve token + cartId vinculado

---

## Cambios técnicos necesarios

- Nuevo endpoint: POST /v1/auth/login
- Nuevo endpoint: GET /v1/carts/user/{userId}
- Modificar colección carts:
  - añadir campo `userId` (opcional)
  - añadir índice: { userId: 1, status: 1 }
  - añadir campo `lastAccessedAt`
- Modificar POST /v1/carts para aceptar userId opcional
- Lógica: si login con cartId guest → asociar a userId
- Si usuario ya tenía carrito → reemplazar (no merge por ahora)

---

## Persistencia mejorada

- Al asociar carrito a userId → persiste en BD
- Usuario puede cerrar app / cambiar dispositivo
- Al hacer login recupera su carrito con GET /v1/carts/user/{userId}
- Carrito guardado hasta TTL o conversión a pedido

---

## Otras consideraciones

- TTL para usuarios logueados: 30 días (vs 24h para guests)
- Seguridad: GET /v1/carts/user/{userId} solo accesible por propio usuario
- Validar token JWT y verificar userId
- Endpoints de gestión de items no cambian
- Usuarios guest siguen funcionando igual
- Merge de carritos se deja para US futura

---

## Comentarios UX

- Mejoraría conversión significativamente
- Usuarios podrían añadir desde móvil y completar desde desktop
- Considerar banner/tooltip incentivando login para "guardar carrito"

---

## Decisiones finales

- Implementar asociación carrito-usuario en login
- Mantener lógica simple: reemplazar, no merge
- Actualizar documentación técnica
- Crear US con este alcance
