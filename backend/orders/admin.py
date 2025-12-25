from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_title', 'product_sku', 'unit_price', 'total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'status', 'origin', 
                    'total', 'created_at']
    list_filter = ['status', 'origin', 'created_at']
    search_fields = ['order_number', 'customer__username', 'customer__email', 
                     'ml_order_id', 'tracking_code']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'subtotal', 'total', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('order_number', 'customer', 'status', 'origin')
        }),
        ('Valores', {
            'fields': ('subtotal', 'shipping_cost', 'discount', 'total')
        }),
        ('Endereço de Entrega', {
            'fields': ('shipping_name', 'shipping_phone', 'shipping_address', 
                      'shipping_number', 'shipping_complement', 'shipping_neighborhood',
                      'shipping_city', 'shipping_state', 'shipping_zipcode')
        }),
        ('Rastreamento', {
            'fields': ('tracking_code', 'carrier')
        }),
        ('Mercado Livre', {
            'fields': ('ml_order_id', 'ml_pack_id'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
