# 🎯 ARQUITECTURA PROPUESTA: Doc Update Agent

**Concepto General**
Un agente que detecte cuando una US se mueve al /backlog/done/, analiza su contenido, y **propone actualizaciones** a los documentos de `docs/services/` de forma **interactiva** con el humano.

### **LangGraph**

1. **Flujo con estados**: podemos modelar el proceso como un grafo de estados (análisis -> propuesta -> revisión/aceptación -> aplicación)
2. **Interacción humana**: langgraph permite pausar el flujo y esperar el input del usuario
3. **Modular**: cada nodo del grafo hace una cosa específica (analizar US, buscar docs afectados, generar diff, etc.,...)
4. **Observable**: podemos ver en todo momento lo que está ocurriendo en el agente

### 🏗️ **DISEÑO DEL GRAFO**

```
┌─────────────────┐
│  INICIO         │
│  (Detectar US   │
│   en /done/)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ANALYZER       │
│  Lee la US,     │
│  extrae cambios │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FINDER         │
│  Identifica qué │
│  docs de        │
│  services       │
│  se afectan     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PROPOSER       │
│  Genera las     │
│  modificaciones │
│  propuestas     │
│  (diffs)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HUMAN REVIEW   │ ◄─── AQUÍ PAUSA Y ESPERA TU DECISIÓN
│  Muestra cambios│
│  y pregunta:    │
│  ¿Aceptar?      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 REJECT    ACCEPT
    │         │
    │    ┌────▼─────┐
    │    │ APPLIER  │
    │    │ Aplica   │
    │    │ cambios  │
    │    └────┬─────┘
    │         │
    └────┬────┘
         │
         ▼
     ┌───────┐
     │  FIN  │
     └───────┘
```

### 📦 **COMPONENTES DEL SISTEMA**

1. **File Watcher**
    - Monitorea `/backlog/done` con la librería de Python `watchdog`
    - Cuando detecta un nuevo archivo `.md` dispara el agente

2. **Agente de LangGraph**

2.1. **Estados del Grafo**:
```python
class AgentState(TypedDict):
    us_file: str              # Ruta del archivo US
    us_content: str           # Contenido de la US
    analysis: dict            # Cambios extraídos (endpoints, modelos, etc.)
    affected_docs: list[str]  # Docs de services afectados
    proposals: list[dict]     # Propuestas de cambio con diffs
    human_decision: str       # "accept" o "reject"
    applied: bool             # Si se aplicaron los cambios
```
2.2. **Nodos**:

1. `analyze_node`:
    - Input: US markdown
    - Output: Diccionario con cambios detectados (nuevos endpoints, cambios en modelo de datos, etc.,...)
    - Usa LLM para extraer información estructurada
2. `find_affected_docs_node`:
    - Input: análisis de cambios
    - Output: lista de archivos en `docs/services/` que deben actualizarse
    - Usa embeddings o búsqueda semántica para encontrar los docs relevantes
3. `propose_changes_node`:
    - Input: US + docs afectados
    - Output: propuestas concretas de modificación (formato diff o descripción clara)
    - Genera el texto exacto a añadir/modificar en cada archivo
4. `human_review_node` (interrupt):
    - Pausa el grafo
    - Muestra las propuestas en consola (o interfaz web si la haces)
    - Espera input: `[A]ceptar / [R]echazar / [E]ditar`
5. `apply_changes_node`:
    - Si se acepta: modifica los archivos
    - Genera un commit o log de cambios

### 🛠️ **TECNOLOGÍAS**

```
langchain          # Para LLMs y prompts
langgraph          # Para el grafo de estados
openai             # API de GPT-4
chromadb           # Vector DB (para buscar docs similares)
watchdog           # File watcher (opcional)
rich               # Para output bonito en consola
```
### **📝 EJEMPLO DE FLUJO**

**Escenario**: Movemos `docs/backlog/to_do/US-108_persist_cart_by_userid.md` a `/backlog/done`

```
1. ANALYZER detecta:
   - Nuevo campo: userId en colección carts
   - Nuevo endpoint: GET /v1/carts/user/{userId}
   - Modificación: POST /v1/carts ahora acepta userId opcional

2. FINDER identifica docs afectados:
   - docs/services/02_modelo_datos_mongo.md (colección carts)
   - docs/services/20_cart_service.md (endpoints)

3. PROPOSER genera cambios:
   
   📄 02_modelo_datos_mongo.md
   ┌─────────────────────────────────────┐
   │ Sección: carts                      │
   │ Añadir campo:                       │
   │   "userId": "user-123" (opcional)   │
   │                                     │
   │ Actualizar índices:                 │
   │   { userId: 1, status: 1 }          │
   └─────────────────────────────────────┘
   
   📄 20_cart_service.md
   ┌─────────────────────────────────────┐
   │ Añadir endpoint:                    │
   │ GET /v1/carts/user/{userId}         │
   │ Devuelve carrito activo del user    │
   │                                     │
   │ Modificar POST /v1/carts:           │
   │ Request puede incluir userId        │
   └─────────────────────────────────────┘

4. HUMAN REVIEW muestra:
   
   ╔════════════════════════════════════╗
   ║  PROPUESTA DE CAMBIOS              ║
   ╠════════════════════════════════════╣
   ║  US: US-108                        ║
   ║  Archivos afectados: 2             ║
   ║                                    ║
   ║  [Ver detalles arriba]             ║
   ║                                    ║
   ║  ¿Aceptar cambios? (A/R/E):        ║
   ╚════════════════════════════════════╝

5. Si aceptas → APPLIER modifica los archivos
   Si rechazas → FIN (sin cambios)
```
