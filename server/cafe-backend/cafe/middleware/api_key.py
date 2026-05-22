from django.http import HttpRequest
from cafe.models import User


class ApiKeyAuthenticationMiddleware:
    """
    Middleware that authenticates users via API key in the Authorization header.
    (The header should be in the format "Bearer <key>.")

    Falls through to session user if no key provided.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest):
        # Check for API key in Authorization header
        auth_header = request.headers.get('Authorization', '')
        
        if auth_header.lower().startswith('bearer '):
            api_key = auth_header[7:]  # Remove 'Bearer ' prefix
            
            # Unsign and validate the token
            user = User.get_user_from_api_key(api_key)
            if user and user.is_active:
                request.user = user
        
        response = self.get_response(request)
        return response
