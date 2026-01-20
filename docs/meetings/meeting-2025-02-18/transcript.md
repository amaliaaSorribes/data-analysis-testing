# Notas reunión – problema persistencia carrito
 
Fecha: 2025-02-18  
Reunión con socios + dev  
Tema: usuarios pierden el carrito
 
---
 
- Soporte comenta varios tickets recientes
- Usuarios dicen que el carrito desaparece
- Pasa cuando:
  - cierran sesión
  - vuelven otro día
  - cambian de móvil / navegador
 
- Socios:
  - esto genera abandono
  - usuarios esperan que el carrito siga ahí
  - “en otros e-commerce no pasa”
 
- Especialmente mal en mobile
  - la app se cierra
  - se pierde sesión muy fácil
 
---
 
## Cómo funciona ahora (según dev)
 
- carrito se crea sin usuario
- se guarda `cartId` en frontend
- backend no lo asocia a nadie
- si se pierde la sesión → carrito perdido
- no hay forma de recuperarlo
 
---
 
## Ideas de la reunión
 
- asociar carrito al usuario cuando está logueado
- mantener guest carts igual que ahora
- al hacer login:
  - buscar carrito activo del usuario
- duda:
  - qué pasa si hay más de uno
- decisión rápida:
  - uno solo activo
  - no mergear de momento
 
---
 
## Decisiones 
 
- persistir carrito por `userId`
- recuperar carrito al login
- no tocar merge ahora
- hacerlo simple primero
 
---
 
## Comentarios finales
 
- esto debería mejorar conversión
- dejar merge para más adelante
- crear una US nueva para esto
- definir bien el alcance antes de tocar código