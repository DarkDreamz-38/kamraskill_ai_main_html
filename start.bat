@echo off
REM ============================================================
REM  KarmaSkill AI - one-click launcher
REM  Starts the FastAPI backend (port 8000) and the static
REM  frontend (port 8090) in separate windows.
REM ============================================================

cd /d "%~dp0"

echo Starting KarmaSkill AI...
echo.

REM --- Backend (FastAPI on port 8000) ---
start "KarmaSkill Backend (8000)" cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000"

REM --- Frontend (static server on port 8090) ---
start "KarmaSkill Frontend (8090)" cmd /k "python -m http.server 8090 --directory frontend\public"

REM Give the backend a moment to boot
timeout /t 4 /nobreak >nul

echo.
echo  Backend : http://localhost:8000  (health: /health)
echo  Frontend: http://localhost:8090/login.html
echo.
echo  Login ID: nexus123   Password: 1234
echo.
echo Opening the portal in your browser...
start http://localhost:8090/login.html

echo Done. Close the two server windows to stop the app.
