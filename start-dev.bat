@echo off
echo ========================================
echo Basey Fare Guide - Starting Servers
echo ========================================
echo.

cd "%~dp0"

echo [1/2] Starting Django Backend...
start cmd /k ".\BFG-env\Scripts\Activate.ps1 && python manage.py runserver"

timeout /t 3 /nobreak > nul

echo [2/2] Starting React Frontend...
start cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Servers are starting!
echo ========================================
echo.
echo Django Backend: http://localhost:8000
echo React Frontend: http://localhost:3000
echo Django Admin:   http://localhost:8000/admin
echo.
echo Press any key to exit this window...
pause > nul
