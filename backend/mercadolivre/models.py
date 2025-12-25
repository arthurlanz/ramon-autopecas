from django.db import models
from accounts.models import User


class MLCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ml_credential')
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_type = models.CharField(max_length=50, default='Bearer')
    expires_in = models.IntegerField()
    ml_user_id = models.BigIntegerField()  # ALTERADO AQUI
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ml_credentials'
    
    def __str__(self):
        return f"ML Credential for {self.user.username}"


class MLSyncLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Criar'),
        ('update', 'Atualizar'),
        ('sync', 'Sincronizar'),
        ('delete', 'Deletar'),
    ]
    
    STATUS_CHOICES = [
        ('success', 'Sucesso'),
        ('error', 'Erro'),
        ('pending', 'Pendente'),
    ]
    
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='ml_sync_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    request_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ml_sync_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action} - {self.status}"
