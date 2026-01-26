```markdown
# Propuesta de actualización - US-115

## Resumen de la US
La US-115 confirma la decisión de mantener la limitación de un solo código promocional por compra en el sistema Cart & Checkout. La funcionalidad de códigos promocionales apilables fue evaluada y rechazada debido a su alta complejidad técnica, riesgos de abuso y problemas de rendimiento. No se realizaron cambios en las APIs ni en la funcionalidad existente.

## Análisis de impacto
Tras analizar la User Story y la documentación actual de los servicios, se concluye que no se requiere ningún cambio en la documentación acumulada de los servicios en el directorio `services/`. Esto se debe a que:
- No se introducen nuevas funcionalidades ni endpoints.
- No se modifica el comportamiento actual del sistema.
- No hay impacto en los modelos de datos, flujos de eventos o dependencias entre servicios.

## Cambios propuestos
No se requieren cambios en la documentación acumulada.

---

## Recomendaciones
Se recomienda registrar la decisión de mantener la limitación de un solo código promocional en un documento de decisiones técnicas (ADR - Architecture Decision Record) o en la documentación funcional (`funcional.md`) para referencia futura. Esto permitirá que el equipo tenga un historial claro de las decisiones tomadas y sus justificaciones.

## Comandos de aplicación
```bash
# Revisar propuesta
cat docs/proposals/US-115_service_changes.md

# Aprobar y aplicar cambios
python agents/doc_updater/apply_proposal.py US-115 --approve

# Rechazar propuesta
python agents/doc_updater/apply_proposal.py US-115 --reject
```
```