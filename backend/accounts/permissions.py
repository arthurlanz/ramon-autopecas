from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """Apenas dono ou admin pode acessar"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.role == 'owner':
            return True
        return obj == request.user


class IsOwnerOrAdvertiser(permissions.BasePermission):
    """Apenas dono ou anunciador pode acessar"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['owner', 'advertiser']
        )
