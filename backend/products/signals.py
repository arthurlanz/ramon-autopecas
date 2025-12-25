from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Product, Category
from .utils import generate_unique_slug, generate_sku

@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    """Gerar slug e SKU automaticamente"""
    if not instance.slug:
        instance.slug = generate_unique_slug(Product, instance.title)
    
    if not instance.sku:
        instance.sku = generate_sku()
    
    # Atualizar status baseado no estoque
    if instance.stock_quantity == 0:
        instance.status = 'out_of_stock'
    elif instance.status == 'out_of_stock' and instance.stock_quantity > 0:
        instance.status = 'active'

@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, **kwargs):
    """Gerar slug para categoria"""
    if not instance.slug:
        instance.slug = slugify(instance.name)
