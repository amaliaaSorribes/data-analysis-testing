import os
from openai import OpenAI

TEMPLATE_FILE = "plantilla_funcional.md"

MEETINGS_PATH = "../../meetings/meeting-2025-02-18"
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


def main():
    # si el archivo ya existe
    if os.path.exists(OUTPUT_FILE):
        respuesta = input(
            f"El archivo {OUTPUT_FILE} ya existe. ¿Quieres actualizarlo? (y/n): "
        ).strip().lower()
        if respuesta != "y":
            print("Se mantiene el funcional existente")
            return

    transcript = read_file(TRANSCRIPT_FILE)
    template = read_file(TEMPLATE_FILE)

    funcional_md = generate_functional_doc(transcript, template)
    write_file(OUTPUT_FILE, funcional_md)

    print(f"Documento funcional generado en {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
