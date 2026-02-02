```markdown
# US-118 - Shared Cart System Implementation

---

## Identificación

- **ID:** US-118
- **Fecha:** 2026-01-30  
- **Servicio:** cart-service

---

## User Story

Como usuario autenticado quiero compartir carritos de compra con otros usuarios para colaborar en tiempo real en la creación y gestión de carritos.

---

## Descripción

Se implementará un sistema de carritos compartidos que permitirá a los usuarios colaborar en tiempo real en la creación y gestión de carritos de compra. Los usuarios podrán compartir carritos mediante enlaces únicos o invitaciones por correo electrónico, con diferentes niveles de permisos (owner, editor, viewer). Además, se incluirán funcionalidades como notificaciones en tiempo real, registro de auditoría, y una sección para gestionar los carritos compartidos.

---

## Cambios

### Qué se añadió

- Lógica para compartir carritos mediante enlace o invitación.
- Gestión de permisos para usuarios compartidos (owner, editor, viewer).
- Notificaciones en tiempo real mediante WebSocket.
- Registro de auditoría de todas las acciones realizadas en el carrito.
- Sección "Mis carritos compartidos" para visualizar y gestionar carritos compartidos.
- Seguridad en los enlaces compartidos (tokens únicos, encriptación, revocación de acceso, rate limiting).

---

## Impacto en APIs

### Nuevo endpoint

- **POST /cart/share/link** - Generar enlace de compartir.
- **POST /cart/share/invite** - Invitar usuario por email.
- **GET /cart/shared/{token}** - Acceder a carrito compartido.
- **DELETE /cart/share/{shareId}** - Revocar acceso.
- **GET /cart/shared** - Listar carritos compartidos conmigo.
- **PUT /cart/share/{shareId}/permissions** - Cambiar permisos de un usuario.
```

---

## Referencias

- Documento funcional: [`funcional.md`](../../docs/meetings/meeting-2026-01-30/funcional.md)
