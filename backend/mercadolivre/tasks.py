from celery import shared_task
from django.utils import timezone
from products.models import Product
from orders.models import Order, OrderItem
from .models import MLSyncLog
from .services import MercadoLivreService

@shared_task
def sync_product_to_ml(product_id):
    """Sincronizar produto individual com Mercado Livre"""
    try:
        product = Product.objects.get(id=product_id)
        
        # Obter usuário com credenciais ML (geralmente o dono)
        from accounts.models import User
        owner = User.objects.filter(role='owner').first()
        
        ml_service = MercadoLivreService(user=owner)
        
        if product.ml_item_id:
            result = ml_service.update_product(product)
        else:
            result = ml_service.create_product(product)
        
        return result
        
    except Product.DoesNotExist:
        return {'error': 'Produto não encontrado'}
    except Exception as e:
        return {'error': str(e)}


@shared_task
def sync_all_active_products():
    """Sincronizar todos os produtos ativos com ML (executar diariamente)"""
    products = Product.objects.filter(sync_with_ml=True, status='active')
    
    results = []
    for product in products:
        result = sync_product_to_ml.delay(product.id)
        results.append(result.id)
    
    return {'total': len(results), 'task_ids': results}


@shared_task
def import_orders_from_ml():
    """Importar pedidos do Mercado Livre"""
    from accounts.models import User
    
    try:
        owner = User.objects.filter(role='owner').first()
        ml_service = MercadoLivreService(user=owner)
        
        # Buscar pedidos
        orders_data = ml_service.get_orders(ml_service.credential.user_id)
        
        imported = 0
        for ml_order in orders_data.get('results', []):
            # Verificar se pedido já existe
            if Order.objects.filter(ml_order_id=ml_order['id']).exists():
                continue
            
            # Buscar detalhes completos do pedido
            order_details = ml_service.get_order_details(ml_order['id'])
            
            # Criar pedido no sistema
            # TODO: Implementar lógica completa de importação
            imported += 1
        
        return {'imported': imported}
        
    except Exception as e:
        return {'error': str(e)}


@shared_task
def check_ml_stock_sync():
    """Verificar e sincronizar estoque entre site e ML"""
    products = Product.objects.filter(
        ml_item_id__isnull=False,
        sync_with_ml=True
    )
    
    for product in products:
        sync_product_to_ml.delay(product.id)
