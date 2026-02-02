```markdown
# Documento Funcional - Sistema de Carritos Compartidos (2026-01-30)

## Descripción General

Se implementará un sistema de carritos compartidos que permitirá a los usuarios colaborar en tiempo real en la creación y gestión de carritos de compra. Este sistema está dirigido tanto a usuarios empresariales como a familias, quienes podrán compartir carritos mediante enlaces o invitaciones directas, con diferentes niveles de permisos.

- **HU:** {completar enlace}  
- **Figma:** {completar enlace}

---

## Lógica Funcional

1. Los usuarios podrán compartir carritos de dos maneras:
   - **Por enlace:** Generar un enlace único para compartir.
   - **Por invitación:** Enviar invitaciones por correo electrónico.
2. Niveles de permisos:
   - **Owner:** Puede editar, eliminar, invitar, completar la compra.
   - **Editor:** Puede añadir/eliminar ítems y cambiar cantidades.
   - **Viewer:** Solo puede visualizar el carrito.
3. Reglas de negocio:
   - Solo el owner puede completar la compra.
   - Máximo 10 usuarios por carrito compartido.
   - Los enlaces compartidos expiran después de 7 días (configurable).
   - Notificaciones en tiempo real de cambios mediante WebSocket.
   - Registro de auditoría de todas las acciones realizadas en el carrito.
   - El owner puede revocar el acceso en cualquier momento.
4. Los usuarios podrán ver en tiempo real quién está editando o visualizando el carrito, con avatares y resaltado de los ítems que están siendo editados.
5. Se incluirá una sección "Mis carritos compartidos" donde los usuarios podrán ver:
   - Carritos que han creado y compartido.
   - Carritos compartidos con ellos.
   - Su rol en cada carrito.

---

## Lógica Frontend

1. Diseñar una interfaz para:
   - Compartir carritos mediante enlace o invitación.
   - Visualizar y gestionar permisos de los usuarios compartidos.
   - Mostrar en tiempo real los usuarios activos y los cambios realizados en el carrito.
   - Sección "Mis carritos compartidos" con:
     - Carritos creados y compartidos.
     - Carritos compartidos con el usuario.
     - Roles asignados.
2. Implementar notificaciones en tiempo real para:
   - Cambios en el carrito.
   - Usuarios activos.
   - Sincronización de ediciones concurrentes.
3. Mostrar avatares de usuarios activos y resaltar los ítems que están siendo editados.

---

## Lógica Backend

1. Implementar lógica para gestionar permisos de usuarios (owner, editor, viewer).
2. Configurar WebSocket para:
   - Notificaciones en tiempo real de cambios en el carrito.
   - Sincronización de ediciones concurrentes.
   - Mostrar usuarios activos.
3. Implementar seguridad en los enlaces compartidos:
   - Generar tokens únicos para los enlaces.
   - Encriptar los tokens.
   - Permitir revocar acceso en cualquier momento.
   - Aplicar rate limiting en la generación de enlaces.
4. Registrar logs de auditoría de todas las acciones realizadas en el carrito.
5. Validar que solo usuarios autenticados puedan editar los carritos.

---

## Nuevos servicios

### Endpoints nuevos:
- **POST /cart/share/link** - Generar enlace de compartir.
- **POST /cart/share/invite** - Invitar usuario por email.
- **GET /cart/shared/{token}** - Acceder a carrito compartido.
- **DELETE /cart/share/{shareId}** - Revocar acceso.
- **GET /cart/shared** - Listar carritos compartidos conmigo.
- **PUT /cart/share/{shareId}/permissions** - Cambiar permisos de un usuario.

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

---

## Partes Afectadas

### Site afectados

No especificado.

---

### Dependencias con terceros

No especificado.

---

### Analítica

No especificado.

---

### Contingencias

No especificado.

---

### Tipo de Usuario

Aplica únicamente a usuarios autenticados.

---

### Método de Envio

No especificado.

---

### Determinar tipo de mercancia

No especificado.

---

### Determinar ventanas de flujo afectadas

No especificado.
```