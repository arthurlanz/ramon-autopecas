import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('ramon_autopecas')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Tarefas agendadas
app.conf.beat_schedule = {
    'sync-ml-products-daily': {
        'task': 'mercadolivre.tasks.sync_all_active_products',
        'schedule': crontab(hour=2, minute=0),  # Todo dia às 2h da manhã
    },
    'import-ml-orders-hourly': {
        'task': 'mercadolivre.tasks.import_orders_from_ml',
        'schedule': crontab(minute=0),  # A cada hora
    },
    'check-ml-stock': {
        'task': 'mercadolivre.tasks.check_ml_stock_sync',
        'schedule': crontab(minute='*/30'),  # A cada 30 minutos
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
