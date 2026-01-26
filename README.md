# 📚 Documentación del proyecto

Este directorio contiene la documentación funcional y técnica del sistema.
La documentación está organizada por **services** y por **releases**, permitiendo
entender tanto el estado actual como la evolución del producto en el tiempo.

Además, el proyecto incluye **agentes automáticos** encargados de:
- Procesar los *transcripts* de las reuniones y transformarlos en documentación funcional y **User Stories**
- Analizar User Stories finalizadas y proponer actualizaciones en la documentación de services
- Gestionar el ciclo de vida de las US manteniendo trazabilidad completa

---

## 🧭 Estructura general

```text
agents/
├── us_creator/          # Agente: transcript → funcional + US
├── doc_updater/         # Agente: US finalizada → propuesta de cambios
└── README.md            # Documentación completa de los agentes
docs/
├── backlog/
│   ├── to_do/          # US generadas automáticamente
│   ├── in_progress/    # US en desarrollo
│   └── done/           # US finalizadas (trigger de análisis)
├── proposals/          # Propuestas de cambios en services/
│   ├── archive/        # Propuestas aprobadas
│   └── rejected/       # Propuestas rechazadas
├── meetings/           # Transcripts y funcionales
├── releases/           # Releases por versión
└── services/           # Documentación técnica acumulada
```

---

## 🔄 Flujo completo del sistema

```
1. Meeting → transcript.md
      ↓
2. 🤖 us_creator_agent.py → funcional.md + US en /backlog/to_do
      ↓
3. 👤 Desarrollo humano → mover a /backlog/in_progress
      ↓
4. 👤 US finalizada → mover a /backlog/done
      ↓
5. 🤖 doc_updater_agent.py → propuesta en /proposals
      ↓
6. 👤 Revisión humana → apply_proposal.py
      ↓
7. 👤 Aplicar cambios manualmente en /docs/services
      ↓
8. 👤 Mover US a /releases/release-X.X
```

---

## ▶️ Cómo usar el sistema

### 1️⃣ Generar US desde meetings

Para transformar los *transcripts* de los meetings en documentación funcional y User Stories:

1. En caso de un **nuevo meeting**, crea una carpeta dentro de `docs/meetings/` con el formato:
    ```bash
    mkdir docs/meetings/meeting-YYYY-MM-DD
    ```
    Y añade un `transcript.md`

2. Crea un archivo `.env` con tu token de GitHub, siguiendo el ejemplo en `.env.example`:
    ```bash
    cp .env.example .env
    # Editar .env y añadir: GITHUB_TOKEN=tu_token_aqui
    ```

3. Ejecuta el agente desde la raíz del proyecto:
    ```bash
    cd agents/us_creator
    python3 US_creator_agent.py
    ```

**Resultado:**
- ✅ Genera el documento funcional en `docs/meetings/meeting-YYYY-MM-DD/funcional.md`
- ✅ Crea la User Story en `docs/backlog/to_do/US-XXX_titulo.md`
- ✅ Añade un enlace al funcional en la User Story

---

### 2️⃣ Gestionar el desarrollo de US

```bash
# Cuando comiences a trabajar en una US
mv docs/backlog/to_do/US-XXX_*.md docs/backlog/in_progress/

# Desarrollar, hacer commits, tests...

# Cuando finalices la US
mv docs/backlog/in_progress/US-XXX_*.md docs/backlog/done/
```

---

### 3️⃣ Generar propuestas de actualización

Cuando una US está en `/backlog/done`, ejecuta el agente de actualización:

```bash
cd agents/doc_updater
python3 doc_updater_agent.py
```

**Resultado:**
- ✅ Analiza todas las US en `/backlog/done`
- ✅ Genera propuestas en `docs/proposals/US-XXX_service_changes.md`
- ✅ No procesa la misma US dos veces

---

### 4️⃣ Revisar y aplicar propuestas

```bash
# Ver la propuesta
cat docs/proposals/US-XXX_service_changes.md

# Aplicar manualmente los cambios en docs/services/
# (siguiendo las instrucciones de la propuesta)

# Aprobar la propuesta
cd agents/doc_updater
python3 apply_proposal.py US-XXX --approve

# O rechazarla si no es adecuada
python3 apply_proposal.py US-XXX --reject
```

---

### 5️⃣ Mover a release

