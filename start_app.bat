@echo off
echo Starting Account Management Module...
echo.

echo Starting Django Backend...
start "Django Backend" cmd /k "cd /d %~dp0 && python manage.py runserver"

echo Starting React Frontend...
start "React Frontend" cmd /k "cd /d %~dp0frontend && npm install && npm start"

echo.
echo Both servers are starting...
echo Backend will be available at: http://127.0.0.1:8000
echo Frontend will be available at: http://localhost:3000
echo.
pause 