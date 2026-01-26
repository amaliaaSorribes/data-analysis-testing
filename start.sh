#!/bin/bash

echo "🚀 Starting project..."

# 1️⃣ Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# 2️⃣ Activate venv
source .venv/bin/activate

# 3️⃣ Upgrade pip (opcional pero recomendable)
pip install --upgrade pip

# 4️⃣ Install dependencies
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "⚠️ requirements.txt no encontrado, instalando paquetes individuales..."
  pip install fastapi==0.111.1 uvicorn[standard]==0.23.1 python-multipart==0.0.6 markdown==3.5.2
fi

# 5️⃣ Ensure backend scripts are executable
chmod +x backend/*.py

# 6️⃣ Start FastAPI (background)
uvicorn backend.main:app --reload &

# 7️⃣ Start frontend server
cd frontend
python3 -m http.server 5500
