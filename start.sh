#!/bin/bash

echo "🚀 Starting project..."

# 1. Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# 2. Activate venv
source .venv/bin/activate

# 3. Install dependencies #save in requirements.txt
#pip install -r requirements.txt
#pip install fastapi uvicorn

# 4. Start FastAPI (background)
uvicorn backend.main:app --reload &

# 5. Start frontend server
cd frontend
python3 -m http.server 5500
