@echo off
title Enigma Admin Portal ^& Backend
echo ========================================================
echo    KHOI CHAY ENIGMA ADMIN PORTAL KET NOI SUPABASE (8000)
echo ========================================================
echo.
echo 1. Ket noi co so du lieu Supabase PostgreSQL thanh cong!
echo 2. Dang mo giao dien Quan Tri tai: http://localhost:8000/admin-portal/
echo.
timeout /t 2 /nobreak >nul
start "" "http://localhost:8000/admin-portal/"
cd /d "%~dp0backend"
if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
) else (
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
)
pause
