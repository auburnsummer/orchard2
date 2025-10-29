from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from cafe.models import User


class ApiKeyAuthenticationMiddleware:
    """
    Middleware that authenticates users via API key in the Authorization header.
    
    If an API key is provided in the format "Bearer <key>", this middleware will
    attempt to authenticate the user with that key and set request.user.
    
    If no API key is provided or authentication fails, the request proceeds normally
    (allowing session-based authentication to work).
    
    Note: API keys are cryptographically signed tokens containing user_id:iteration.
    The signature is validated and the iteration number is checked against the user's
    current api_key_iter to ensure the key hasn't been revoked.
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
            if user:
                request.user = user
                request.api_key_authenticated = True
            else:
                request.api_key_authenticated = False
        else:
            request.api_key_authenticated = False
        
        response = self.get_response(request)
        return response
