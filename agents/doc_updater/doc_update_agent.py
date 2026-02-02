#!/usr/bin/env python3
"""
Doc Update Agent - Actualiza documentación de services desde User Stories completadas

Flujo:
1. Lee una US desde /backlog/done/
2. Analiza los cambios que implica
3. Identifica qué docs de /docs/services/ se afectan
4. Propone modificaciones concretas
5. Espera aprobación humana
6. Aplica cambios si se acepta
"""

import os
import re
import json
from typing import TypedDict, Literal
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph import StateGraph, END
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

def load_env_manual(path="../../.env"):
    with open(path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

load_env_manual()

# Configuración del cliente según el proveedor
PROVIDER = os.environ.get("AI_PROVIDER", "openai").lower()  # "openai" o "github"

if PROVIDER == "github":
    # Usar GitHub Models
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.environ.get("GITHUB_TOKEN")
    )
    DEFAULT_MODEL = "gpt-4o"  # Modelo disponible en GitHub
else:
    # Usar OpenAI
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    DEFAULT_MODEL = "gpt-4o-mini"  # Modelo de OpenAI

console = Console()

# Rutas relativas desde este script
BASE_PATH = Path(__file__).parent.parent.parent
BACKLOG_DONE_PATH = BASE_PATH / "docs" / "backlog" / "done"
SERVICES_PATH = BASE_PATH / "docs" / "services"
RELEASES_PATH = BASE_PATH / "docs" / "releases"
PROPOSALS_PATH = BASE_PATH / "docs" / "proposals"
REJECTED_LOG = PROPOSALS_PATH / "rejected" / "rejected.json"
ACCEPTED_LOG = PROPOSALS_PATH / "accepted" / "accepted.json"

# ============================================================================
# ESTADOS DEL GRAFO
# ============================================================================

class AgentState(TypedDict):
    us_file: str                    # Ruta del archivo US
    us_content: str                 # Contenido de la US
    analysis: dict                  # Cambios extraídos (endpoints, modelos, etc.)
    affected_docs: list[str]        # Docs de services afectados
    proposals: list[dict]           # Propuestas de cambio con diffs
    human_decision: Literal["accept", "reject"]  # Decisión del usuario
    applied: bool                   # Si se aplicaron los cambios
    acceptance_reason: str          # Motivo de la aceptación

# ============================================================================
# FUNCIONES HELPER
# ============================================================================

def read_file(path: str) -> str:
    """Lee el contenido de un archivo"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path: str, content: str):
    """Escribe contenido a un archivo"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def list_service_docs() -> list[str]:
    """Lista todos los archivos .md en /docs/services/"""
    return [str(f) for f in SERVICES_PATH.glob("*.md")]

#===========================================================================
# ACTUALIZADOR DE RELEASES
#===========================================================================

def register_rejection(us_file: str, us_id: str, us_title: str, affected_docs: list[str], proposals: list[dict], reason: str):
    """Registra un rechazo en el log JSON"""
    from datetime import datetime
    
    # Crear estructura del rechazo
    rejection_entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "us_id": us_id,
        "us_title": us_title,
        "us_file": str(Path(us_file).name),
        "affected_documents": [Path(doc).name for doc in affected_docs],
        "proposed_changes_count": sum(len(p.get("proposal", {}).get("changes", [])) for p in proposals),
        "reason": reason,
        "proposals_summary": [
            {
                "document": Path(p["file"]).name,
                "changes_count": len(p.get("proposal", {}).get("changes", [])),
                "sections_affected": [c.get("section", "N/A") for c in p.get("proposal", {}).get("changes", [])]
            }
            for p in proposals
        ]
    }
    
    # Leer log existente o crear nuevo
    if REJECTED_LOG.exists():
        with open(REJECTED_LOG, "r", encoding="utf-8") as f:
            try:
                rejections = json.load(f)
            except json.JSONDecodeError:
                rejections = {"rejections": []}
    else:
        rejections = {
            "metadata": {
                "description": "Registro histórico de propuestas de cambios rechazadas",
                "purpose": "Trazabilidad de decisiones para evitar re-proponer cambios ya rechazados"
            },
            "rejections": []
        }
    
    # Añadir nuevo rechazo
    rejections["rejections"].append(rejection_entry)
    
    # Guardar
    with open(REJECTED_LOG, "w", encoding="utf-8") as f:
        json.dump(rejections, f, indent=2, ensure_ascii=False)
    
    return str(REJECTED_LOG)

