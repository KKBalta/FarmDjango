from rest_framework.permissions import BasePermission

class PublicOrAuthenticated(BasePermission):
    """
    Allow public access to certain endpoints and require authentication for others.
    """
    public_endpoints = [
        '/api/auth/register/',
        '/api/auth/password-reset-request/',
        'api/auth/password-reset-confirm/',
        
    ]

    def has_permission(self, request, view):
        if request.path in self.public_endpoints:
            return True  # Public access
        return request.user and request.user.is_authenticated  # Require login for others
