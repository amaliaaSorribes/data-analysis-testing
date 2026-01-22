
### Qué contiene cada release

- **Objetivo del sprint** → qué se pretende entregar
- **Historias de usuario (US) incluidas** → con commits y links
- **Documentación acumulada afectada** (si aplica)
- **Resumen del sprint**

### Ejemplo de navegación

- `indice_releases.md` → listado de releases con fecha y enlace al detalle
- `release-1.0_YYYY-MM-DD/indice.md` → objetivo, historias incluidas, cambios en docs
- `US-105_update_item_quantity.md` → cada user story documenta:
  - **Identificación**: ID, fecha, servicio
  - **User Story**: Como [tipo de usuario], quiero [funcionalidad], para [beneficio]
  - **Descripción**: implementación detallada y restricciones
  - **Cambios**: endpoints, validaciones, lógica
  - **Impacto en APIs**
  - **Impacto en MongoDB** (si aplica)
  - **Links** a documentación relacionada
  - **Notas** de compatibilidad

> Cada release documenta la evolución del sistema y sirve como **histórico de entregas**.

---

## 🔄 Relación entre `releases` y `services`

- `releases/` → histórico de **qué y cuándo se entregó**
- `services/` → descripción de **cómo funciona el sistema hoy**

Ambas vistas se complementan:  
- Releases → evolución / histórico  
- Services → estado actual

---

## ⚡ Buenas prácticas

- Mantener el histórico de releases intacto  
- No duplicar información entre releases y servicios  
- Extraer información hacia `services/` solo cuando el servicio está consolidado  
- Seguir la convención de numeración y naming de archivos para mantener la estructura clara y navegable

---