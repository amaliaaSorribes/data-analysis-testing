# Doc Update Agent

Agente automático que actualiza la documentación de microservicios (`/docs/services/`) cuando se completan User Stories.

## 🎯 Funcionamiento

1. Detecta User Stories completadas en `/docs/backlog/done/`
2. Analiza los cambios técnicos que implican
3. Identifica qué documentos de `/docs/services/` deben actualizarse
4. Propone modificaciones específicas
5. **Solicita aprobación humana**
6. Aplica cambios si se aceptan

## 🚀 Instalación

```bash
# Desde la raíz del proyecto
cd agents/doc_updater

# Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY