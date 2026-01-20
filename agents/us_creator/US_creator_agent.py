import os
from openai import OpenAI

TEMPLATE_FILE = "plantilla_funcional.md"

MEETINGS_PATH = "../../docs/meetings/meeting-2025-02-18"
TRANSCRIPT_FILE = os.path.join(MEETINGS_PATH, "transcript.md")
OUTPUT_FILE = os.path.join(MEETINGS_PATH, "funcional.md")

client = OpenAI()  # usa OPENAI_API_KEY del entorno

SYSTEM_PROMPT = """
Eres un agente de documentación funcional.

Tu tarea es:
- Leer un transcript de una reunión en formato Markdown.
- Leer una plantilla de documento funcional en Markdown.
- Rellenar la plantilla usando únicamente información explícita presente en el transcript.

Reglas estrictas:
- NO inventes información.
- NO hagas suposiciones.
- NO completes secciones si el transcript no contiene información clara.
- Si una sección no puede completarse, elimina esa sección del documento final.
- Guardar fecha en el título del documento funcional según la fecha de la reunión (2025-02-18).

Objetivo:
Generar un nuevo documento funcional claro, estructurado y fiel al contenido del transcript.
"""


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_functional_doc(transcript, template):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
TRANSCRIPT:
----------------
{transcript}

PLANTILLA:
----------------
{template}

Genera el documento funcional final en Markdown.
"""
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

BACKLOG_PATH = "../../docs/backlog"
US_OUTPUT_FILE = os.path.join(BACKLOG_PATH, "US.md")

US_SYSTEM_PROMPT = """
Eres un agente que genera User Stories de backlog a partir de documentación funcional.

Tu tarea:
- Leer un documento funcional en Markdown.
- Extraer la información esencial para generar una User Story completa.
- Solo usa información presente en el funcional, no inventes nada.
- Salida en Markdown limpia.

Formato obligatorio de User Story a rellenar:

# US- <ID> - [Título breve]

---

## Identificación

- **ID:** 
- **Fecha:**   
- **Servicio:** cart-service

---

## User Story

[Como <rol> quiero <objetivo> para <beneficio>.]

---

## Descripción

[breve descripción del requerimiento con solución propuesta]

---

## Cambios

### Qué se añadió

---

## Impacto en APIs

### Nuevo endpoint

"""

def generate_user_story(funcional_doc):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": US_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
DOCUMENTO FUNCIONAL:
----------------
{funcional_doc}

Genera la User Story en Markdown.
"""
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content


def main():
    generar = True

    if os.path.exists(OUTPUT_FILE):
        respuesta = input(f"El archivo {OUTPUT_FILE} ya existe. ¿Quieres actualizarlo? (y/n): ").strip().lower()
        if respuesta != "y":
            print("Se mantiene el funcional existente")
            funcional_doc = read_file(OUTPUT_FILE)
            generar = False

    if generar:
        print("Generando documento funcional...")
        transcript = read_file(TRANSCRIPT_FILE)
        template = read_file(TEMPLATE_FILE)
        funcional_doc = generate_functional_doc(transcript, template)
        write_file(OUTPUT_FILE, funcional_doc)
        print(f"Documento funcional generado en {OUTPUT_FILE}")

    # Generar User Story
    if os.path.exists(US_OUTPUT_FILE):
        respuesta = input(f"El archivo {US_OUTPUT_FILE} ya existe. ¿Quieres actualizarlo? (y/n): ").strip().lower()
        if respuesta != "y":
            print("Se mantiene el user story existente") 
            return
        else:
            print("Generando User Story...")
            user_story_md = generate_user_story(funcional_doc)
            write_file(US_OUTPUT_FILE, user_story_md)
            print(f"User Story generada en {US_OUTPUT_FILE}")


if __name__ == "__main__":
    main()
