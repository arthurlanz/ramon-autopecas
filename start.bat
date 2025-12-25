@echo off
echo ========================================
echo  RAMON AUTOPECAS - INICIAR BACKEND
echo ========================================
echo.

REM Ativar ambiente virtual
call venv\Scripts\activate

REM Rodar migrações
echo [1/4] Executando migrações...
python manage.py makemigrations
python manage.py migrate

REM Criar superuser se não existir
echo.
echo [2/4] Verificando superuser...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@ramonautopecas.com', 'admin123', role='owner')"

REM Coletar arquivos estáticos
echo.
echo [3/4] Coletando arquivos estáticos...
python manage.py collectstatic --noinput

REM Iniciar servidor
echo.
echo [4/4] Iniciando servidor...
echo.
echo ========================================
echo  Servidor rodando em http://localhost:8000
echo  Admin em http://localhost:8000/admin
echo  User: admin / Password: admin123
echo ========================================
echo.

python manage.py runserver
