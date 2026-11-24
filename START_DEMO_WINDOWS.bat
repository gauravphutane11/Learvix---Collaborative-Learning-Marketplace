@echo off
setlocal
start "Learvix Backend" cmd /k "cd /d %~dp0backend && call .venv\Scripts\activate.bat && python app.py"
start "Learvix Frontend" cmd /k "cd /d %~dp0frontend && npm install && npm run dev"
echo Learvix is starting. Open the Vite URL shown in the frontend terminal.
pause
