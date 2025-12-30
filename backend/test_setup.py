"""
Script para testar configuração do ambiente
Execute: python test_setup.py
"""

import sys
import os

def test_python():
    """Testar versão do Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("  ⚠️  Recomendado Python 3.10+")
    return True

def test_imports():
    """Testar importações essenciais"""
    modules = [
        'django',
        'rest_framework',
        'celery',
        'redis',
        'psycopg2',
        'PIL',
        'requests'
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - NÃO INSTALADO")
            failed.append(module)
    
    return len(failed) == 0

def test_env():
    """Testar arquivo .env"""
    if not os.path.exists('.env'):
        print("✗ Arquivo .env não encontrado")
        print("  Copie .env.example para .env e preencha as variáveis")
        return False
    
    print("✓ Arquivo .env encontrado")
    return True

def test_redis():
    """Testar conexão Redis"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✓ Redis conectado")
        return True
    except Exception as e:
        print(f"✗ Redis não disponível: {e}")
        return False

def test_postgres():
    """Testar conexão PostgreSQL"""
    try:
        import psycopg2
        from decouple import config
        
        conn = psycopg2.connect(
            dbname=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PORT', default='5432')
        )
        conn.close()
        print("✓ PostgreSQL conectado")
        return True
    except Exception as e:
        print(f"✗ PostgreSQL: {e}")
        return False

def main():
    """Executar todos os testes"""
    print("=" * 50)
    print("RAMON AUTOPEÇAS - TESTE DE CONFIGURAÇÃO")
    print("=" * 50)
    print()
    
    tests = [
        ("Python", test_python),
        ("Módulos Python", test_imports),
        ("Arquivo .env", test_env),
        ("Redis", test_redis),
        ("PostgreSQL", test_postgres),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 50)
        try:
            results.append(test_func())
        except Exception as e:
            print(f"✗ Erro: {e}")
            results.append(False)
    
    print()
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTestes: {passed}/{total} passaram")
    
    if passed == total:
        print("\n🎉 Ambiente configurado corretamente!")
        print("\nPróximos passos:")
        print("  1. python manage.py migrate")
        print("  2. start.bat")
        print("  3. start_celery.bat")
    else:
        print("\n⚠️  Corrija os erros acima")

if __name__ == '__main__':
    main()
