#!/bin/bash

# Vai para o diretório do script
cd "$(dirname "$0")"

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload