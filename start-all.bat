@echo off
echo Starting AI Travel Planner...
start "Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && python app.py"
timeout /t 3 /nobreak >nul
start "Frontend" cmd /k "cd /d %~dp0frontend && npm start"
echo Both servers are starting in separate windows.