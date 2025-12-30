from celery import shared_task
from django.utils import timezone
from django.db import transaction
from products.models import Product, Category, ProductImage
from orders.models import Order, OrderItem
from accounts.models import User
from .models import MLCredential, MLSyncLog
from .services import MercadoLivreService
import logging

logger = logging.getLogger(__name__)


@shared_task
def sync_product_to_ml(product_id):
    """Sincronizar produto individual com Mercado Livre"""
    try:
        product = Product.objects.get(id=product_id)
        owner = User.objects.filter(role='owner').first()
        if not owner:
            return {'error': 'Usuário dono não encontrado'}
        
        ml_service = MercadoLivreService(user=owner)
        
        if product.ml_item_id:
            result = ml_service.update_product(product)
        else:
            result = ml_service.create_product(product)
        
        return result
        
    except Product.DoesNotExist:
        return {'error': 'Produto não encontrado'}
    except Exception as e:
        logger.error(f"Erro ao sincronizar produto {product_id}: {e}")
        return {'error': str(e)}


@shared_task
def sync_all_active_products():
    """Sincronizar todos os produtos ativos com ML"""
    products = Product.objects.filter(sync_with_ml=True, status='active')
    
    results = []
    for product in products:
        result = sync_product_to_ml.delay(product.id)
        results.append(result.id)
    
    return {'total': len(results), 'task_ids': results}


@shared_task
def import_all_ml_products():
    """Importar TODOS os produtos do Mercado Livre para o sistema"""
    try:
        owner = User.objects.filter(role='owner').first()
        if not owner:
            return {'error': 'Usuário dono não encontrado'}
        
        ml_service = MercadoLivreService(user=owner)
        
        # Buscar todos os itens do ML
        ml_items = ml_service.get_all_seller_items()
        
        imported = 0
        updated = 0
        errors = []
        
        for ml_item in ml_items:
            try:
                with transaction.atomic():
                    # Verificar se produto já existe pelo ml_item_id
                    product = Product.objects.filter(ml_item_id=ml_item['id']).first()
                    
                    # Buscar ou criar categoria
                    category = _get_or_create_category_from_ml(ml_item['category_id'])
                    
                    # Preparar dados do produto
                    product_data = {
                        'title': ml_item['title'],
                        'description': ml_item.get('full_description', ml_item.get('subtitle', '')),
                        'category': category,
                        'price': ml_item['price'],
                        'stock_quantity': ml_item['available_quantity'],
                        'condition': ml_item['condition'],
                        'status': 'active' if ml_item['status'] == 'active' else 'inactive',
                        'ml_item_id': ml_item['id'],
                        'ml_permalink': ml_item['permalink'],
                        'ml_status': ml_item['status'],
                        'sync_with_ml': True,
                        'last_ml_sync': timezone.now(),
                    }
                    
                    # Extrair atributos (marca, modelo)
                    for attr in ml_item.get('attributes', []):
                        if attr['id'] == 'BRAND':
                            product_data['brand'] = attr.get('value_name', 'Sem marca')
                        elif attr['id'] == 'MODEL':
                            product_data['model'] = attr.get('value_name', '')
                    
                    # SKU baseado no ML ID se não existir
                    if not product:
                        product_data['sku'] = f"ML-{ml_item['id']}"
                        product_data['created_by'] = owner
                    
                    # Criar ou atualizar produto
                    if product:
                        for key, value in product_data.items():
                            setattr(product, key, value)
                        product.save()
                        updated += 1
                    else:
                        # Gerar slug único
                        from django.utils.text import slugify
                        base_slug = slugify(ml_item['title'][:50])
                        slug = base_slug
                        counter = 1
                        while Product.objects.filter(slug=slug).exists():
                            slug = f"{base_slug}-{counter}"
                            counter += 1
                        product_data['slug'] = slug
                        
                        product = Product.objects.create(**product_data)
                        imported += 1
                    
                    # Importar imagens
                    _import_product_images(product, ml_item.get('pictures', []))
                    
            except Exception as e:
                error_msg = f"Erro ao importar item {ml_item['id']}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        return {
            'success': True,
            'imported': imported,
            'updated': updated,
            'total_items': len(ml_items),
            'errors': errors
        }
        
    except Exception as e:
        logger.error(f"Erro ao importar produtos do ML: {e}")
        return {'error': str(e)}


