# 📚 Sistema de Actualización de Documentación

Este directorio contiene los agentes para gestionar el ciclo de vida de las User Stories y mantener la documentación sincronizada.

## 🔄 Flujo completo

```
1. Meeting → transcript.md
         ↓
2. us_creator_agent.py → funcional.md + US en /backlog/to_do
         ↓
3. (Desarrollo humano) → mover a /backlog/in_progress
         ↓
4. (US finalizada) → mover a /backlog/done
         ↓
5. doc_updater_agent.py → propuesta en /proposals
         ↓
6. (Revisión humana) → apply_proposal.py --approve/reject
         ↓
7. (Manual) → aplicar cambios en /docs/services
         ↓
8. (Manual) → mover US a /releases/release-X.X
```

## 📁 Estructura de carpetas

```
docs/
├── backlog/
│   ├── to_do/          # US generadas automáticamente
│   ├── in_progress/    # US en desarrollo
│   └── done/           # US finalizadas (trigger del análisis)
├── proposals/          # Propuestas de cambios en services/
│   ├── archive/        # Propuestas aprobadas
│   └── rejected/       # Propuestas rechazadas
├── services/           # Documentación acumulada
└── releases/           # US deployadas por versión
```

## 🤖 Agentes disponibles

### 1. us_creator_agent.py
**Ubicación:** `agents/us_creator/`

**Función:** Genera documentación funcional y User Stories desde transcripts de meetings.

**Uso:**
```bash
cd agents/us_creator
python3 US_creator_agent.py
```

**Salida:**
- `docs/meetings/meeting-YYYY-MM-DD/funcional.md`
- `docs/backlog/to_do/US-XXX_titulo.md`

---

### 2. doc_updater_agent.py
**Ubicación:** `agents/doc_updater/`

**Función:** Analiza US finalizadas y genera propuestas de actualización para la documentación de services/.

**Uso:**
```bash
cd agents/doc_updater
python3 doc_updater_agent.py
```

**Entrada:** User Stories en `docs/backlog/done/`

**Salida:** Propuestas en `docs/proposals/US-XXX_service_changes.md`

**Características:**
- ✅ Analiza el impacto de cada US en la documentación
- ✅ Propone cambios específicos con contenido exacto
- ✅ Mantiene registro de US procesadas (`.processed_us.json`)
- ✅ No procesa la misma US dos veces

---

### 3. apply_proposal.py
**Ubicación:** `agents/doc_updater/`

**Función:** Gestiona la aprobación/rechazo de propuestas de actualización.

**Uso:**
```bash
cd agents/doc_updater

# Ver estado de una propuesta
python3 apply_proposal.py US-XXX --status

# Aprobar propuesta (después de aplicar cambios manualmente)
python3 apply_proposal.py US-XXX --approve

# Rechazar propuesta
python3 apply_proposal.py US-XXX --reject
```

**Notas:**
- ⚠️ Los cambios en `docs/services/` deben aplicarse **manualmente** siguiendo la propuesta
- ✅ El script solo registra la aprobación y archiva documentos
- 📝 Mantiene log de propuestas aplicadas/rechazadas

---

## 📝 Workflow ejemplo completo

### Paso 1: Nueva reunión
```bash
# Crear carpeta de meeting
mkdir docs/meetings/meeting-2026-01-23

# Añadir transcript
echo "..." > docs/meetings/meeting-2026-01-23/transcript.md

# Generar funcional y US
cd agents/us_creator
python3 US_creator_agent.py
```

**Resultado:** `US-113` creada en `docs/backlog/to_do/`

---

### Paso 2: Desarrollo
```bash
# Mover a in_progress cuando empieces a trabajar
mv docs/backlog/to_do/US-113_*.md docs/backlog/in_progress/

# Desarrollar la funcionalidad...
# Hacer commits, tests, etc.
```

---

### Paso 3: Finalizar US
```bash
# Cuando termines, mover a done
mv docs/backlog/in_progress/US-113_*.md docs/backlog/done/
```

---

### Paso 4: Generar propuesta de actualización
```bash
cd agents/doc_updater
python3 doc_updater_agent.py
```

**Resultado:** `docs/proposals/US-113_service_changes.md` creada

---

### Paso 5: Revisar propuesta
```bash
# Ver la propuesta
cat docs/proposals/US-113_service_changes.md

# O abrirla en VS Code
code docs/proposals/US-113_service_changes.md
```

---

### Paso 6: Aplicar cambios manualmente
Siguiendo la propuesta, editar los archivos en `docs/services/`:
```bash
# Ejemplo: si la propuesta dice actualizar 20_cart_service.md
code docs/services/20_cart_service.md
# Aplicar los cambios indicados en la propuesta
```

---

### Paso 7: Aprobar propuesta
```bash
cd agents/doc_updater
python3 apply_proposal.py US-113 --approve
```

Esto:
- ✅ Registra la aprobación
- ✅ Archiva la propuesta en `proposals/archive/`
- ⚠️ NO mueve automáticamente la US a releases

---

### Paso 8: Mover a release
```bash
# Crear o usar release existente
mkdir -p docs/releases/release-1.3_2026-01-25

# Mover US a la release
mv docs/backlog/done/US-113_*.md docs/releases/release-1.3_2026-01-25/

# Actualizar índice de la release
code docs/releases/release-1.3_2026-01-25/indice.md
```

---

## 🎯 Comandos rápidos

```bash
# Ver US pendientes
ls docs/backlog/to_do/

# Ver US en desarrollo
ls docs/backlog/in_progress/

# Ver US finalizadas esperando propuesta
ls docs/backlog/done/

# Ver propuestas pendientes
ls docs/proposals/*.md

# Ver propuestas aprobadas
ls docs/proposals/archive/

# Ver propuestas rechazadas
ls docs/proposals/rejected/
```

---

## 🔧 Configuración

### Variables de entorno (.env)
```bash
GITHUB_TOKEN=tu_token_aqui
```

### Dependencias
```bash
pip install -r requirements.txt
```

---

## 📊 Estado del sistema

Para ver el estado completo:
```bash
# Contar US por estado
echo "To Do: $(ls docs/backlog/to_do/ | wc -l)"
echo "In Progress: $(ls docs/backlog/in_progress/ | wc -l)"
echo "Done: $(ls docs/backlog/done/ | wc -l)"
echo "Propuestas pendientes: $(ls docs/proposals/*.md 2>/dev/null | wc -l)"
echo "Releases: $(ls -d docs/releases/release-* | wc -l)"
```

---

## ⚠️ Notas importantes

1. **Control humano:** Todos los cambios en `docs/services/` son manuales
2. **Trazabilidad:** Cada propuesta está documentada y archivada
3. **Idempotencia:** Los agentes no procesan la misma US dos veces
4. **Flexibilidad:** Puedes editar propuestas antes de aprobarlas
5. **Auditoría:** El log `.applied_proposals.json` guarda historial

---

## 🐛 Troubleshooting

### US no se procesa
```bash
# Verificar que está en done/
ls docs/backlog/done/US-XXX*

# Verificar si ya fue procesada
cat agents/doc_updater/.processed_us.json
```

### Propuesta no se genera
```bash
# Ver logs del agente
cd agents/doc_updater
python3 doc_updater_agent.py

# Verificar token de GitHub
echo $GITHUB_TOKEN
```

### Error al aprobar propuesta
```bash
# Verificar que la propuesta existe
ls docs/proposals/US-XXX*

# Verificar permisos
chmod +x agents/doc_updater/apply_proposal.py
```
