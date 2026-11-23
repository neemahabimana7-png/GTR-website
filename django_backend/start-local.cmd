@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Create the virtual environment first. See README.md.
  exit /b 1
)
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
