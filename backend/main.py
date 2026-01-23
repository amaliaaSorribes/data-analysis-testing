from pathlib import Path
import re
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # SOLO para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

BACKLOG_PATH = Path("docs/backlog")
conversation_state = {"awaiting_story_id": False}

@app.get("/")
def root():
    return {"msg": "Backend activo 🚀"}

@app.post("/chat")
def chat(msg: Message):
    text = msg.message.strip().lower()

    # 🟡 Paso 2: esperando ID de user story
    if conversation_state["awaiting_story_id"]:
        conversation_state["awaiting_story_id"] = False

        story_id = text

        for file in BACKLOG_PATH.rglob("*"):
            if file.is_file() and story_id in file.name:
                content = file.read_text(encoding="utf-8")

                return {
                    "response": (
                        f"<b>📄 {file.name}</b>\n\n"
                        + content
                    )
                }

        return {"response": f"❌ No encontré ninguna user story con id {story_id}."}

    # 🟢 Menú principal
    match = re.search(r"\b[1-4]\b", text)
    if not match:
        return {"response": "Por favor elige un número del 1-4"}

    option = match.group()

    if option == "1":
        return {"response": "🐞 Esta opción aún no está implementada."}

    if option == "2":
        dirs = sorted([p for p in BACKLOG_PATH.iterdir() if p.is_dir()])
        files = sorted([p for p in BACKLOG_PATH.iterdir() if p.is_file()])

        items = []

        for d in dirs:
            items.append(f"📁 {d.name}")
            inner_files = sorted([f for f in d.iterdir() if f.is_file()])

            if inner_files:
                for f in inner_files:
                    items.append(f"  └─ 📄 {f.name}")
            else:
                items.append("  └─ (vacía)")

        for f in files:
            items.append(f"📄 {f.name}")

        return {
            "response": (
                "Contenido del backlog:\n\n"
                + "\n".join(items)
            )
        }

    # 🟢 OPCIÓN 3 — buscar user story por ID
    if option == "3":
        conversation_state["awaiting_story_id"] = True
        return {
            "response": "🔎 ¿Qué user story quieres buscar? Introduce el ID."
        }

    if option == "4":
        return {"response": "🐞 Esta opción aún no está implementada."}
