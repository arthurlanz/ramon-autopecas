from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source='product', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_details', 'quantity', 'unit_price', 
                  'total_price', 'product_title', 'product_sku']
        read_only_fields = ['id', 'unit_price', 'total_price', 'product_title', 'product_sku']


class OrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer_name', 'status', 'origin', 
                  'total', 'items_count', 'created_at']
        read_only_fields = ['id', 'order_number', 'created_at']
    
    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    customer_email = serializers.EmailField(source='customer.email', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['customer', 'items', 'shipping_name', 'shipping_phone', 
                  'shipping_address', 'shipping_number', 'shipping_complement',
                  'shipping_neighborhood', 'shipping_city', 'shipping_state', 
                  'shipping_zipcode', 'notes']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calcular totais
        subtotal = sum(item['quantity'] * item['product'].price for item in items_data)
        shipping_cost = 0  # Calcular baseado em CEP/peso
        total = subtotal + shipping_cost
        
        # Gerar número do pedido
        import uuid
        order_number = f"RA{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            order_number=order_number,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            **validated_data
        )
        
        # Criar items do pedido
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price,
                total_price=product.price * quantity,
                product_title=product.title,
                product_sku=product.sku
            )
            
            # Atualizar estoque
            product.stock_quantity -= quantity
            product.save()
        
        return order
