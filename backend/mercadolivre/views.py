from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import MLCredential, MLSyncLog
from .serializers import MLCredentialSerializer, MLSyncLogSerializer
from .services import MercadoLivreService
from .tasks import (
    sync_product_to_ml, 
    sync_all_active_products, 
    import_all_ml_products,
    import_orders_from_ml,
    process_ml_notification
)
import json
import logging

logger = logging.getLogger(__name__)


class MLSyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para logs de sincronização"""
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
        f"https://auth.mercadolivre.com.br/authorization"
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
    
    if not user:
        # Usar usuário dono
        from accounts.models import User
        user = User.objects.filter(role='owner').first()
    
    if user:
        MLCredential.objects.update_or_create(
            user=user,
            defaults={
                'access_token': token_data['access_token'],
                'refresh_token': token_data['refresh_token'],
                'token_type': token_data['token_type'],
                'expires_in': token_data['expires_in'],
                'ml_user_id': token_data['user_id'],
            }
        )
        
        # Configurar webhooks automaticamente
        setup_webhooks.delay()
    
    return redirect('/#/dashboard/mercadolivre/success')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_all_products(request):
    """Sincronizar todos os produtos com ML"""
    task = sync_all_active_products.delay()
    
    return Response({
        "message": "Sincronização iniciada",
        "task_id": task.id
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_ml_products(request):
    """Importar todos os produtos do ML"""
    task = import_all_ml_products.delay()
    
    return Response({
        "message": "Importação de produtos iniciada",
        "task_id": task.id
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_ml_orders(request):
    """Importar pedidos do Mercado Livre"""
    task = import_orders_from_ml.delay()
    
    return Response({
        "message": "Importação de pedidos iniciada",
        "task_id": task.id
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ml_status(request):
    """Verificar status da integração com ML"""
    try:
        credential = MLCredential.objects.get(user=request.user)
        
        return Response({
            "connected": True,
            "ml_user_id": credential.ml_user_id,
            "last_sync": credential.updated_at
        })
    except MLCredential.DoesNotExist:
        return Response({
            "connected": False,
            "message": "Credenciais não configuradas"
        })


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def ml_webhook(request):
    """Endpoint para receber notificações do Mercado Livre"""
    try:
        # ML envia notificações como application/x-www-form-urlencoded ou JSON
        if request.content_type == 'application/json':
            notification_data = json.loads(request.body)
        else:
            notification_data = {
                'topic': request.POST.get('topic'),
                'resource': request.POST.get('resource'),
                'user_id': request.POST.get('user_id'),
                'application_id': request.POST.get('application_id')
            }
        
        logger.info(f"Webhook recebido: {notification_data}")
        
        # Processar notificação assincronamente
        process_ml_notification.delay(notification_data)
        
        # ML espera resposta 200
        return HttpResponse(status=200)
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return HttpResponse(status=200)  # Sempre retornar 200 para evitar reenvios


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_webhooks_view(request):
    """Configurar webhooks do ML"""
    from .tasks import setup_webhooks
    
    task = setup_webhooks.delay()
    
    return Response({
        "message": "Configuração de webhooks iniciada",
        "task_id": task.id
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_webhooks(request):
    """Listar webhooks configurados"""
    try:
        from accounts.models import User
        owner = User.objects.filter(role='owner').first()
        
        ml_service = MercadoLivreService(user=owner)
        webhooks = ml_service.get_notifications()
        
        return Response({"webhooks": webhooks})
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
