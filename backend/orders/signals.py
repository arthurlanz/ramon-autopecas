from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, F
from .models import Category, Product, ProductImage
from .serializers import (
    CategorySerializer, ProductListSerializer,
    ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductImageSerializer
)
from .filters import ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status='active')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'sku', 'brand', 'compatible_vehicles']
    ordering_fields = ['price', 'created_at', 'stock_quantity', 'title']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Incrementar visualizações
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Produtos em destaque"""
        products = self.queryset.filter(featured=True)[:10]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Produtos com estoque baixo"""
        products = Product.objects.filter(
            stock_quantity__lte=F('min_stock_alert'),
            status='active'
        )
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_image(self, request, slug=None):
        """Adicionar imagem ao produto"""
        product = self.get_object()
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def sync_to_ml(self, request, slug=None):
        """Sincronizar produto com Mercado Livre"""
        product = self.get_object()
        from mercadolivre.tasks import sync_product_to_ml
        task = sync_product_to_ml.delay(product.id)
        return Response({
            "message": "Sincronização iniciada",
            "task_id": task.id
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Estatísticas dos produtos"""
        stats = {
            'total': Product.objects.count(),
            'active': Product.objects.filter(status='active').count(),
            'low_stock': Product.objects.filter(
                stock_quantity__lte=F('min_stock_alert')
            ).count(),
            'out_of_stock': Product.objects.filter(stock_quantity=0).count(),
            'synced_ml': Product.objects.filter(ml_item_id__isnull=False).count(),
        }
        return Response(stats)
