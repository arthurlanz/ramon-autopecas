import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    customer_name = django_filters.CharFilter(field_name='customer__username', lookup_expr='icontains')
    
    class Meta:
        model = Order
        fields = ['status', 'origin', 'customer']