def _get_or_create_category_from_ml(ml_category_id):
    """Buscar ou criar categoria a partir do ID do ML"""
    # Verificar se categoria já existe
    category = Category.objects.filter(ml_category_id=ml_category_id).first()
    
    if category:
        return category
    
    # Buscar informações da categoria no ML
    try:
        ml_service = MercadoLivreService()
        url = f"{ml_service.api_url}/categories/{ml_category_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            cat_data = response.json()
            
            from django.utils.text import slugify
            slug = slugify(cat_data['name'])
            
            # Garantir slug único
            counter = 1
            original_slug = slug
            while Category.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            category = Category.objects.create(
                name=cat_data['name'],
                slug=slug,
                ml_category_id=ml_category_id
            )
            
            return category
    except Exception as e:
        logger.error(f"Erro ao criar categoria {ml_category_id}: {e}")
    
    # Categoria padrão
    return Category.objects.get_or_create(
        slug='geral',
        defaults={'name': 'Geral', 'ml_category_id': ml_category_id}
    )[0]


def _import_product_images(product, ml_pictures):
    """Importar imagens do produto do ML"""
    import requests
    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage
    
    # Limpar imagens antigas se necessário
    if not product.images.exists():
        for idx, picture in enumerate(ml_pictures[:6]):  # Limitar a 6 imagens
            try:
                # Baixar imagem
                img_response = requests.get(picture['secure_url'])
                if img_response.status_code == 200:
                    # Salvar imagem
                    img_name = f"products/{product.slug}-{idx}.jpg"
                    img_content = ContentFile(img_response.content)
                    
                    ProductImage.objects.create(
                        product=product,
                        image=img_name,
                        is_primary=(idx == 0),
                        order=idx
                    )
                    
                    # Salvar arquivo
                    default_storage.save(img_name, img_content)
                    
            except Exception as e:
                logger.error(f"Erro ao importar imagem: {e}")


@shared_task
def import_orders_from_ml():
    """Importar pedidos do Mercado Livre"""
    try:
        owner = User.objects.filter(role='owner').first()
        if not owner:
            return {'error': 'Usuário dono não encontrado'}
        
        ml_service = MercadoLivreService(user=owner)
        
        # Buscar pedidos
        orders_data = ml_service.get_orders(limit=50)
        
        imported = 0
        updated = 0
        
        for ml_order_summary in orders_data.get('results', []):
            try:
                # Buscar detalhes completos do pedido
                ml_order = ml_service.get_order_detail(ml_order_summary['id'])
                
                if not ml_order:
                    continue
                
                # Verificar se pedido já existe
                order = Order.objects.filter(ml_order_id=ml_order['id']).first()
                
                if order:
                    # Atualizar status
                    order.status = _map_ml_status(ml_order['status'])
                    order.save()
                    updated += 1
                    continue
                
                # Criar novo pedido
                with transaction.atomic():
                    # Buscar ou criar cliente
                    buyer_info = ml_order['buyer']
                    customer = _get_or_create_customer(buyer_info)
                    
                    # Dados de envio
                    shipping = ml_order.get('shipping', {})
                    receiver = shipping.get('receiver_address', {})
                    
                    # Calcular valores
                    total_amount = ml_order['total_amount']
                    shipping_cost = shipping.get('shipping_cost', 0)
                    
                    # Criar pedido
                    order = Order.objects.create(
                        order_number=f"ML-{ml_order['id']}",
                        customer=customer,
                        status=_map_ml_status(ml_order['status']),
                        origin='mercadolivre',
                        ml_order_id=ml_order['id'],
                        ml_pack_id=ml_order.get('pack_id', ''),
                        subtotal=total_amount - shipping_cost,
                        shipping_cost=shipping_cost,
                        total=total_amount,
                        shipping_name=receiver.get('receiver_name', ''),
                        shipping_phone=receiver.get('phone', ''),
                        shipping_address=receiver.get('street_name', ''),
                        shipping_number=receiver.get('street_number', ''),
                        shipping_complement=receiver.get('comment', ''),
                        shipping_neighborhood=receiver.get('neighborhood', {}).get('name', ''),
                        shipping_city=receiver.get('city', {}).get('name', ''),
                        shipping_state=receiver.get('state', {}).get('id', ''),
                        shipping_zipcode=receiver.get('zip_code', ''),
                        tracking_code=shipping.get('tracking_number', ''),
                        carrier=shipping.get('logistic_type', '')
                    )
                    
                    # Criar itens do pedido
                    for item in ml_order['order_items']:
                        # Buscar produto
                        product = Product.objects.filter(ml_item_id=item['item']['id']).first()
                        
                        if product:
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                quantity=item['quantity'],
                                unit_price=item['unit_price'],
                                total_price=item['full_unit_price'] * item['quantity'],
                                product_title=item['item']['title'],
                                product_sku=product.sku
                            )
                            
                            # Atualizar estoque
                            if order.status == 'paid':
                                product.stock_quantity -= item['quantity']
                                product.save()
                    
                    imported += 1
                    
            except Exception as e:
                logger.error(f"Erro ao importar pedido {ml_order_summary['id']}: {e}")
        
        return {
            'success': True,
            'imported': imported,
            'updated': updated,
            'total': len(orders_data.get('results', []))
        }
        
    except Exception as e:
        logger.error(f"Erro ao importar pedidos: {e}")
        return {'error': str(e)}


