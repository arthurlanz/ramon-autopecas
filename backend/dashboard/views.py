from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from datetime import timedelta
from products.models import Product
from orders.models import Order, OrderItem
from accounts.models import User

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Overview geral do dashboard"""
        today = timezone.now().date()
        month_start = today.replace(day=1)
        
        # Estatísticas de produtos
        products_stats = {
            'total': Product.objects.count(),
            'active': Product.objects.filter(status='active').count(),
            'low_stock': Product.objects.filter(
                stock_quantity__lte=F('min_stock_alert')
            ).count(),
            'out_of_stock': Product.objects.filter(stock_quantity=0).count(),
        }
        
        # Estatísticas de pedidos
        orders_stats = {
            'total': Order.objects.count(),
            'pending': Order.objects.filter(status='pending').count(),
            'month_total': Order.objects.filter(created_at__gte=month_start).count(),
            'month_revenue': Order.objects.filter(
                created_at__gte=month_start,
                status__in=['paid', 'processing', 'shipped', 'delivered']
            ).aggregate(total=Sum('total'))['total'] or 0,
        }
        
        # Top produtos
        top_products = OrderItem.objects.values(
            'product__title', 'product__id'
        ).annotate(
            total_sold=Sum('quantity'),
            revenue=Sum('total_price')
        ).order_by('-total_sold')[:5]
        
        # Vendas por origem
        sales_by_origin = Order.objects.values('origin').annotate(
            count=Count('id'),
            revenue=Sum('total')
        )
        
        return Response({
            'products': products_stats,
            'orders': orders_stats,
            'top_products': list(top_products),
            'sales_by_origin': list(sales_by_origin),
        })
    
    @action(detail=False, methods=['get'])
    def sales_chart(self, request):
        """Dados para gráfico de vendas (últimos 30 dias)"""
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        
        daily_sales = []
        current_date = start_date
        
        while current_date <= timezone.now().date():
            sales = Order.objects.filter(
                created_at__date=current_date,
                status__in=['paid', 'processing', 'shipped', 'delivered']
            ).aggregate(
                count=Count('id'),
                revenue=Sum('total')
            )
            
            daily_sales.append({
                'date': current_date.isoformat(),
                'count': sales['count'] or 0,
                'revenue': float(sales['revenue'] or 0),
            })
            
            current_date += timedelta(days=1)
        
        return Response(daily_sales)
    
    @action(detail=False, methods=['get'])
    def revenue_by_category(self, request):
        """Receita por categoria"""
        from products.models import Category
        
        categories = Category.objects.annotate(
            revenue=Sum(
                'products__orderitem__total_price',
                filter=Q(products__orderitem__order__status__in=[
                    'paid', 'processing', 'shipped', 'delivered'
                ])
            ),
            sales_count=Count(
                'products__orderitem',
                filter=Q(products__orderitem__order__status__in=[
                    'paid', 'processing', 'shipped', 'delivered'
                ])
            )
        ).filter(revenue__gt=0).order_by('-revenue')[:10]
        
        data = [
            {
                'category': cat.name,
                'revenue': float(cat.revenue or 0),
                'sales_count': cat.sales_count
            }
            for cat in categories
        ]
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def recent_orders(self, request):
        """Pedidos recentes"""
        limit = int(request.query_params.get('limit', 10))
        
        orders = Order.objects.select_related('customer').order_by('-created_at')[:limit]
        
        from orders.serializers import OrderListSerializer
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """Alertas do sistema"""
        alerts = []
        
        # Produtos com estoque baixo
        low_stock = Product.objects.filter(
            stock_quantity__lte=F('min_stock_alert'),
            stock_quantity__gt=0,
            status='active'
        ).count()
        
        if low_stock > 0:
            alerts.append({
                'type': 'warning',
                'message': f'{low_stock} produto(s) com estoque baixo',
                'link': '/dashboard/products?filter=low_stock'
            })
        
        # Produtos sem estoque
        out_of_stock = Product.objects.filter(
            stock_quantity=0,
            status='active'
        ).count()
        
        if out_of_stock > 0:
            alerts.append({
                'type': 'error',
                'message': f'{out_of_stock} produto(s) sem estoque',
                'link': '/dashboard/products?filter=out_of_stock'
            })
        
        # Pedidos pendentes
        pending_orders = Order.objects.filter(status='pending').count()
        
        if pending_orders > 0:
            alerts.append({
                'type': 'info',
                'message': f'{pending_orders} pedido(s) pendente(s)',
                'link': '/dashboard/orders?status=pending'
            })
        
        return Response(alerts)
