import requests
from django.conf import settings
from datetime import datetime, timedelta
from .models import MLCredential, MLSyncLog
import logging

logger = logging.getLogger(__name__)


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

    # ============ PRODUTOS - IMPORTAÇÃO DO ML ============
    
    def get_all_seller_items(self, limit=50):
        """Buscar TODOS os itens do vendedor no ML"""
        url = f"{self.api_url}/users/{self.credential.ml_user_id}/items/search"
        
        all_items = []
        offset = 0
        
        while True:
            params = {
                'offset': offset,
                'limit': limit
            }
            
            try:
                response = requests.get(url, headers=self._get_headers(), params=params)
                response.raise_for_status()
                data = response.json()
                
                items_ids = data.get('results', [])
                if not items_ids:
                    break
                
                # Buscar detalhes de cada item
                for item_id in items_ids:
                    item_detail = self.get_item_detail(item_id)
                    if item_detail:
                        all_items.append(item_detail)
                
                # Verificar se tem mais itens
                if len(items_ids) < limit:
                    break
                    
                offset += limit
                
            except Exception as e:
                logger.error(f"Erro ao buscar itens: {e}")
                break
        
        return all_items
    
    def get_item_detail(self, item_id):
        """Buscar detalhes completos de um item"""
        url = f"{self.api_url}/items/{item_id}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            item = response.json()
            
            # Buscar descrição separadamente
            desc_url = f"{self.api_url}/items/{item_id}/description"
            desc_response = requests.get(desc_url)
            if desc_response.status_code == 200:
                item['full_description'] = desc_response.json().get('plain_text', '')
            
            return item
            
        except Exception as e:
            logger.error(f"Erro ao buscar item {item_id}: {e}")
            return None
    
    def get_categories(self, site_id='MLB'):
        """Buscar todas as categorias do ML"""
        url = f"{self.api_url}/sites/{site_id}/categories"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao buscar categorias: {e}")
            return []
    
    def get_category_attributes(self, category_id):
        """Buscar atributos obrigatórios de uma categoria"""
        url = f"{self.api_url}/categories/{category_id}/attributes"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao buscar atributos da categoria: {e}")
            return []

    # ============ CRIAR/ATUALIZAR PRODUTOS NO ML ============

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
                {'source': request.build_absolute_uri(img.image.url)}
                for img in product.images.all()[:12]  # ML permite até 12 imagens
            ],
            'attributes': [
                {'id': 'BRAND', 'value_name': product.brand},
                {'id': 'MODEL', 'value_name': product.model or 'N/A'},
            ],
            'shipping': {
                'mode': 'me2',
                'local_pick_up': True,
                'free_shipping': False,
                'dimensions': {
                    'width': str(product.width or 10),
                    'height': str(product.height or 10),
                    'length': str(product.length or 10),
                    'weight': str(int(product.weight * 1000) if product.weight else 1000)  # em gramas
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
            'status': 'active' if product.status == 'active' else 'paused'
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

    # ============ PEDIDOS ============

    def get_orders(self, limit=50, offset=0):
        """Buscar pedidos do vendedor"""
        url = f"{self.api_url}/orders/search"
        
        params = {
            'seller': self.credential.ml_user_id,
            'sort': 'date_desc',
            'limit': limit,
            'offset': offset
        }
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao buscar pedidos: {e}")
            return {'results': [], 'paging': {}}

    def get_order_detail(self, order_id):
        """Buscar detalhes completos de um pedido"""
        url = f"{self.api_url}/orders/{order_id}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao buscar pedido {order_id}: {e}")
            return None

    # ============ WEBHOOKS/NOTIFICAÇÕES ============

    def create_notification_webhook(self, topic, url_callback):
        """Criar webhook para receber notificações do ML"""
        url = f"{self.api_url}/applications/{self.config['APP_ID']}/notifications"
        
        data = {
            'topic': topic,  # 'items', 'orders', 'messages', etc
            'callback_url': url_callback
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao criar webhook: {e}")
            return None

    def get_notifications(self):
        """Listar webhooks configurados"""
        url = f"{self.api_url}/applications/{self.config['APP_ID']}/notifications"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao listar webhooks: {e}")
            return []

    def delete_notification(self, notification_id):
        """Deletar um webhook"""
        url = f"{self.api_url}/applications/{self.config['APP_ID']}/notifications/{notification_id}"
        
        try:
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar webhook: {e}")
            return False
