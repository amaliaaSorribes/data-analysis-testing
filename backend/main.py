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

@app.get("/")
def root():
    return {"msg": "Backend activo 🚀"}

@app.post("/chat")
def chat(msg: Message):
    text = msg.message.lower()

    # Buscar un número del 1 al 4 en el mensaje
    match = re.search(r"\b[1-4]\b", text)

    if not match:
        return {"response": ("Porfavor elige un número del 1-4\n")}

    option = match.group()

    if option == "1":
        return {"response": "🐞 Esta opción aún no está implementada."}

    if option == "2":
        return {"response": "🐞 Esta opción aún no está implementada."}

    if option == "3":
        return {"response": "🐞 Esta opción aún no está implementada."}

    if option == "4":
        return {"response": "🐞 Esta opción aún no está implementada."}