def get_next_release_version() -> tuple[str, str]:
    """Obtiene la versión de release para hoy (reutiliza si ya existe, crea nueva si no)"""
    import re
    from datetime import datetime
    
    # Fecha actual en formato YYYY-MM-DD
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Buscar todas las carpetas release-X.Y_*
    release_dirs = list(RELEASES_PATH.glob("release-*"))
    
    # Verificar si ya existe un release con la fecha de hoy
    for d in release_dirs:
        if date_str in d.name:
            # Ya existe un release para hoy, extraer su versión
            match = re.match(r"release-(\d+)\.(\d+)_", d.name)
            if match:
                version = f"{match.group(1)}.{match.group(2)}"
                return version, date_str
    
    # No existe release para hoy, crear uno nuevo
    if not release_dirs:
        # No hay releases, empezar en 1.0
        version = "1.0"
    else:
        # Extraer versiones y encontrar la más alta
        versions = []
        for d in release_dirs:
            match = re.match(r"release-(\d+)\.(\d+)_", d.name)
            if match:
                major, minor = int(match.group(1)), int(match.group(2))
                versions.append((major, minor))
        
        if versions:
            # Ordenar y obtener la más alta
            versions.sort()
            last_major, last_minor = versions[-1]
            # Incrementar minor
            version = f"{last_major}.{last_minor + 1}"
        else:
            version = "1.0"
    
    return version, date_str

def register_rejection(us_file: str, us_id: str, us_title: str, affected_docs: list[str], proposals: list[dict], reason: str):
    """Registra un rechazo en el log JSON"""
    from datetime import datetime
    import json
    
    # Crear estructura del rechazo
    rejection_entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "us_id": us_id,
        "us_title": us_title,
        "us_file": str(Path(us_file).name),
        "affected_documents": [Path(doc).name for doc in affected_docs],
        "proposed_changes_count": sum(len(p.get("proposal", {}).get("changes", [])) for p in proposals),
        "reason": reason,
        "proposals_summary": [
            {
                "document": Path(p["file"]).name,
                "changes_count": len(p.get("proposal", {}).get("changes", [])),
                "sections_affected": [c.get("section", "N/A") for c in p.get("proposal", {}).get("changes", [])]
            }
            for p in proposals
        ]
    }
    
    # Leer log existente o crear nuevo
    if REJECTED_LOG.exists():
        with open(REJECTED_LOG, "r", encoding="utf-8") as f:
            try:
                rejections = json.load(f)
            except json.JSONDecodeError:
                rejections = {"rejections": []}
    else:
        rejections = {
            "metadata": {
                "description": "Registro histórico de propuestas de cambios rechazadas",
                "purpose": "Trazabilidad de decisiones para evitar re-proponer cambios ya rechazados"
            },
            "rejections": []
        }
    
    # Añadir nuevo rechazo
    rejections["rejections"].append(rejection_entry)
    
    # Guardar
    with open(REJECTED_LOG, "w", encoding="utf-8") as f:
        json.dump(rejections, f, indent=2, ensure_ascii=False)
    
    return str(REJECTED_LOG)

def register_acceptance(us_file: str, us_id: str, us_title: str, affected_docs: list[str], proposals: list[dict], reason: str, version: str, release_date: str):
    """Registra una aceptación en el log JSON"""
    from datetime import datetime
    
    # Crear estructura de la aceptación
    acceptance_entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "us_id": us_id,
        "us_title": us_title,
        "us_file": str(Path(us_file).name),
        "affected_documents": [Path(doc).name for doc in affected_docs],
        "applied_changes_count": sum(len(p.get("proposal", {}).get("changes", [])) for p in proposals),
        "reason": reason,
        "release": version,
        "release_date": release_date,
        "proposals_summary": [
            {
                "document": Path(p["file"]).name,
                "changes_count": len(p.get("proposal", {}).get("changes", [])),
                "sections_affected": [c.get("section", "N/A") for c in p.get("proposal", {}).get("changes", [])]
            }
            for p in proposals
        ]
    }
    
    # Leer log existente o crear nuevo
    if ACCEPTED_LOG.exists():
        with open(ACCEPTED_LOG, "r", encoding="utf-8") as f:
            try:
                acceptances = json.load(f)
            except json.JSONDecodeError:
                acceptances = {"accepted": []}
    else:
        acceptances = {
            "metadata": {
                "description": "Registro histórico de propuestas de cambios aceptadas y aplicadas",
                "purpose": "Trazabilidad de decisiones y base para generar objetivos de release"
            },
            "accepted": []
        }
    
    # Añadir nueva aceptación
    acceptances["accepted"].append(acceptance_entry)
    
    # Guardar
    with open(ACCEPTED_LOG, "w", encoding="utf-8") as f:
        json.dump(acceptances, f, indent=2, ensure_ascii=False)
    
    return str(ACCEPTED_LOG)

