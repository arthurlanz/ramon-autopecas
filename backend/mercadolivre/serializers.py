from rest_framework import serializers
from .models import MLCredential, MLSyncLog

class MLCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLCredential
        fields = ['id', 'user_id', 'token_type', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MLSyncLogSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    
    class Meta:
        model = MLSyncLog
        fields = ['id', 'product', 'product_title', 'action', 'status', 
                  'request_data', 'response_data', 'error_message', 'created_at']
        read_only_fields = ['id', 'created_at']
