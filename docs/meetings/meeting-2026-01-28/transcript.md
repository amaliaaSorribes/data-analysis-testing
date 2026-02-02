# Transcript - Reunión de Producto
**Fecha:** 2026-01-28  
**Participantes:** Product Manager, Tech Lead, Frontend Developer  

---

## Contexto

Los usuarios están pidiendo poder guardar productos para comprar más adelante sin añadirlos al carrito. Necesitamos implementar un sistema de wishlist o lista de deseos.

## Discusión

**Product Manager:**  
Los datos muestran que muchos usuarios vuelven a buscar los mismos productos varias veces antes de comprarlos. Una wishlist les permitiría guardar productos de interés sin compromiso de compra inmediata.

**Tech Lead:**  
Entiendo. Básicamente necesitamos permitir que los usuarios:
1. Añadan productos a una wishlist
2. Vean su lista de productos guardados
3. Muevan productos de wishlist al carrito fácilmente
4. Eliminen productos de la wishlist

**Frontend Developer:**  
¿Los usuarios pueden tener múltiples wishlists o solo una?

**Product Manager:**  
Para la primera versión, una sola wishlist por usuario es suficiente. Podemos evaluar múltiples listas en el futuro según el feedback.

**Tech Lead:**  
De acuerdo. A nivel técnico necesitaríamos:

### Endpoints nuevos:
- **POST /wishlist/items** - Añadir producto a wishlist
- **GET /wishlist** - Obtener wishlist del usuario
- **DELETE /wishlist/items/{productId}** - Eliminar producto de wishlist
- **POST /wishlist/move-to-cart** - Mover uno o todos los items al carrito

### Modelo de datos MongoDB:
```json
{
  "userId": "string",
  "items": [
    {
      "productId": "string",
      "addedAt": "timestamp",
      "notifyOnDiscount": boolean,
      "notifyOnStock": boolean
    }
  ],
  "createdAt": "timestamp",
  "lastModified": "timestamp"
}
```

### Reglas de negocio:
1. Máximo 100 productos en wishlist
2. Notificar al usuario si producto tiene descuento
3. Notificar si producto agotado vuelve a tener stock
4. Los precios se consultan en tiempo real al mostrar wishlist
5. Productos descatalogados se marcan pero no se eliminan automáticamente

**Frontend Developer:**  
¿Mostramos la wishlist en todas partes o solo en una sección dedicada?

**Product Manager:**  
Sección dedicada accesible desde el menú principal. También un botón "Añadir a wishlist" en cada página de producto.

**Tech Lead:**  
Para las notificaciones necesitaríamos:
- Evento cuando precio baja más de 10%
- Evento cuando producto vuelve a estar disponible
- Email o notificación push según preferencias del usuario

**Product Manager:**  
Perfecto. También necesitamos mostrar si un producto ya está en la wishlist para evitar duplicados.

## Decisiones finales

1. Implementar sistema de wishlist con una lista por usuario
2. Límite de 100 productos
3. Notificaciones de descuentos y disponibilidad
4. Integración visual en páginas de producto
5. Opción de mover items al carrito directamente

## Próximos pasos

- Crear User Story en backlog
- Diseñar UI de la wishlist
- Implementar sistema de notificaciones
- Definir endpoints y modelo de datos
