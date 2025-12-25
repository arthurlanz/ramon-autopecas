from django.utils.text import slugify
import uuid

def generate_unique_slug(model_class, title):
    """Gera slug único para produtos"""
    base_slug = slugify(title)
    unique_slug = base_slug
    num = 1
    
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{base_slug}-{num}'
        num += 1
    
    return unique_slug


def generate_sku():
    """Gera SKU único"""
    return f"RA-{uuid.uuid4().hex[:8].upper()}"
