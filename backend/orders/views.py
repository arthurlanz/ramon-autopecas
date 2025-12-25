from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from .models import Order, OrderItem
from .serializers import (
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer
)
from .filters import OrderFilter

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        return OrderDetailSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Cliente vê apenas seus pedidos
        if user.role == 'customer':
            return self.queryset.filter(customer=user)
        
        # Dono e anunciador veem todos
        return self.queryset.all()
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Atualizar status do pedido"""
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Status inválido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_tracking(self, request, pk=None):
        """Adicionar código de rastreamento"""
        order = self.get_object()
        
        order.tracking_code = request.data.get('tracking_code')
        order.carrier = request.data.get('carrier')
        order.status = 'shipped'
        order.save()
        
        # TODO: Enviar email/notificação ao cliente
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Estatísticas de pedidos"""
        from django.db.models import Sum
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        month_start = today.replace(day=1)
        
        stats = {
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(status='pending').count(),
            'month_orders': Order.objects.filter(created_at__gte=month_start).count(),
            'month_revenue': Order.objects.filter(
                created_at__gte=month_start,
                status__in=['paid', 'processing', 'shipped', 'delivered']
            ).aggregate(Sum('total'))['total__sum'] or 0,
            'by_status': {
                status[0]: Order.objects.filter(status=status[0]).count()
                for status in Order.STATUS_CHOICES
            }
        }
        
        return Response(stats)
