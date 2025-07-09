@echo off
echo Installing Python dependencies for Accounting System...
echo.

echo Installing Django and related packages...
pip install -r requirements.txt

echo.
echo Dependencies installed successfully!
echo.
echo To start the backend server, run: python manage.py runserver
echo To start the frontend, run: cd frontend && npm start
echo.
pause 