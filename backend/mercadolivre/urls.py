from django.urls import path
from . import views

urlpatterns = [
    path('auth-url/', views.ml_auth_url, name='ml_auth_url'),
    path('callback/', views.ml_callback, name='ml_callback'),
    path('sync-all/', views.sync_all_products, name='sync_all_products'),
    path('import-orders/', views.import_ml_orders, name='import_ml_orders'),
]
