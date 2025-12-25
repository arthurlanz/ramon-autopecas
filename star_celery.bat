@echo off
echo ========================================
echo  RAMON AUTOPECAS - CELERY WORKER
echo ========================================
echo.

call venv\Scripts\activate

REM Iniciar Celery Worker
start "Celery Worker" celery -A config worker -l info --pool=solo

REM Iniciar Celery Beat
start "Celery Beat" celery -A config beat -l info

echo.
echo Celery Worker e Beat iniciados!
echo.
pause