```bash
# Crear o usar release existente
mkdir -p docs/releases/release-X.X_YYYY-MM-DD

# Mover US a la release
mv docs/backlog/done/US-XXX_*.md docs/releases/release-X.X_YYYY-MM-DD/

# Actualizar índice de la release
code docs/releases/release-X.X_YYYY-MM-DD/indice.md
```

---

## 🛠️ Instalación y configuración

### Requisitos
- Python 3.8+
- **Una de las siguientes opciones:**
  - Token de GitHub (para usar GitHub Models - **gratis** 🆓)
  - API Key de OpenAI (de pago 💳)

### Instalación

1. **Clonar el repositorio**
    ```bash
    git clone <url-del-repo>
    cd data-analysis-testing
    ```

2. **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```
    
    O con entorno virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Configurar proveedor de IA**

    ```bash
    cp .env.example .env
    ```

    Edita el archivo `.env` y elige tu proveedor:

    #### **Opción A: GitHub Models (Gratis)** 🆓
    ```bash
    AI_PROVIDER=github
    GITHUB_TOKEN=tu_token_aqui
    ```
    
    Obtén tu token en: https://github.com/settings/tokens  
    **Ventaja:** Gratis con límites generosos  
    **Modelo usado:** gpt-4o
    
    #### **Opción B: OpenAI API (De pago)** 💳
    ```bash
    AI_PROVIDER=openai
    OPENAI_API_KEY=sk-tu-key-aqui
    ```
    
    Obtén tu API key en: https://platform.openai.com/api-keys  
    **Ventaja:** Sin límites (pagas por uso)  
    **Modelo usado:** gpt-4o

---

## 📖 Documentación adicional

- **[agents/README.md](agents/README.md)**: Documentación completa de los agentes
- **[docs/services/indice.md](docs/services/indice.md)**: Índice de la documentación técnica
- **[docs/releases/indice_releases.md](docs/releases/indice_releases.md)**: Historial de releases

---

## 🎯 Características principales

✅ **Automatización inteligente**: Genera documentación y US desde transcripts  
✅ **Control humano**: Todos los cambios críticos requieren aprobación manual  
✅ **Trazabilidad completa**: Desde meetings hasta releases  
✅ **Propuestas revisables**: Edita propuestas antes de aplicarlas  
✅ **Idempotencia**: No procesa la misma US dos veces  
✅ **Historial auditable**: Log de todas las propuestas aplicadas/rechazadas  

---

## 🔍 Comandos útiles

```bash
# Ver estado del backlog
ls docs/backlog/to_do/        # US pendientes
ls docs/backlog/in_progress/  # US en desarrollo
ls docs/backlog/done/         # US finalizadas

# Ver propuestas
ls docs/proposals/            # Pendientes de revisión
ls docs/proposals/archive/    # Aprobadas
ls docs/proposals/rejected/   # Rechazadas

# Contar US por estado
echo "To Do: $(ls docs/backlog/to_do/ | wc -l)"
echo "In Progress: $(ls docs/backlog/in_progress/ | wc -l)"
echo "Done: $(ls docs/backlog/done/ | wc -l)"
```

---

## 🐛 Troubleshooting

### Error de autenticación
```bash
# Verificar que el .env está configurado
cat .env

# Opción 1: Si usas GitHub Models
# - Verificar que AI_PROVIDER=github
# - Verificar que GITHUB_TOKEN está correcto
# - Solicitar acceso en: https://github.com/marketplace/models

# Opción 2: Si usas OpenAI
# - Verificar que AI_PROVIDER=openai
# - Verificar que OPENAI_API_KEY está correcta
# - Verificar saldo en: https://platform.openai.com/usage
```

### Cambiar de proveedor
```bash
# Editar .env
nano .env

# Cambiar AI_PROVIDER de "github" a "openai" o viceversa
AI_PROVIDER=openai  # o "github"

# Ejecutar agente - mostrará qué proveedor usa
cd agents/us_creator
python3 US_creator_agent.py
# 🤖 Usando OpenAI API (gpt-4o)
```

### Propuesta no se genera
```bash
# Verificar que la US está en done/
ls docs/backlog/done/

# Ver si ya fue procesada
cat agents/doc_updater/.processed_us.json
```

### Script no se ejecuta
```bash
# Verificar entorno virtual
source venv/bin/activate

# Verificar dependencias
pip list | grep openai
```

---

## 📝 Contribuir

1. Crear una rama para tu feature
2. Hacer commits descriptivos
3. Actualizar documentación si es necesario
4. Crear Pull Request

---

## 📄 Licencia

[Especificar licencia del proyecto]
