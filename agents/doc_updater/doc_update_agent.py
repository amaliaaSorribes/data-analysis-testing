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

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))  

console = Console()

# Rutas relativas desde este script
BASE_PATH = Path(__file__).parent.parent.parent
BACKLOG_DONE_PATH = BASE_PATH / "docs" / "backlog" / "done"
SERVICES_PATH = BASE_PATH / "docs" / "services"

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
        model="gpt-4o",
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
            model="gpt-4o",
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

def apply_changes_node(state: AgentState) -> AgentState:
    """
    Nodo 5: APPLIER
    Aplica los cambios a los archivos si fueron aceptados
    """
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
            model="gpt-4o",
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
    
    return state

def reject_node(state: AgentState) -> AgentState:
    """
    Nodo alternativo: REJECT
    Termina sin aplicar cambios
    """
    console.print("\n[bold yellow]❌ Cambios rechazados. No se modificó ningún archivo.[/bold yellow]")
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
    
    # Por ahora procesamos la primera
    # TODO: permitir selección o procesamiento en batch
    us_file = str(done_files[0])
    us_content = read_file(us_file)
    
    console.print(f"[cyan]📋 Procesando:[/cyan] {Path(us_file).name}\n")
    
    # Estado inicial
    initial_state: AgentState = {
        "us_file": us_file,
        "us_content": us_content,
        "analysis": {},
        "affected_docs": [],
        "proposals": [],
        "human_decision": "reject",
        "applied": False
    }
    
    # Construir y ejecutar grafo
    graph = build_graph()
    
    try:
        final_state = graph.invoke(initial_state)
        
        console.print("\n" + "="*70)
        if final_state.get("applied"):
            console.print("[bold green]✅ Proceso completado: Cambios aplicados[/bold green]")
        else:
            console.print("[bold yellow]ℹ️  Proceso completado: Sin cambios[/bold yellow]")
        console.print("="*70 + "\n")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        raise

if __name__ == "__main__":
    main()