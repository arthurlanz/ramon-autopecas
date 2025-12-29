from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'product_count', 'is_active']
        read_only_fields = ['slug']
    
    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'is_primary', 'order']
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'price', 'stock_quantity', 'brand', 'sku',
            'category', 'category_name', 'primary_image', 'status', 'featured',
            'ml_item_id', 'ml_permalink', 'ml_status', 'created_at'
        ]
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if not primary:
            primary = obj.images.first()
        if primary:
            request = self.context.get('request')
            return request.build_absolute_uri(primary.image.url) if request else primary.image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'description', 'price', 'cost_price',
            'stock_quantity', 'min_stock_alert', 'brand', 'model', 'sku', 'barcode',
            'category', 'category_name', 'compatible_vehicles', 'year_from', 'year_to',
            'condition', 'status', 'weight', 'length', 'width', 'height',
            'images', 'ml_item_id', 'ml_permalink', 'ml_status', 'sync_with_ml',
            'last_ml_sync', 'featured', 'views_count', 'is_low_stock',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'views_count', 'created_at', 'updated_at']

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price', 'cost_price', 'stock_quantity',
            'min_stock_alert', 'brand', 'model', 'sku', 'barcode', 'category',
            'compatible_vehicles', 'year_from', 'year_to', 'condition', 'status',
            'weight', 'length', 'width', 'height', 'featured', 'sync_with_ml',
            'uploaded_images'
        ]
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        validated_data['created_by'] = self.context['request'].user
        
        # Gerar slug automático
        from django.utils.text import slugify
        validated_data['slug'] = slugify(validated_data['title'])
        
        product = Product.objects.create(**validated_data)
        
        # Criar imagens
        for idx, image in enumerate(uploaded_images):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(idx == 0),
                order=idx
            )
        
        # Se sync_with_ml=True, agendar sincronização
        if validated_data.get('sync_with_ml'):
            from mercadolivre.tasks import sync_product_to_ml
            sync_product_to_ml.delay(product.id)
        
        return product
    
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualizar imagens se fornecidas
        if uploaded_images is not None:
            instance.images.all().delete()
            for idx, image in enumerate(uploaded_images):
                ProductImage.objects.create(
                    product=instance,
                    image=image,
                    is_primary=(idx == 0),
                    order=idx
                )
        
        # Se sync_with_ml=True, sincronizar
        if validated_data.get('sync_with_ml'):
            from mercadolivre.tasks import sync_product_to_ml
            sync_product_to_ml.delay(instance.id)
        
        return instance
