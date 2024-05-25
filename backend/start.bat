@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Set environment variable
set FLASK_ENV=production

REM Run Gunicorn
gunicorn -w 4 wsgi:app
