@echo off
cd /d %~dp0

echo Starting FastAPI server...
venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload
pause