def generate_release_objective(release_dir: Path, version: str, date_str: str) -> str:
    """Genera un objetivo conciso del release basado en las US incluidas"""
    # Leer todas las US del release
    us_files = list(release_dir.glob("US-*.md"))
    
    if not us_files:
        return "Release inicial sin historias."
    
    # Extraer títulos y descripciones breves de cada US
    us_summaries = []
    for us_file in us_files:
        content = read_file(str(us_file))
        # Extraer título (primera línea con #)
        title_match = re.search(r"^#\s+US-\d+\s+-\s+(.+)$", content, re.MULTILINE)
        # Extraer user story statement
        us_match = re.search(r"## User Story\s+(.+?)(?=\n##|\Z)", content, re.DOTALL)
        
        if title_match:
            title = title_match.group(1).strip()
            us_statement = us_match.group(1).strip() if us_match else ""
            us_summaries.append({
                "id": us_file.stem.split("_")[0],
                "title": title,
                "statement": us_statement[:200]  # Limitar longitud
            })
    
    # Usar IA para generar objetivo del release
    summaries_text = "\n".join([
        f"- {s['id']}: {s['title']}\n  {s['statement'][:150]}"
        for s in us_summaries
    ])
    
    prompt = f"""Genera un objetivo conciso para un release de software basándote en estas User Stories.

RELEASE: {version} ({date_str})

USER STORIES INCLUIDAS:
{summaries_text}

TAREA:
Escribe 1-2 frases que describan el OBJETIVO PRINCIPAL de este release. Debe explicar QUÉ se logra y PARA QUÉ (valor de negocio).

REGLAS:
- Máximo 2 frases
- Enfócate en el valor de negocio, no en detalles técnicos
- Usa lenguaje claro y directo
- No uses formato markdown
- Ejemplo: "Mejorar la experiencia de compra con persistencia de carrito y validación de precios en tiempo real."
"""
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "Eres un product manager experto que escribe objetivos claros y concisos de releases."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()

def archive_us_to_release(us_file: str, version: str, date_str: str, us_id: str, us_title: str, proposals: list[dict] = None):
    """Archiva una US en la carpeta de release correspondiente"""
    # Crear nombre de carpeta release
    release_dir_name = f"release-{version}_{date_str}"
    release_dir = RELEASES_PATH / release_dir_name
    
    # Crear carpeta si no existe
    release_dir.mkdir(exist_ok=True)
    
    # Mover archivo US
    us_filename = Path(us_file).name
    dest_path = release_dir / us_filename
    
    import shutil
    shutil.move(us_file, str(dest_path))
    
    # Generar resumen de cambios aplicados
    changes_summary = ""
    brief_summary = ""
    if proposals:
        # Lista detallada de cambios
        changes_summary = "\n  - **Cambios aplicados:**\n"
        for prop in proposals:
            doc_name = Path(prop["file"]).name
            changes = prop.get("proposal", {}).get("changes", [])
            if changes:
                sections = [c.get("section", "N/A") for c in changes]
                sections_str = ", ".join(set(sections))
                changes_summary += f"    - Modificado `{doc_name}`: {len(changes)} cambio(s) en {sections_str}\n"
        
        # Generar resumen breve con LLM
        proposals_json = json.dumps([
            {
                "documento": Path(p["file"]).name,
                "cambios": [{"seccion": c.get("section"), "accion": c.get("action")} for c in p.get("proposal", {}).get("changes", [])]
            }
            for p in proposals
        ], indent=2, ensure_ascii=False)
        
        summary_prompt = f"""Genera un resumen MUY BREVE (máximo 2 frases) de estos cambios aplicados a documentación técnica.

CAMBIOS:
{proposals_json}

US: {us_title}

Responde solo con 1-2 frases concisas que resuman QUÉ se actualizó y POR QUÉ. No uses formato markdown, solo texto plano."""

        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "Eres un experto técnico que resume cambios de documentación de forma concisa."},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=0.2,
            max_tokens=100
        )
        
        brief_summary = response.choices[0].message.content.strip()
        changes_summary += f"  - **Resumen:** {brief_summary}\n"
    
    # Crear/actualizar indice.md del release
    indice_path = release_dir / "indice.md"
    
    if indice_path.exists():
        # Añadir US al índice existente
        indice_content = read_file(str(indice_path))
        
        # Buscar sección "Historias incluidas"
        us_entry = f"""\n- **{us_id} – {us_title}**
  - 📄 [Detalle {us_id}](./{us_filename}){changes_summary}
"""
        
        # Insertar antes de "Documentos afectados" si existe, sino al final
        if "## Documentos afectados" in indice_content:
            indice_content = indice_content.replace(
                "## Documentos afectados",
                us_entry + "\n## Documentos afectados"
            )
        else:
            indice_content += us_entry
        
        # Regenerar objetivo del release basado en todas las US
        release_objective = generate_release_objective(release_dir, version, date_str)
        
        # Actualizar sección de objetivo si existe
        if "## Objetivo" in indice_content:
            # Reemplazar contenido entre "## Objetivo" y el siguiente "##"
            indice_content = re.sub(
                r"(## Objetivo\s*\n\n)(.+?)(\n\n---\n\n## Historias incluidas)",
                rf"\1{release_objective}\3",
                indice_content,
                flags=re.DOTALL
            )
        
        write_file(str(indice_path), indice_content)
    else:
        # Crear nuevo índice con objetivo generado
        release_objective = generate_release_objective(release_dir, version, date_str)
        
        indice_content = f"""# Release {version}

Sprint del {date_str}

---

## Objetivo

{release_objective}

---

## Historias incluidas

- **{us_id} – {us_title}**
  - 📄 [Detalle {us_id}](./{us_filename}){changes_summary}

---

## Documentos afectados

> Los cambios aplicados actualizan la documentación acumulada en `/docs/services/`.
"""
        write_file(str(indice_path), indice_content)
    
    # Actualizar indice_releases.md global
    indice_releases_path = RELEASES_PATH / "indice_releases.md"
    
    if indice_releases_path.exists():
        indice_releases = read_file(str(indice_releases_path))
        
        # Verificar si ya existe este release
        if release_dir_name not in indice_releases:
            # Generar objetivo para el índice global
            release_objective_short = generate_release_objective(release_dir, version, date_str)
            
            # Añadir nuevo release al final
            new_entry = f"""\n---

## Release {version} – {date_str}
**Objetivo:** {release_objective_short}  
📄 [Ver detalle del release](./{release_dir_name}/indice.md)
"""
            indice_releases += new_entry
            write_file(str(indice_releases_path), indice_releases)
    
    return str(dest_path)

