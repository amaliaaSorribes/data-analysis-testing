import os
import re
import json
from openai import OpenAI

DOCS_PATH = "docs"
OUTPUT_FILE = "data.json"

client = OpenAI()  # usa OPENAI_API_KEY del entorno


SYSTEM_PROMPT = """
Eres un agente que analiza documentación técnica en Markdown y los convierte a JSON.

Tu objetivo es entender el contenido y extraer la información
más relevante sin imponer una estructura artificial.

Instrucciones:
- Identifica qué tipo de documento es (guía, referencia, concepto, tutorial, etc.)
- Detecta la estructura real del documento si existe
- Resume las ideas principales con tus propias palabras
- Extrae conceptos clave, términos técnicos y relaciones importantes
- Si el documento no tiene secciones claras, no las inventes

Devuelve un JSON válido que represente fielmente el contenido.
La estructura del JSON puede variar según el documento, pero debe:
- ser coherente
- ser fácil de consumir por otro agente
- no perder información relevante

Incluye siempre:
- "summary": resumen general del documento
- "topics": lista de conceptos o temas principales

No añadas texto fuera del JSON.
No expliques el resultado.

"""


def analyze_markdown(markdown_text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # rápido y suficiente para docs
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": markdown_text}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    content = re.sub(r"```json\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"\s*```", "", content)

    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"❌ JSON inválido devuelto por el LLM:\n{content}"
        ) from e


def run_agent():
    documents = []

    for file in os.listdir(DOCS_PATH):
        if not file.endswith(".md"):
            continue

        path = os.path.join(DOCS_PATH, file)

        with open(path, "r", encoding="utf-8") as f:
            markdown = f.read()

        extracted = analyze_markdown(markdown)

        documents.append({
            "doc_title": os.path.splitext(file)[0],
            "source": path,
            **extracted
        })

        print(f"✅ Procesado: {file}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"documents": documents}, f, indent=2, ensure_ascii=False)

    print(f"\n🔥 data.json generado con {len(documents)} documentos")


if __name__ == "__main__":
    run_agent()
