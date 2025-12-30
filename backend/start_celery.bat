@echo off
echo ========================================
echo RAMON AUTOPECAS - CELERY WORKER
echo ========================================
echo.

call venv\Scripts\activate

REM Iniciar Celery Worker em nova janela
start "Celery Worker" cmd /k "celery -A config worker -l info --pool=solo"

REM Aguardar 2 segundos
timeout /t 2 /nobreak >nul

REM Iniciar Celery Beat em nova janela
start "Celery Beat" cmd /k "celery -A config beat -l info"

echo.
echo Celery Worker e Beat iniciados em janelas separadas!
echo.
echo Para parar, feche as janelas ou pressione CTRL+C em cada uma.
echo.
pause