# ============================================================================
# NODOS DEL GRAFO
# ============================================================================

def analyze_node(state: AgentState) -> AgentState:
    """
    Nodo 1: ANALYZER
    Lee la US y extrae cambios estructurados (endpoints, modelos, etc.)
    """
    console.print("\n[bold cyan]🔍 ANALYZER:[/bold cyan] Analizando User Story...")
    
    us_content = state["us_content"]
    
    # Prompt para extraer información estructurada
    analysis_prompt = f"""
Analiza esta User Story y extrae ÚNICAMENTE la información relevante para actualizar documentación técnica.

USER STORY:
{us_content}

Extrae y estructura la siguiente información en formato JSON:

{{
  "us_id": "US-XXX",
  "title": "título breve",
  "service": "nombre del servicio afectado (ej: cart-service, pricing-service)",
  "changes": {{
    "new_endpoints": [
      {{"method": "POST", "path": "/v1/...", "description": "..."}}
    ],
    "modified_endpoints": [
      {{"method": "GET", "path": "/v1/...", "changes": "qué cambia"}}
    ],
    "data_model_changes": [
      {{"collection": "carts", "changes": "añadir campo userId (opcional)"}}
    ],
    "new_indices": [
      {{"collection": "carts", "index": "{{ userId: 1, status: 1 }}"}}
    ]
  }}
}}

REGLAS:
- Solo incluye información EXPLÍCITA en la US
- Si no hay cambios de algún tipo, usa array vacío []
- Sé preciso y conciso
"""
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "Eres un experto en análisis de requisitos técnicos. Extraes información estructurada de User Stories."},
            {"role": "user", "content": analysis_prompt}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    analysis = json.loads(response.choices[0].message.content)
    
    console.print(f"[green]✓[/green] Análisis completado: US-{analysis.get('us_id', 'N/A')}")
    console.print(f"   Servicio: {analysis.get('service', 'N/A')}")
    
    state["analysis"] = analysis
    return state

def find_affected_docs_node(state: AgentState) -> AgentState:
    """
    Nodo 2: FINDER
    Identifica qué documentos de /docs/services/ deben actualizarse
    """
    console.print("\n[bold cyan]📂 FINDER:[/bold cyan] Identificando documentos afectados...")
    
    analysis = state["analysis"]
    service_docs = list_service_docs()
    
    affected = []
    
    # Siempre revisar el doc del servicio mencionado
    service_name = analysis.get("service", "").lower()
    for doc in service_docs:
        doc_name = Path(doc).name.lower()
        if service_name.replace("-", "_") in doc_name:
            affected.append(doc)
    
    # Si hay cambios en modelo de datos, incluir 02_modelo_datos_mongo.md
    if analysis.get("changes", {}).get("data_model_changes"):
        modelo_doc = str(SERVICES_PATH / "02_modelo_datos_mongo.md")
        if modelo_doc not in affected:
            affected.append(modelo_doc)
    
    # Si hay cambios en endpoints, incluir el overview
    if analysis.get("changes", {}).get("new_endpoints") or analysis.get("changes", {}).get("modified_endpoints"):
        overview_doc = str(SERVICES_PATH / "00_overview_cart_checkout.md")
        if overview_doc not in affected:
            affected.append(overview_doc)
    
    console.print(f"[green]✓[/green] {len(affected)} documentos identificados:")
    for doc in affected:
        console.print(f"   • {Path(doc).name}")
    
    state["affected_docs"] = affected
    return state

