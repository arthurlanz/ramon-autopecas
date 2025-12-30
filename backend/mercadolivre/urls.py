from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('logs', views.MLSyncLogViewSet, basename='ml-logs')

urlpatterns = [
    path('', include(router.urls)),
    path('auth-url/', views.ml_auth_url, name='ml_auth_url'),
    path('callback/', views.ml_callback, name='ml_callback'),
    path('status/', views.ml_status, name='ml_status'),
    path('sync-all/', views.sync_all_products, name='sync_all_products'),
    path('import-products/', views.import_ml_products, name='import_ml_products'),
    path('import-orders/', views.import_ml_orders, name='import_ml_orders'),
    path('webhook/', views.ml_webhook, name='ml_webhook'),
    path('setup-webhooks/', views.setup_webhooks_view, name='setup_webhooks'),
    path('list-webhooks/', views.list_webhooks, name='list_webhooks'),
]
