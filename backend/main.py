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

chat_state = {
    "awaiting_story_id": False,
    "waiting_for_date": False,
    "current_meeting_date": None
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
        if file.is_file() and story_id in file.name:
            html = render_md(file.read_text(encoding="utf-8"))

            return {
                "response_html": f"{html}"
            }

    return {
        "response": f"❌ No encontré ninguna user story con id {story_id}."
    }
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
        result = os.system("python3 US_creator_agent_individual.py "+folder_name)
        os.chdir(cwd)

        if result != 0:
            raise Exception("Error ejecutando US_creator_agent_individual.py")
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
            "show_options": False,
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

    # --- Menú principal ---
    match = re.search(r"\b[1-5]|opciones\b", text)
    if not match:
        return {"response": "❌ Por favor elige un número del 1-5 o escribe 'opciones' para ver el menú."}

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
        return {"response": "🐞 Esta opción aún no está implementada."}