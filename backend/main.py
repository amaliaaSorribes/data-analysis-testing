import re, shutil, os, datetime, markdown
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

BACKLOG_PATH = Path("docs/backlog")
MEETINGS_PATH = Path("docs/meetings")

STATES = ["to-do", "in-progress", "done"]

chat_state = {
    "awaiting_story_id": False,
    "waiting_for_date": False,
    "current_meeting_date": None,

    "changing_state": False,
    "selected_us_file": None
}

# ----------------- Funciones auxiliares ----------------- #

def create_meeting_folder(date: str) -> str:
    """Crea la carpeta del meeting si no existe"""
    folder_name = f"meeting-{date}"
    path = MEETINGS_PATH / folder_name
    path.mkdir(parents=True, exist_ok=True)
    return folder_name

def save_md_file(file: UploadFile, folder_name: str):
    """Guarda el archivo .md dentro de la carpeta del meeting"""
    file_path = MEETINGS_PATH / folder_name / "transcript.md"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def list_backlog() -> str:
    """Genera un listado del backlog"""
    items = []
    dirs = sorted([p for p in BACKLOG_PATH.iterdir() if p.is_dir()])
    files = sorted([p for p in BACKLOG_PATH.iterdir() if p.is_file()])

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

    return "\n".join(items)

def list_meetings() -> str:
    """Genera un listado de los meetings"""
    items = []
    dirs = sorted([p for p in MEETINGS_PATH.iterdir() if p.is_dir()])
    files = sorted([p for p in MEETINGS_PATH.iterdir() if p.is_file()])

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

    return "\n".join(items)

def render_md(md_text: str) -> str:
    return markdown.markdown(md_text)

def search_user_story(story_id: str) -> dict:
    for file in BACKLOG_PATH.rglob("*"):
        if file.is_file() and story_id.lower() in file.name.lower():
            html = render_md(file.read_text(encoding="utf-8"))

            return {
                "response_html": f"{html}"
            }

    return {
        "response": f"❌ No encontré ninguna user story con id {story_id}."
    }

def find_user_story(story_id: str):
    for state in STATES:
        state_path = BACKLOG_PATH / state
        if not state_path.exists():
            continue

        for file in state_path.iterdir():
            if file.is_file() and story_id in file.name:
                return file, state

    return None, None

# ----------------- Endpoints ----------------- #

@app.get("/")
def root():
    return {"msg": "Backend activo 🚀"}

@app.post("/upload-md")
def upload_md(file: UploadFile = File(...)):
    date = chat_state.get("current_meeting_date")
    if not date:
        raise HTTPException(status_code=400, detail="Primero dime la fecha del meeting antes de subir el archivo.")
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos .md")

    folder_name = create_meeting_folder(date)
    save_md_file(file, folder_name)
    chat_state["current_meeting_date"] = None

    # --- Ejecutar agente ---
    try:
        # Guardamos la ruta actual
        cwd = os.getcwd()
        os.chdir("agents/us_creator")
        result = os.system("python3 US_creator_agent.py "+folder_name)
        os.chdir(cwd)

        if result != 0:
            raise Exception("Error ejecutando US_creator_agent.py")
    except Exception as e:
        return {"message": f"❌ Hubo un problema ejecutando el agente: {e}"}

    return {"message": f"✅ Meeting creado, transcript.md subido y agente ejecutado correctamente en {folder_name}"}

@app.post("/chat")
def chat(msg: Message):
    text = msg.message.strip().lower()

    if text == "exit" or text == "quit":
        chat_state["awaiting_story_id"] = False
        chat_state["waiting_for_date"] = False
        chat_state["current_meeting_date"] = None
        return {
            "response": "🔄 Estás de vuelta en el menú principal",
            "show_options": True,
            "enable_upload": False
        }

    # --- Buscar US ---
    if chat_state["awaiting_story_id"]:
        chat_state["awaiting_story_id"] = False
        return search_user_story(text)

    # --- Esperando fecha para nuevo meeting ---
    if chat_state["waiting_for_date"]:
        try:
            datetime.datetime.strptime(text, "%Y-%m-%d")
            folder_name = f"meeting-{text}"
            path = MEETINGS_PATH / folder_name

            if path.exists():
                return {"response": f"⚠️ Ya existe un meeting para la fecha {text}. Prueba con otra fecha."}

            chat_state["current_meeting_date"] = text
            chat_state["waiting_for_date"] = False

            return {"response": "✅ Fecha recibida. Ahora sube tu transcript en formato .md para crear el meeting 📄", 
                    "enable_upload": True}

        except ValueError:
            return {"response": "❌ Formato incorrecto. Usa YYYY-MM-DD (ej: 2025-01-02)"}

    # --- Cambiar estado de una US ---
    if chat_state["changing_state"] and not chat_state["selected_us_file"]:
        file, state = find_user_story(text)

        if not file:
            return {"response": "❌ No encontré esa User Story."}

        chat_state["selected_us_file"] = (file, state)

        if state == "to-do":
            return {"response": "📌 La US está en TO-DO. ¿Quieres subir su estado? (si/no)"}
        elif state == "done":
            return {"response": "📌 La US está en DONE. ¿Quieres bajar su estado? (si/no)"}
        else:
            return {"response": "📌 La US está en IN-PROGRESS. ¿Quieres subir o bajar su estado?"}

    # --- Confirmar cambio de estado ---
    if chat_state["selected_us_file"]:
        file, state = chat_state["selected_us_file"]

        direction = None
        if state in ["to-do", "done"]:
            if text in ["si", "yes", "ok"]:
                direction = "up" if state == "to-do" else "down"
            else:
                chat_state["changing_state"] = False
                chat_state["selected_us_file"] = None
                return {"response": "❎ Cambio cancelado"}
        else: 
            if "sub" in text:
                direction = "up"
            elif "baj" in text:
                direction = "down"
            else:
                return {"response": "❓ Responde con subir o bajar."}

        idx = STATES.index(state)

        if direction == "up" and idx < len(STATES) - 1:
            new_state = STATES[idx + 1]
        elif direction == "down" and idx > 0:
            new_state = STATES[idx - 1]
        else:
            return {"response": "⚠️ No se puede mover la US en esa dirección."}

        new_path = BACKLOG_PATH / new_state / file.name
        shutil.move(str(file), new_path)

        chat_state["changing_state"] = False
        chat_state["selected_us_file"] = None

        return {
            "response": f"✅ US movida de {state.upper()} a {new_state.upper()}"
        }

    # --- Menú principal ---
    match = re.search(r"\b[1-6]|opciones\b", text)
    if not match:
        return {"response": "❌ Por favor elige un número del 1-6 o escribe 'opciones' para ver el menú."}

    option = match.group()

    if option == "opciones":
        return {"show_options": True}
    elif option == "1":
        chat_state["waiting_for_date"] = True
        return {"response": "Para añadir un meeting, dime la fecha en formato YYYY-MM-DD 📅"}
    elif option == "2":
        return {"response": "Contenido de meetings:\n\n" + list_meetings()}
    elif option == "3":
        return {"response": "Contenido del backlog:\n\n" + list_backlog()}
    elif option == "4":
        chat_state["awaiting_story_id"] = True
        return {"response": "🔎 ¿Qué user story quieres buscar? Introduce el ID."}
    elif option == "5":
        chat_state["changing_state"] = True
        return {"response": "🔁 ¿Qué User Story quieres cambiar de estado? Introduce el ID."}
    elif option == "6":
        return {"response": "🐞 Esta opción aún no está implementada."}