def propose_changes_node(state: AgentState) -> AgentState:
    """
    Nodo 3: PROPOSER
    Genera propuestas concretas de modificación para cada documento
    """
    console.print("\n[bold cyan]✨ PROPOSER:[/bold cyan] Generando propuestas de cambios...")
    
    analysis = state["analysis"]
    affected_docs = state["affected_docs"]
    us_content = state["us_content"]
    
    proposals = []
    
    for doc_path in affected_docs:
        doc_content = read_file(doc_path)
        doc_name = Path(doc_path).name
        
        # Prompt para generar cambios específicos
        propose_prompt = f"""
Eres un experto técnico actualizando documentación de microservicios.

CONTEXTO:
- User Story completada que introduce cambios
- Documento técnico que debe actualizarse

USER STORY:
{us_content}

ANÁLISIS DE CAMBIOS:
{json.dumps(analysis['changes'], indent=2)}

DOCUMENTO ACTUAL ({doc_name}):
{doc_content[:2000]}... (primeras 2000 chars)

TAREA:
Genera las modificaciones ESPECÍFICAS que deben hacerse en este documento.

FORMATO DE RESPUESTA (JSON):
{{
  "document": "{doc_name}",
  "changes": [
    {{
      "section": "nombre de la sección a modificar",
      "action": "add|modify|delete",
      "content": "texto exacto a añadir o modificar",
      "reason": "por qué este cambio"
    }}
  ]
}}

REGLAS:
- Sé específico: indica la sección exacta donde hacer el cambio
- Respeta el formato markdown del documento original
- Solo propón cambios que sean NECESARIOS según la US
- Si no hay cambios necesarios en este doc, devuelve array vacío
"""
        
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "Eres un experto en documentación técnica de microservicios."},
                {"role": "user", "content": propose_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        proposal = json.loads(response.choices[0].message.content)
        
        if proposal.get("changes"):
            proposals.append({
                "file": doc_path,
                "proposal": proposal
            })
    
    console.print(f"[green]✓[/green] Propuestas generadas para {len(proposals)} archivos")
    
    state["proposals"] = proposals
    return state

def human_review_node(state: AgentState) -> AgentState:
    """
    Nodo 4: HUMAN REVIEW
    Muestra las propuestas y espera decisión del usuario
    """
    console.print("\n" + "="*70)
    console.print(Panel.fit(
        "[bold yellow]👤 REVISIÓN HUMANA REQUERIDA[/bold yellow]\n\n"
        f"US: {state['analysis'].get('us_id', 'N/A')} - {state['analysis'].get('title', 'N/A')}\n"
        f"Archivos afectados: {len(state['proposals'])}",
        title="🔍 Propuesta de Cambios",
        border_style="yellow"
    ))
    
    # Mostrar cada propuesta
    for i, prop in enumerate(state["proposals"], 1):
        doc_name = Path(prop["file"]).name
        changes = prop["proposal"].get("changes", [])
        
        console.print(f"\n[bold cyan]📄 {i}. {doc_name}[/bold cyan]")
        console.print(f"   Cambios propuestos: {len(changes)}\n")
        
        for j, change in enumerate(changes, 1):
            console.print(f"   [yellow]{j}.[/yellow] Sección: [bold]{change.get('section', 'N/A')}[/bold]")
            console.print(f"      Acción: {change.get('action', 'N/A')}")
            console.print(f"      Razón: {change.get('reason', 'N/A')}")
            
            content = change.get('content', '')
            if len(content) > 200:
                content = content[:200] + "..."
            console.print(f"      Contenido:\n      {content}\n")
    
    console.print("\n" + "="*70)
    
    # Solicitar decisión
    decision = Prompt.ask(
        "\n¿Qué deseas hacer?",
        choices=["accept", "reject"],
        default="reject"
    )
    
    state["human_decision"] = decision
    return state

def choose_release() -> tuple[str, str]:
    """Permite elegir un release existente o crear uno nuevo"""
    # Listar releases existentes
    release_dirs = sorted(RELEASES_PATH.glob("release-*"))
    
    if release_dirs:
        console.print("\n[bold cyan]📦 Releases existentes:[/bold cyan]\n")
        for i, release_dir in enumerate(release_dirs, 1):
            console.print(f"  {i}. {release_dir.name}")
        console.print(f"  {len(release_dirs) + 1}. [yellow]Crear nuevo release[/yellow]")
        console.print()
        
        choice = Prompt.ask(
            "¿En qué release quieres incluir esta US?",
            default=str(len(release_dirs) + 1)
        )
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(release_dirs):
                # Usar release existente
                selected_release = release_dirs[choice_num - 1]
                # Extraer versión y fecha del nombre: release-X.Y_YYYY-MM-DD
                match = re.match(r"release-(\d+\.\d+)_(\d{4}-\d{2}-\d{2})", selected_release.name)
                if match:
                    return match.group(1), match.group(2)
        except ValueError:
            pass
    
    # Crear nuevo release
    console.print("\n[bold cyan]🆕 Crear nuevo release:[/bold cyan]\n")
    
    # Sugerir siguiente versión
    if release_dirs:
        last_release = release_dirs[-1]
        match = re.match(r"release-(\d+)\.(\d+)_", last_release.name)
        if match:
            major, minor = int(match.group(1)), int(match.group(2))
            suggested_version = f"{major}.{minor + 1}"
        else:
            suggested_version = "1.0"
    else:
        suggested_version = "1.0"
    
    version = Prompt.ask("Versión del release", default=suggested_version)
    
    # Sugerir fecha de hoy
    from datetime import datetime
    suggested_date = datetime.now().strftime("%Y-%m-%d")
    date_str = Prompt.ask("Fecha del release (YYYY-MM-DD)", default=suggested_date)
    
    return version, date_str

def apply_changes_node(state: AgentState) -> AgentState:
    """
    Nodo 5: APPLIER
    Aplica los cambios a los archivos si fueron aceptados
    """
    # Solicitar justificación de la aceptación
    console.print("\n[dim]Para trazabilidad, indica el motivo de la aceptación:[/dim]")
    console.print("[dim](Ejemplos: 'Cambios necesarios y bien fundamentados', 'Mejora la documentación', 'Alineado con US', etc.)[/dim]\n")
    
    acceptance_reason = Prompt.ask(
        "Motivo de la aceptación",
        default="Cambios aprobados"
    )
    
    # Guardar el motivo en el estado para usarlo después
    state["acceptance_reason"] = acceptance_reason
    
    console.print("\n[bold cyan]⚙️  APPLIER:[/bold cyan] Aplicando cambios...")
    
    analysis = state["analysis"]
    us_content = state["us_content"]
    
    for prop in state["proposals"]:
        doc_path = prop["file"]
        changes = prop["proposal"].get("changes", [])
        
        if not changes:
            continue
            
        # Leer contenido actual del documento
        doc_content = read_file(doc_path)
        doc_name = Path(doc_path).name
        
        # Usar LLM para aplicar los cambios al documento completo
        apply_prompt = f"""
Eres un experto técnico que actualiza documentación de microservicios.

DOCUMENTO ACTUAL ({doc_name}):
{doc_content}

CAMBIOS A APLICAR:
{json.dumps(changes, indent=2, ensure_ascii=False)}

CONTEXTO (User Story que motiva los cambios):
{us_content}

TAREA:
Aplica TODOS los cambios propuestos al documento actual y devuelve el documento COMPLETO actualizado.

REGLAS CRÍTICAS:
- Mantén TODO el contenido existente que no se modifica
- Respeta EXACTAMENTE el formato markdown original
- Aplica los cambios en las secciones correctas
- Si un cambio dice "add", añade el contenido en la sección indicada
- Si un cambio dice "modify", actualiza el contenido existente
- Si un cambio dice "delete", elimina el contenido indicado
- NO añadas comentarios, solo devuelve el markdown actualizado
- NO uses marcadores como "// cambio aquí" o similares
- Devuelve el documento COMPLETO, no solo las partes modificadas
"""
        
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "Eres un experto en documentación técnica. Actualizas documentos aplicando cambios específicos mientras mantienes el formato y estructura original."},
                {"role": "user", "content": apply_prompt}
            ],
            temperature=0.1
        )
        
        updated_content = response.choices[0].message.content
        
        # Limpiar posibles marcadores de código markdown
        if updated_content.startswith("```markdown"):
            updated_content = updated_content.replace("```markdown\n", "", 1)
        if updated_content.startswith("```"):
            updated_content = updated_content.replace("```\n", "", 1)
        if updated_content.endswith("```"):
            updated_content = updated_content.rsplit("```", 1)[0]
        
        updated_content = updated_content.strip()
        
        # Guardar el archivo actualizado
        write_file(doc_path, updated_content + "\n")
        
        console.print(f"[green]✓[/green] Aplicados {len(changes)} cambios en {doc_name}")
    
    state["applied"] = True
    
    console.print("\n[bold green]✅ Todos los cambios aplicados correctamente[/bold green]")
    
    # NO archivamos aquí, se hará al final en batch
    
    return state

