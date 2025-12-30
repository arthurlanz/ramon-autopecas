@echo off
echo ========================================
echo RAMON AUTOPECAS - INICIAR BACKEND
echo ========================================
echo.

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate

REM Verificar se ativou
if errorlevel 1 (
    echo ERRO: Nao foi possivel ativar o ambiente virtual!
    echo Execute: python -m venv venv
    pause
    exit /b 1
)

REM Instalar dependências (caso tenha atualizações)
echo.
echo [1/5] Verificando dependencias...
pip install -r requirements.txt --quiet

REM Rodar migrações
echo.
echo [2/5] Executando migracoes...
python manage.py makemigrations
python manage.py migrate

REM Criar superuser se não existir
echo.
echo [3/5] Verificando superuser...
python manage.py shell -c "from accounts.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser(username='admin', email='admin@ramonautopecas.com', password='admin123', first_name='Admin', last_name='Sistema', role='owner')"

REM Coletar arquivos estáticos
echo.
echo [4/5] Coletando arquivos estaticos...
python manage.py collectstatic --noinput

REM Iniciar servidor
echo.
echo [5/5] Iniciando servidor...
echo.
echo ========================================
echo Servidor rodando em http://localhost:8000
echo Admin em http://localhost:8000/admin/
echo.
echo CREDENCIAIS:
echo   Usuario: admin
echo   Senha: admin123
echo ========================================
echo.
echo Pressione CTRL+C para parar o servidor
echo.

python manage.py runserver
