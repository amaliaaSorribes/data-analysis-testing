import os, re, json
from openai import OpenAI

def load_env_manual(path="../../.env"):
    with open(path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

load_env_manual()

# Configuración para GitHub Models
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ.get("GITHUB_TOKEN")
)

DONE_PATH = "../../docs/backlog/done"
PROPOSALS_PATH = "../../docs/proposals"
SERVICES_PATH = "../../docs/services"
PROCESSED_FILE = ".processed_us.json"

SYSTEM_PROMPT = """
Eres un agente experto en análisis de User Stories y actualización de documentación técnica.

Tu tarea es:
1. Analizar una User Story finalizada
2. Identificar qué documentos de services/ necesitan actualización
3. Proponer cambios específicos, concretos y aplicables
4. Justificar cada cambio

Reglas:
- Sé específico: indica sección exacta, línea aproximada, contenido antes/después
- Solo propón cambios que estén explícitamente justificados por la US
- Si no hay cambios necesarios en services/, di claramente "No requiere cambios en documentación acumulada"
- Formato claro para que un humano pueda revisar y aplicar
"""


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_processed():
    """Carga la lista de US ya procesadas"""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            return json.load(f)
    return []


def mark_as_processed(us_id):
    """Marca una US como procesada"""
    processed = load_processed()
    if us_id not in processed:
        processed.append(us_id)
        with open(PROCESSED_FILE, "w") as f:
            json.dump(processed, f, indent=2)


def get_us_id_from_filename(filename):
    """Extrae el ID de US del nombre de archivo"""
    match = re.match(r"(US-\d+)", filename)
    return match.group(1) if match else None


def load_all_services():
    """Carga todos los documentos de services para contexto"""
    services_content = {}
    
    for filename in os.listdir(SERVICES_PATH):
        if filename.endswith(".md"):
            path = os.path.join(SERVICES_PATH, filename)
            services_content[filename] = read_file(path)
    
    return services_content


def generate_proposal(us_file):
    """Genera propuesta de cambios para una US"""
    us_id = get_us_id_from_filename(us_file)
    
    print(f"\nAnalizando {us_id}...")
    
    # Leer US
    us_path = os.path.join(DONE_PATH, us_file)
    us_content = read_file(us_path)
    
    # Cargar documentación de services
    services = load_all_services()
    services_summary = "\n\n".join([
        f"=== {filename} ===\n{content[:500]}...\n"
        for filename, content in services.items()
    ])
    
    # Generar propuesta con LLM
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Analiza esta User Story finalizada y propón cambios en la documentación de services/.

USER STORY COMPLETA:
-------------------
{us_content}

DOCUMENTACIÓN ACTUAL DE SERVICES (primeras líneas):
--------------------------------------------------
{services_summary}

Genera un documento de propuesta en Markdown con:

# Propuesta de actualización - {us_id}

## Resumen de la US
[Breve resumen de qué hace la US]

## Análisis de impacto
[Qué partes de la documentación se ven afectadas]

## Cambios propuestos

### [Nombre del archivo service afectado]

#### Cambio 1: [Título descriptivo]
**Sección afectada:** [Nombre de la sección]
**Tipo de cambio:** [Añadir/Modificar/Deprecar/Eliminar]

**Justificación:**
[Por qué es necesario este cambio]

**Contenido propuesto:**
```
[Contenido exacto a añadir o modificar]
```

**Ubicación:**
[Después de qué contenido o en qué parte del documento]

---

## Recomendaciones
[Cualquier consideración adicional]

## Comandos de aplicación
```bash
# Revisar propuesta
cat docs/proposals/{us_id}_service_changes.md

# Aprobar y aplicar cambios
python agents/doc_updater/apply_proposal.py {us_id} --approve

# Rechazar propuesta
python agents/doc_updater/apply_proposal.py {us_id} --reject
```
"""
            }
        ],
        temperature=0.3
    )
    
    proposal_content = response.choices[0].message.content
    
    # Guardar propuesta
    proposal_filename = f"{us_id}_service_changes.md"
    proposal_path = os.path.join(PROPOSALS_PATH, proposal_filename)
    write_file(proposal_path, proposal_content)
    
    print(f"✅ Propuesta generada: {proposal_path}")
    
    return proposal_path


def main():
    print("🔍 Buscando User Stories en /backlog/done...")
    
    if not os.path.exists(DONE_PATH):
        print(f"❌ La carpeta {DONE_PATH} no existe")
        return
    
    # Cargar US ya procesadas
    processed = load_processed()
    
    # Buscar US en done/
    us_files = [f for f in os.listdir(DONE_PATH) if f.startswith("US-") and f.endswith(".md")]
    
    if not us_files:
        print("ℹ️  No hay User Stories en /backlog/done")
        return
    
    # Procesar cada US nueva
    new_proposals = 0
    for us_file in us_files:
        us_id = get_us_id_from_filename(us_file)
        
        if us_id in processed:
            print(f"⏭️  {us_id} ya fue procesada anteriormente")
            continue
        
        try:
            generate_proposal(us_file)
            mark_as_processed(us_id)
            new_proposals += 1
        except Exception as e:
            print(f"❌ Error procesando {us_id}: {e}")
    
    print(f"\n{'='*50}")
    print(f"✨ Proceso completado: {new_proposals} propuesta(s) generada(s)")
    
    if new_proposals > 0:
        print(f"\n📁 Revisa las propuestas en: {PROPOSALS_PATH}")
        print(f"📝 Para aplicar cambios: python agents/doc_updater/apply_proposal.py <US-ID> --approve")


if __name__ == "__main__":
    main()