def _map_ml_status(ml_status):
    """Mapear status do ML para status do sistema"""
    status_map = {
        'confirmed': 'paid',
        'payment_required': 'pending',
        'payment_in_process': 'pending',
        'paid': 'paid',
        'delivered': 'delivered',
        'cancelled': 'cancelled',
        'invalid': 'cancelled'
    }
    return status_map.get(ml_status, 'pending')


def _get_or_create_customer(buyer_info):
    """Buscar ou criar cliente a partir dos dados do ML"""
    # Verificar se já existe usuário com esse email
    email = buyer_info.get('email', f"ml_{buyer_info['id']}@placeholder.com")
    
    customer = User.objects.filter(email=email).first()
    
    if not customer:
        # Criar novo cliente
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        customer = User.objects.create(
            username=f"ml_{buyer_info['id']}",
            email=email,
            first_name=buyer_info.get('nickname', ''),
            role='customer'
        )
    
    return customer


@shared_task
def sync_stock_with_ml():
    """Sincronizar estoque entre site e ML"""
    products = Product.objects.filter(
        ml_item_id__isnull=False,
        sync_with_ml=True
    )
    
    synced = 0
    for product in products:
        try:
            sync_product_to_ml.delay(product.id)
            synced += 1
        except Exception as e:
            logger.error(f"Erro ao sincronizar estoque do produto {product.id}: {e}")
    
    return {'synced': synced}


@shared_task
def process_ml_notification(notification_data):
    """Processar notificação webhook do ML"""
    try:
        topic = notification_data.get('topic')
        resource = notification_data.get('resource')
        
        owner = User.objects.filter(role='owner').first()
        if not owner:
            return {'error': 'Usuário dono não encontrado'}
        
        ml_service = MercadoLivreService(user=owner)
        
        if topic == 'items':
            # Atualização de produto
            item_id = resource.split('/')[-1]
            item_data = ml_service.get_item_detail(item_id)
            
            if item_data:
                # Atualizar produto local
                product = Product.objects.filter(ml_item_id=item_id).first()
                if product:
                    product.stock_quantity = item_data['available_quantity']
                    product.price = item_data['price']
                    product.ml_status = item_data['status']
                    product.last_ml_sync = timezone.now()
                    product.save()
                    
                    return {'success': True, 'updated_product': product.id}
        
        elif topic == 'orders':
            # Nova venda/atualização de pedido
            order_id = resource.split('/')[-1]
            import_orders_from_ml.delay()
            return {'success': True, 'importing_orders': True}
        
        return {'success': True, 'topic': topic}
        
    except Exception as e:
        logger.error(f"Erro ao processar notificação ML: {e}")
        return {'error': str(e)}


# Importar requests aqui para uso nas funções auxiliares
import requests
# Adicionar no final de mercadolivre/tasks.py

@shared_task
def setup_webhooks():
    """Configurar webhooks do Mercado Livre automaticamente"""
    try:
        owner = User.objects.filter(role='owner').first()
        if not owner:
            return {'error': 'Usuário dono não encontrado'}
        
        ml_service = MercadoLivreService(user=owner)
        
        # URL base do webhook (deve ser HTTPS em produção)
        base_url = settings.ALLOWED_HOSTS[0]
        webhook_url = f"https://{base_url}/api/ml/webhook/"
        
        # Topics para monitorar
        topics = ['items', 'orders']
        
        # Deletar webhooks antigos
        existing_webhooks = ml_service.get_notifications()
        for webhook in existing_webhooks:
            ml_service.delete_notification(webhook['id'])
        
        # Criar novos webhooks
        created = []
        for topic in topics:
            result = ml_service.create_notification_webhook(topic, webhook_url)
            if result:
                created.append(result)
        
        return {
            'success': True,
            'webhooks_created': len(created),
            'topics': topics
        }
        
    except Exception as e:
        logger.error(f"Erro ao configurar webhooks: {e}")
        return {'error': str(e)}

