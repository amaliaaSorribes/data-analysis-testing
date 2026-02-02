# Transcript - Reunión de Producto
**Fecha:** 2026-01-30  
**Participantes:** Product Manager, Tech Lead, UX Designer, Security Lead  

---

## Contexto

Usuarios empresariales y familias están pidiendo poder compartir carritos entre múltiples usuarios para compras colaborativas.

## Discusión

**Product Manager:**  
Hemos recibido solicitudes de equipos de compras y familias que quieren poder colaborar en un mismo carrito. Por ejemplo, una familia preparando una fiesta o un equipo comprando material de oficina.

**UX Designer:**  
¿Cómo funcionaría? ¿Un usuario crea el carrito y envía un enlace?

**Tech Lead:**  
Propongo dos modos:
1. **Compartir por enlace** - Generar link único que otros puedan usar
2. **Invitar por email** - Invitar usuarios específicos con permisos

**Product Manager:**  
Me gusta. ¿Qué permisos tendrían?
- Owner: puede editar, eliminar, invitar, completar compra
- Editor: puede añadir/eliminar items, cambiar cantidades
- Viewer: solo ver, no editar

**Security Lead:**  
Importante: los enlaces compartidos deben ser seguros, con tokens únicos y posibilidad de revocar acceso en cualquier momento.

**Tech Lead:**  
De acuerdo. Arquitectura propuesta:

### Endpoints nuevos:
- **POST /cart/share/link** - Generar enlace de compartir
- **POST /cart/share/invite** - Invitar usuario por email
- **GET /cart/shared/{token}** - Acceder a carrito compartido
- **DELETE /cart/share/{shareId}** - Revocar acceso
- **GET /cart/shared** - Listar carritos compartidos conmigo
- **PUT /cart/share/{shareId}/permissions** - Cambiar permisos de un usuario

### Modelo de datos:
```json
{
  "cartId": "string",
  "ownerId": "string",
  "sharedWith": [
    {
      "shareId": "uuid",
      "userId": "string",
      "email": "string",
      "permission": "owner|editor|viewer",
      "sharedAt": "timestamp",
      "shareMethod": "link|invite",
      "token": "hashed-token",
      "status": "active|revoked"
    }
  ],
  "shareSettings": {
    "allowLinkSharing": boolean,
    "linkExpiresAt": "timestamp",
    "maxSharedUsers": number
  }
}
```

### Reglas de negocio:
1. Solo el owner puede completar la compra
2. Máximo 10 usuarios por carrito compartido
3. Enlaces expiran después de 7 días (configurable)
4. Notificaciones en tiempo real de cambios (WebSocket)
5. Log de quién hizo cada cambio
6. Owner puede revocar acceso en cualquier momento

**UX Designer:**  
¿Mostramos quién está viendo/editando el carrito en tiempo real?

**Product Manager:**  
Sí, como Google Docs. Mostrar avatares de usuarios activos y highlight de qué item está editando cada uno.

**Tech Lead:**  
Necesitaríamos WebSocket para:
- Notificar cambios en tiempo real
- Mostrar usuarios activos
- Sincronizar ediciones concurrentes

**Security Lead:**  
También debemos:
- Rate limiting en generación de enlaces
- Validar que solo usuarios autenticados puedan editar
- Encriptar tokens de compartir
- Logs de auditoría de todos los accesos

**Product Manager:**  
¿Qué pasa con el pago? Si el owner completa la compra, ¿los demás pueden contribuir?

**Tech Lead:**  
Para v1, solo el owner paga. En v2 podríamos implementar split payment donde cada usuario paga su parte.

**UX Designer:**  
Necesitamos una sección "Mis carritos compartidos" donde el usuario vea:
- Carritos que creó y compartió
- Carritos compartidos con él
- Su rol en cada carrito

## Decisiones finales

1. Implementar sistema de carritos compartidos
2. 3 niveles de permisos: owner, editor, viewer
3. Compartir por enlace o invitación directa
4. Máximo 10 usuarios por carrito
5. WebSocket para colaboración en tiempo real
6. Solo owner puede completar compra (v1)
7. Logs de auditoría completos

## Próximos pasos

- Crear User Story en backlog
- Diseñar UI de colaboración en tiempo real
- Implementar sistema de permisos
- Configurar WebSocket infrastructure
- Definir flujo de notificaciones
