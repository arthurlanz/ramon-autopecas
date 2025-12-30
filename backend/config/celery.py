import os
from celery import Celery
from celery.schedules import crontab

# Configurar Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('ramon_autopecas')

# Carregar configurações do Django com namespace CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir tarefas automaticamente em todos os apps
app.autodiscover_tasks()

# Configurar timezone
app.conf.timezone = 'America/Sao_Paulo'
app.conf.enable_utc = False

# Tarefas agendadas (Celery Beat)
app.conf.beat_schedule = {
    # Sincronizar estoque a cada 10 minutos
    'sync-ml-stock-every-10min': {
        'task': 'mercadolivre.tasks.sync_stock_with_ml',
        'schedule': crontab(minute='*/10'),
    },
    
    # Importar pedidos a cada 15 minutos
    'import-ml-orders-every-15min': {
        'task': 'mercadolivre.tasks.import_orders_from_ml',
        'schedule': crontab(minute='*/15'),
    },
    
    # Sincronização completa todo dia às 2h
    'full-sync-daily-2am': {
        'task': 'mercadolivre.tasks.sync_all_active_products',
        'schedule': crontab(hour=2, minute=0),
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tarefa de debug"""
    print(f'Request: {self.request!r}')
