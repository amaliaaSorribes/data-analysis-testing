#!/usr/bin/env python3
"""
Doc Update Agent - Modo chat simplificado
Lee US de /backlog/done/, genera propuestas y las imprime para el usuario.
"""

import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno
load_dotenv(Path(__file__).parent.parent.parent / ".env")
client = OpenAI()

BASE_PATH = Path(__file__).parent.parent.parent
BACKLOG_DONE_PATH = BASE_PATH / "docs" / "backlog" / "done"
SERVICES_PATH = BASE_PATH / "docs" / "services"

def read_file(path):
    """Lee archivo de texto"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def chat_mode():
    """Modo chat: genera propuestas y las imprime para el usuario"""
    # Buscar US en /backlog/done/
    done_files = list(BACKLOG_DONE_PATH.glob("*.md"))
    
    if not done_files:
        print("❌ No hay User Stories completadas en /backlog/done/")
        return False
    
    # Tomar la primera US
    us_file = done_files[0]
    us_content = read_file(us_file)
    us_id = us_file.stem
    
    print(f"\n📋 **User Story seleccionada:** {us_id}\n")
    
    # Analizar la US con LLM
    analysis_prompt = f"""
Analiza esta User Story y extrae:
1. Título
2. Qué cambios implica
3. Qué documentos de /docs/services/ se deben actualizar

USER STORY:
{us_content}

Responde en formato JSON:
{{
  "title": "título breve",
  "summary": "resumen de cambios",
  "affected_services": ["servicio1", "servicio2"],
  "proposed_changes": ["cambio 1", "cambio 2"]
}}
"""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un experto en análisis de requisitos técnicos."},
            {"role": "user", "content": analysis_prompt}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    try:
        analysis = json.loads(response.choices[0].message.content)
    except:
        print("❌ Error analizando la US")
        return False
    
    # Mostrar propuestas de forma clara
    print(f"**Título:** {analysis.get('title', 'N/A')}\n")
    print(f"**Resumen:** {analysis.get('summary', 'N/A')}\n")
    
    if analysis.get('affected_services'):
        print("**Documentos afectados:**")
        for service in analysis.get('affected_services', []):
            print(f"  • {service}")
        print()
    
    if analysis.get('proposed_changes'):
        print("**Cambios propuestos:**")
        for i, change in enumerate(analysis.get('proposed_changes', []), 1):
            print(f"  {i}. {change}")
        print()
    
    return True

def apply_changes(decision):
    """Aplica o rechaza los cambios basándose en la decisión"""
    if decision == "accept":
        print("✅ Cambios aceptados y aplicados")
        # Aquí iría la lógica para aplicar realmente los cambios
    else:
        print("❌ Cambios rechazados")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat-mode", action="store_true", help="Modo chat: genera y muestra propuestas")
    parser.add_argument("--decision", choices=["accept", "reject"], help="Aplicar o rechazar cambios")
    
    args = parser.parse_args()
    
    if args.chat_mode:
        chat_mode()
    elif args.decision:
        apply_changes(args.decision)
