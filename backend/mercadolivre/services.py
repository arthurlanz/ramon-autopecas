import requests
from django.conf import settings
from datetime import datetime, timedelta
from .models import MLCredential, MLSyncLog

class MercadoLivreService:
    def __init__(self, user=None):
        self.config = settings.MERCADO_LIVRE
        self.api_url = self.config['API_URL']
        self.user = user
        self.credential = None
        
        if user:
            try:
                self.credential = MLCredential.objects.get(user=user)
            except MLCredential.DoesNotExist:
                pass
    
    def get_access_token(self, code):
        """Obter token de acesso usando código de autorização"""
        url = f"{self.api_url}/oauth/token"
        
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.config['APP_ID'],
            'client_secret': self.config['CLIENT_SECRET'],
            'code': code,
            'redirect_uri': self.config['REDIRECT_URI']
        }
        
        response = requests.post(url, data=data)
        return response.json()
    
    def refresh_access_token(self):
        """Renovar token de acesso"""
        if not self.credential:
            return None
        
        url = f"{self.api_url}/oauth/token"
        
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.config['APP_ID'],
            'client_secret': self.config['CLIENT_SECRET'],
            'refresh_token': self.credential.refresh_token
        }
        
        response = requests.post(url, data=data)
        token_data = response.json()
        
        if 'access_token' in token_data:
            self.credential.access_token = token_data['access_token']
            self.credential.refresh_token = token_data['refresh_token']
            self.credential.expires_in = token_data['expires_in']
            self.credential.save()
        
        return token_data
    
    def _get_headers(self):
        """Headers para requisições autenticadas"""
        if not self.credential:
            raise Exception("Credenciais do Mercado Livre não configuradas")
        
        return {
            'Authorization': f'Bearer {self.credential.access_token}',
            'Content-Type': 'application/json'
        }
    
    def create_product(self, product):
        """Criar produto no Mercado Livre"""
        url = f"{self.api_url}/items"
        
        # Preparar dados do produto
        data = {
            'title': product.title[:60],  # ML tem limite de 60 caracteres
            'category_id': product.category.ml_category_id,
            'price': float(product.price),
            'currency_id': 'BRL',
            'available_quantity': product.stock_quantity,
            'buying_mode': 'buy_it_now',
            'condition': product.condition,
            'listing_type_id': 'gold_special',  # ou 'gold_pro', 'free'
            'description': {
                'plain_text': product.description
            },
            'pictures': [
                {'source': img.image.url} 
                for img in product.images.all()[:12]  # ML permite até 12 imagens
            ],
            'attributes': [
                {'id': 'BRAND', 'value_name': product.brand},
                {'id': 'MODEL', 'value_name': product.model},
            ],
            'shipping': {
                'mode': 'me2',
                'local_pick_up': True,
                'free_shipping': False,
                'dimensions': {
                    'width': str(product.width or 10),
                    'height': str(product.height or 10),
                    'length': str(product.length or 10),
                    'weight': str(product.weight or 100)
                }
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            result = response.json()
            
            # Log da sincronização
            MLSyncLog.objects.create(
                product=product,
                action='create',
                status='success' if response.status_code == 201 else 'error',
                request_data=data,
                response_data=result,
                error_message=result.get('message', '') if response.status_code != 201 else ''
            )
            
            if response.status_code == 201:
                product.ml_item_id = result['id']
                product.ml_permalink = result['permalink']
                product.ml_status = result['status']
                product.last_ml_sync = datetime.now()
                product.save()
            
            return result
            
        except Exception as e:
            MLSyncLog.objects.create(
                product=product,
                action='create',
                status='error',
                request_data=data,
                error_message=str(e)
            )
            return {'error': str(e)}
    
    def update_product(self, product):
        """Atualizar produto no Mercado Livre"""
        if not product.ml_item_id:
            return self.create_product(product)
        
        url = f"{self.api_url}/items/{product.ml_item_id}"
        
        data = {
            'title': product.title[:60],
            'price': float(product.price),
            'available_quantity': product.stock_quantity,
            'description': {
                'plain_text': product.description
            }
        }
        
        try:
            response = requests.put(url, json=data, headers=self._get_headers())
            result = response.json()
            
            MLSyncLog.objects.create(
                product=product,
                action='update',
                status='success' if response.status_code == 200 else 'error',
                request_data=data,
                response_data=result,
                error_message=result.get('message', '') if response.status_code != 200 else ''
            )
            
            if response.status_code == 200:
                product.ml_status = result['status']
                product.last_ml_sync = datetime.now()
                product.save()
            
            return result
            
        except Exception as e:
            MLSyncLog.objects.create(
                product=product,
                action='update',
                status='error',
                request_data=data,
                error_message=str(e)
            )
            return {'error': str(e)}
    
    def get_orders(self, seller_id):
        """Buscar pedidos do vendedor"""
        url = f"{self.api_url}/orders/search"
        
        params = {
            'seller': seller_id,
            'sort': 'date_desc',
            'limit': 50
        }
        
        response = requests.get(url, params=params, headers=self._get_headers())
        return response.json()
    
    def get_order_details(self, order_id):
        """Buscar detalhes de um pedido"""
        url = f"{self.api_url}/orders/{order_id}"
        response = requests.get(url, headers=self._get_headers())
        return response.json()
    
    def pause_product(self, product):
        """Pausar anúncio no ML"""
        if not product.ml_item_id:
            return {'error': 'Produto não está no Mercado Livre'}
        
        url = f"{self.api_url}/items/{product.ml_item_id}"
        data = {'status': 'paused'}
        
        response = requests.put(url, json=data, headers=self._get_headers())
        return response.json()
    
    def close_product(self, product):
        """Encerrar anúncio no ML"""
        if not product.ml_item_id:
            return {'error': 'Produto não está no Mercado Livre'}
        
        url = f"{self.api_url}/items/{product.ml_item_id}"
        data = {'status': 'closed'}
        
        response = requests.put(url, json=data, headers=self._get_headers())
        return response.json()
