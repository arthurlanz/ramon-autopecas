from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'sku', 'brand', 'price', 'stock_quantity', 
                    'status', 'category', 'ml_item_id', 'created_at']
    list_filter = ['status', 'condition', 'category', 'brand', 'featured', 'sync_with_ml']
    search_fields = ['title', 'sku', 'description', 'brand', 'compatible_vehicles']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]
    readonly_fields = ['ml_item_id', 'ml_permalink', 'ml_status', 'last_ml_sync', 
                       'views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'slug', 'description', 'category', 'brand', 'model')
        }),
        ('Códigos', {
            'fields': ('sku', 'barcode')
        }),
        ('Compatibilidade', {
            'fields': ('compatible_vehicles', 'year_from', 'year_to')
        }),
        ('Preço e Estoque', {
            'fields': ('price', 'cost_price', 'stock_quantity', 'min_stock_alert')
        }),
        ('Dimensões', {
            'fields': ('weight', 'length', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('condition', 'status', 'featured')
        }),
        ('Mercado Livre', {
            'fields': ('sync_with_ml', 'ml_item_id', 'ml_permalink', 'ml_status', 'last_ml_sync')
        }),
        ('Metadata', {
            'fields': ('created_by', 'views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
