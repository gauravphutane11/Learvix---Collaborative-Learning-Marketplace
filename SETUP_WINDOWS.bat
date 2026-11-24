@echo off
setlocal
cd /d "%~dp0backend"
py -m venv .venv
call .venv\Scripts\activate.bat
if not exist .env copy .env.example .env
python -m pip install --upgrade pip
pip install -r requirements.txt
python seed.py
echo.
echo Backend setup complete. Start backend with START_DEMO_WINDOWS.bat
pause