def reject_node(state: AgentState) -> AgentState:
    """
    Nodo alternativo: REJECT
    Termina sin aplicar cambios y registra el rechazo
    """
    console.print("\n[bold yellow]❌ Cambios rechazados. No se modificó ningún archivo.[/bold yellow]\n")
    
    # Solicitar motivo del rechazo
    console.print("[dim]Para trazabilidad, indica el motivo del rechazo:[/dim]")
    console.print("[dim](Ejemplos: 'Cambios demasiado agresivos', 'Falta contexto', 'Enfoque incorrecto', etc.)[/dim]\n")
    
    reason = Prompt.ask(
        "Motivo del rechazo",
        default="No especificado"
    )
    
    # Registrar rechazo
    us_id = state["analysis"].get("us_id", "US-XXX")
    us_title = state["analysis"].get("title", "Sin título")
    
    console.print("\n[cyan]📝 Registrando rechazo...[/cyan]")
    
    log_path = register_rejection(
        us_file=state["us_file"],
        us_id=us_id,
        us_title=us_title,
        affected_docs=state["affected_docs"],
        proposals=state["proposals"],
        reason=reason
    )
    
    console.print(f"[green]✓[/green] Rechazo registrado en: {Path(log_path).relative_to(BASE_PATH)}")
    console.print(f"[dim]   Motivo: {reason}[/dim]")
    
    state["applied"] = False
    return state

