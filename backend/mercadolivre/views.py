from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import redirect
from .models import MLCredential, MLSyncLog
from .serializers import MLCredentialSerializer, MLSyncLogSerializer
from .services import MercadoLivreService

class MLSyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MLSyncLog.objects.all()
    serializer_class = MLSyncLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ml_auth_url(request):
    """Retorna URL de autorização do Mercado Livre"""
    ml_config = settings.MERCADO_LIVRE
    auth_url = (
        f"{ml_config['API_URL']}/authorization"
        f"?response_type=code"
        f"&client_id={ml_config['APP_ID']}"
        f"&redirect_uri={ml_config['REDIRECT_URI']}"
    )
    return Response({"auth_url": auth_url})


@api_view(['GET'])
def ml_callback(request):
    """Callback do Mercado Livre após autorização"""
    code = request.GET.get('code')
    
    if not code:
        return Response(
            {"error": "Código de autorização não fornecido"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    ml_service = MercadoLivreService()
    token_data = ml_service.get_access_token(code)
    
    if 'error' in token_data:
        return Response(token_data, status=status.HTTP_400_BAD_REQUEST)
    
    # Salvar credenciais
    user = request.user if request.user.is_authenticated else None
    
    if user:
        MLCredential.objects.update_or_create(
            user=user,
            defaults={
                'access_token': token_data['access_token'],
                'refresh_token': token_data['refresh_token'],
                'token_type': token_data['token_type'],
                'expires_in': token_data['expires_in'],
                'user_id': token_data['user_id'],
            }
        )
    
    return redirect('/#/dashboard/mercadolivre/success')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_all_products(request):
    """Sincronizar todos os produtos com ML"""
    from products.models import Product
    from mercadolivre.tasks import sync_product_to_ml
    
    products = Product.objects.filter(sync_with_ml=True, status='active')
    
    tasks = []
    for product in products:
        task = sync_product_to_ml.delay(product.id)
        tasks.append(task.id)
    
    return Response({
        "message": f"{len(tasks)} produtos sendo sincronizados",
        "task_ids": tasks
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_ml_orders(request):
    """Importar pedidos do Mercado Livre"""
    from mercadolivre.tasks import import_orders_from_ml
    
    task = import_orders_from_ml.delay()
    
    return Response({
        "message": "Importação de pedidos iniciada",
        "task_id": task.id
    })
