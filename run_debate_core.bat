@echo off
setlocal

echo ==========================================
echo    DEBATE CORE - STARTUP LAUNCHER
echo ==========================================
echo.

:: Get the current directory
set BASE_DIR=%~dp0

:: Close any existing terminals from previous runs (optional but cleaner)
taskkill /FI "WINDOWTITLE eq DEBATE-CORE-*" /F > nul 2>&1

:: Launch Backend in a new window
echo [SERVER] Starting Backend (Python)...
start "DEBATE-CORE-BACKEND" cmd /c "cd /d %BASE_DIR%backend && echo Starting Backend... && .\venv\Scripts\python.exe app.py || pause"

:: Wait for backend
echo.
echo Waiting for backend to initialize...
timeout /t 3 /nobreak > nul

:: Launch Frontend in a new window
echo [UI] Starting Frontend (Vite)...
start "DEBATE-CORE-FRONTEND" cmd /c "cd /d %BASE_DIR%frontend && echo Starting Frontend... && npm run dev || pause"

echo.
echo ==========================================
echo  Frontend: http://localhost:5173
echo  Backend:  http://localhost:8000
echo ==========================================
echo.
echo Launching browser in 5 seconds...
timeout /t 5 /nobreak > nul
start http://localhost:5173

:: This main window closes safely
exit