# ============================================================================
# ROUTING
# ============================================================================

def should_apply_changes(state: AgentState) -> Literal["apply", "reject"]:
    """Decide si aplicar o rechazar cambios según decisión humana"""
    if state.get("human_decision") == "accept":
        return "apply"
    return "reject"

# ============================================================================
# CONSTRUCCIÓN DEL GRAFO
# ============================================================================

def build_graph():
    """Construye el grafo de LangGraph"""
    
    workflow = StateGraph(AgentState)
    
    # Añadir nodos
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("find_docs", find_affected_docs_node)
    workflow.add_node("propose", propose_changes_node)
    workflow.add_node("review", human_review_node)
    workflow.add_node("apply", apply_changes_node)
    workflow.add_node("reject", reject_node)
    
    # Definir flujo
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "find_docs")
    workflow.add_edge("find_docs", "propose")
    workflow.add_edge("propose", "review")
    
    # Branching condicional después de review
    workflow.add_conditional_edges(
        "review",
        should_apply_changes,
        {
            "apply": "apply",
            "reject": "reject"
        }
    )
    
    # Ambos caminos terminan
    workflow.add_edge("apply", END)
    workflow.add_edge("reject", END)
    
    return workflow.compile()

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    
    console.print("\n[bold magenta]🤖 Doc Update Agent v1.0[/bold magenta]\n")
    
    # Buscar US files en /backlog/done/
    done_files = list(BACKLOG_DONE_PATH.glob("*.md"))
    
    if not done_files:
        console.print("[yellow]⚠️  No hay User Stories en /backlog/done/[/yellow]")
        console.print(f"   Ruta: {BACKLOG_DONE_PATH}")
        return
    
    console.print(f"[green]✓[/green] Encontradas {len(done_files)} US en /backlog/done/\n")
    
    # Mostrar lista de US disponibles
    console.print("[bold cyan]User Stories disponibles:[/bold cyan]\n")
    for i, file in enumerate(done_files, 1):
        console.print(f"  {i}. {file.name}")
    
    console.print()
    
    # Solicitar selección
    if len(done_files) == 1:
        selected_indices = [0]
        console.print("[yellow]Solo hay una US, procesándola automáticamente...[/yellow]\n")
    else:
        console.print("[dim]Opciones:[/dim]")
        console.print("  • Un número: [cyan]1[/cyan]")
        console.print("  • Varios separados por coma: [cyan]1,3,5[/cyan]")
        console.print("  • Todas: [cyan]all[/cyan] o [cyan]todas[/cyan]\n")
        
        selection = Prompt.ask(
            "¿Qué User Stories quieres procesar?",
            default="all"
        )
        console.print()
        
        # Parsear selección
        if selection.lower() in ["all", "todas", "todo"]:
            selected_indices = list(range(len(done_files)))
            console.print(f"[yellow]📦 Procesando todas las US ({len(done_files)})...[/yellow]\n")
        else:
            # Parsear números separados por coma
            try:
                numbers = [int(n.strip()) for n in selection.split(",")]
                selected_indices = [n - 1 for n in numbers if 1 <= n <= len(done_files)]
                
                if not selected_indices:
                    console.print("[red]❌ Selección inválida[/red]")
                    return
                    
                console.print(f"[yellow]📦 Procesando {len(selected_indices)} US seleccionadas...[/yellow]\n")
            except ValueError:
                console.print("[red]❌ Formato inválido. Usa números separados por coma (ej: 1,3,5)[/red]")
                return
    
    # Construir grafo una vez
    graph = build_graph()
    
    # Lista para almacenar US aceptadas
    accepted_us_states = []
    
    # Procesar cada US seleccionada
    for idx, us_index in enumerate(selected_indices, 1):
        us_file = str(done_files[us_index])
        us_content = read_file(us_file)
        
        if len(selected_indices) > 1:
            console.print("\n" + "="*70)
            console.print(f"[bold magenta]📋 US {idx}/{len(selected_indices)}[/bold magenta]")
            console.print("="*70)
        
        console.print(f"\n[cyan]📋 Procesando:[/cyan] {Path(us_file).name}\n")
        
        # Estado inicial
        initial_state: AgentState = {
            "us_file": us_file,
            "us_content": us_content,
            "analysis": {},
            "affected_docs": [],
            "proposals": [],
            "human_decision": "reject",
            "applied": False,
            "acceptance_reason": ""
        }
        
        try:
            final_state = graph.invoke(initial_state)
            
            console.print("\n" + "="*70)
            if final_state.get("applied"):
                console.print("[bold green]✅ Proceso completado: Cambios aplicados[/bold green]")
                accepted_us_states.append(final_state)
            else:
                console.print("[bold yellow]ℹ️  Proceso completado: Sin cambios[/bold yellow]")
            console.print("="*70 + "\n")
            
        except Exception as e:
            console.print(f"\n[bold red]❌ Error procesando {Path(us_file).name}:[/bold red] {str(e)}")
            
            if len(selected_indices) > 1:
                continuar = Prompt.ask(
                    "¿Continuar con las siguientes US?",
                    choices=["si", "no"],
                    default="si"
                )
                if continuar.lower() == "no":
                    break
            else:
                raise
    
    # Si hay US aceptadas, archivarlas
    if accepted_us_states:
        console.print("\n" + "="*70)
        console.print(f"[bold magenta]📦 {len(accepted_us_states)} US aceptadas para archivar[/bold magenta]")
        console.print("="*70 + "\n")
        
        # Mostrar resumen de US aceptadas
        console.print("[cyan]US aceptadas:[/cyan]")
        for state in accepted_us_states:
            us_id = state["analysis"].get("us_id", "US-XXX")
            us_title = state["analysis"].get("title", "Sin título")
            console.print(f"  • {us_id}: {us_title}")
        
        console.print()
        
        # Decidir si usar mismo release o releases separados
        if len(accepted_us_states) > 1:
            release_mode = Prompt.ask(
                "¿Cómo quieres archivar estas US?",
                choices=["mismo", "separados"],
                default="mismo"
            )
        else:
            release_mode = "mismo"
        
        if release_mode == "mismo":
            # Elegir release UNA SOLA VEZ
            version, date_str = choose_release()
            
            console.print(f"\n[bold cyan]📦 Archivando todas las US en release-{version}_{date_str}...[/bold cyan]\n")
            
            # Archivar cada US aceptada en el mismo release
            for state in accepted_us_states:
                us_file = state["us_file"]
                us_id = state["analysis"].get("us_id", "US-XXX")
                us_title = state["analysis"].get("title", "Sin título")
                acceptance_reason = state.get("acceptance_reason", "Cambios aprobados")
                
                # Archivar US
                new_path = archive_us_to_release(us_file, version, date_str, us_id, us_title, state["proposals"])
                
                console.print(f"[green]✓[/green] {us_id} archivada")
                
                # Registrar aceptación
                log_path = register_acceptance(
                    us_file=us_file,
                    us_id=us_id,
                    us_title=us_title,
                    affected_docs=state["affected_docs"],
                    proposals=state["proposals"],
                    reason=acceptance_reason,
                    version=version,
                    release_date=date_str
                )
            
            console.print(f"\n[bold green]✅ Todas las US archivadas en release-{version}_{date_str}[/bold green]")
            console.print(f"[green]✓[/green] Registro guardado en: {Path(log_path).relative_to(BASE_PATH)}")
        
        else:  # releases separados
            console.print("\n[bold cyan]📦 Archivando US en releases separados...[/bold cyan]\n")
            
            for idx, state in enumerate(accepted_us_states, 1):
                us_file = state["us_file"]
                us_id = state["analysis"].get("us_id", "US-XXX")
                us_title = state["analysis"].get("title", "Sin título")
                acceptance_reason = state.get("acceptance_reason", "Cambios aprobados")
                
                console.print(f"\n[yellow]US {idx}/{len(accepted_us_states)}: {us_id}[/yellow]")
                
                # Elegir release para esta US específica
                version, date_str = choose_release()
                
                # Archivar US
                new_path = archive_us_to_release(us_file, version, date_str, us_id, us_title, state["proposals"])
                
                console.print(f"[green]✓[/green] {us_id} archivada en release-{version}_{date_str}")
                
                # Registrar aceptación
                register_acceptance(
                    us_file=us_file,
                    us_id=us_id,
                    us_title=us_title,
                    affected_docs=state["affected_docs"],
                    proposals=state["proposals"],
                    reason=acceptance_reason,
                    version=version,
                    release_date=date_str
                )
            
            console.print(f"\n[bold green]✅ Todas las US archivadas correctamente[/bold green]")
    
    else:
        console.print("\n[yellow]ℹ️  No hay US aceptadas para archivar[/yellow]")

if __name__ == "__main__":
    main()