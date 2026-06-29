@echo off
echo Starting VeriQAI Review UI...

:: Install backend dependencies (fastapi, uvicorn, python-dotenv)
echo Installing backend dependencies...
python -m pip install -r "%~dp0backend\requirements.txt"

:: Check for node_modules
if not exist "%~dp0frontend\node_modules" (
    echo Installing frontend dependencies...
    cd /d "%~dp0frontend"
    call npm install
    cd /d "%~dp0"
)

:: Start FastAPI backend in background
start "VeriQAI Backend" cmd /k "cd /d "%~dp0backend" && uvicorn main:app --reload --port 8000"

:: Wait a moment then open frontend dev server
timeout /t 2 /nobreak >nul
start "VeriQAI Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

:: Open browser after another moment
timeout /t 3 /nobreak >nul
start http://localhost:5173
