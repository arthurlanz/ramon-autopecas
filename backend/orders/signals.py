"""
Signals para o app Orders
Gerenciar automaticamente estoque e outras ações quando pedidos são criados/atualizados
"""

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db.models import F

from products.models import Product
from .models import Order, OrderItem


@receiver(pre_save, sender=Order)
def generate_order_number(sender, instance, **kwargs):
    """
    Gerar número único de pedido automaticamente se não existir
    """
    if not instance.order_number:
        import random
        import string
        from django.utils import timezone
        
        # Formato: RP-YYYYMMDD-XXXX (Ramon Peças)
        date_str = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.digits, k=4))
        instance.order_number = f"RP-{date_str}-{random_str}"
        
        # Verificar se já existe (improvável mas possível)
        while Order.objects.filter(order_number=instance.order_number).exists():
            random_str = ''.join(random.choices(string.digits, k=4))
            instance.order_number = f"RP-{date_str}-{random_str}"


@receiver(post_save, sender=OrderItem)
def update_product_stock_on_item_created(sender, instance, created, **kwargs):
    """
    Reduzir estoque quando um item de pedido é criado
    Apenas se o pedido já estiver pago/processando
    """
    if created:
        order = instance.order
        
        # Só atualizar estoque se pedido estiver confirmado
        if order.status in ['paid', 'processing', 'shipped', 'delivered']:
            product = instance.product
            
            # Usar F() para evitar race conditions
            product.stock_quantity = F('stock_quantity') - instance.quantity
            product.save(update_fields=['stock_quantity'])
            
            # Recarregar para ter o valor atualizado
            product.refresh_from_db()


@receiver(post_save, sender=Order)
def handle_order_status_change(sender, instance, created, **kwargs):
    """
    Gerenciar mudanças de status do pedido
    """
    if not created:
        # Se pedido foi cancelado, devolver estoque
        if instance.status == 'cancelled':
            for item in instance.items.all():
                product = item.product
                product.stock_quantity = F('stock_quantity') + item.quantity
                product.save(update_fields=['stock_quantity'])
                product.refresh_from_db()
        
        # Se mudou de pending para paid, reduzir estoque
        elif instance.status in ['paid', 'processing']:
            # Verificar se itens já tiveram estoque reduzido
            # (essa lógica pode ser melhorada com um flag no OrderItem)
            pass


@receiver(post_delete, sender=OrderItem)
def restore_stock_on_item_deleted(sender, instance, **kwargs):
    """
    Restaurar estoque se um item de pedido for deletado
    """
    # Só restaurar se o pedido não estiver cancelado
    if instance.order.status != 'cancelled':
        product = instance.product
        product.stock_quantity = F('stock_quantity') + instance.quantity
        product.save(update_fields=['stock_quantity'])
        product.refresh_from_db()
