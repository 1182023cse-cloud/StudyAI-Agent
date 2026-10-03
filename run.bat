@echo off
title StudyAI Agent

echo ==========================================
echo        STUDYAI AGENT STARTING...
echo ==========================================
echo.

cd /d "%~dp0"

echo Starting Backend...
start "StudyAI Backend" cmd /k "call ..\venv\Scripts\activate.bat && cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend...
start "StudyAI Frontend" cmd /k "call ..\venv\Scripts\activate.bat && streamlit run frontend/app.py"

echo.
echo ==========================================
echo Backend:  http://127.0.0.1:5000
echo Frontend: http://localhost:8501
echo ==========================================
echo.

pause