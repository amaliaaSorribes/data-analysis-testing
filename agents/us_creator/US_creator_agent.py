import os, re
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

def append_file(path, content):
    with open(path, "a", encoding="utf-8") as f:
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

PATHS_TO_SCAN = ["../../docs/releases", "../../docs/backlog"]

def next_us_id(paths=PATHS_TO_SCAN):
    ids = []

    for base_path in paths:
        for _, _, files in os.walk(base_path):
            for file in files:
                match = re.match(r"US-(\d+).*\.md", file)
                if match:
                    ids.append(int(match.group(1)))

    return str(max(ids) + 1) if ids else "101"

US_ID = next_us_id()

US_SYSTEM_PROMPT = f"""
Eres un agente que genera User Stories de backlog a partir de documentación funcional.

Tu tarea:
- Leer un documento funcional en Markdown.
- Extraer la información esencial para generar una User Story completa.
- Solo usa información presente en el funcional, no inventes nada.
- Salida en Markdown limpia.

Formato obligatorio de User Story a rellenar:

# US-{US_ID} - [Título muy breve en inglés]

---

## Identificación

- **ID:** US-{US_ID}
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

def extract_us_title(markdown):
    match = re.search(r"^#\s+US-\d+\s+-\s+(.+)$", markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "untitled"

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text.strip("_")

LINK_FUNCIONAL = f"""

---

## Referencias

- Documento funcional: [`funcional.md`]({OUTPUT_FILE})
"""

def main():
    for root, _, files in os.walk(MEETINGS_PATH):
        print(f"\nProcesando transcript de reunión en {root}")
        if "funcional.md" not in files:
            print("\nGenerando documento funcional...")
            transcript = read_file(TRANSCRIPT_FILE)
            template = read_file(TEMPLATE_FILE)
            funcional_doc = generate_functional_doc(transcript, template)
            write_file(OUTPUT_FILE, funcional_doc)
            print(f"Documento funcional generado en {OUTPUT_FILE}")

            print("\nGenerando User Story...")
            user_story_md = generate_user_story(funcional_doc)

            title = extract_us_title(user_story_md)
            slug = slugify(title)

            us_filename = f"US-{US_ID}_{slug}.md"
            us_path = os.path.join(BACKLOG_PATH, us_filename)

            write_file(us_path, user_story_md)
            append_file(us_path, LINK_FUNCIONAL)

            print(f"User Story generada en {us_path}")
        else:
            print("Documento funcional y user story ya existen, saltando generación.")

if __name__ == "__main__":
    main()
