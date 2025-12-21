from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from rules.contrib.views import objectgetter, permission_required
import requests
from urllib.parse import unquote

from cafe.views.types import AuthenticatedHttpRequest
from cryptography.fernet import Fernet, InvalidToken

@csrf_exempt
@permission_required("cafe.blend_rdlevel")
def execute_webhook(request: AuthenticatedHttpRequest, code: str):
    """
    Decrypts an encrypted Discord webhook URL and forwards the request to it.
    
    Args:
        request: The incoming HTTP request
        code: URL-encoded encrypted Discord webhook URL
    """
    try:
        cipher = Fernet(settings.WEBHOOK_ENCRYPTION_KEY.encode())
        
        encrypted_url = unquote(code)
        decrypted_url = cipher.decrypt(encrypted_url.encode()).decode()
        
        # Forward the request to the decrypted webhook URL
        headers = {
            'Content-Type': request.content_type,
            'User-Agent': request.META.get('HTTP_USER_AGENT', 'orchard2'),
        }
        
        response = requests.request(
            method=request.method,
            url=decrypted_url,
            data=request.body,
            headers=headers,
            timeout=10
        )
        
        # Return the response from Discord
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/json')
        )
        
    except InvalidToken:
        return JsonResponse(
            {"error": "Invalid or corrupted webhook code"},
            status=400
        )
    except requests.RequestException as e:
        return JsonResponse(
            {"error": f"Failed to forward request: {str(e)}"},
            status=502
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Unexpected error: {str(e)}"},
            status=500
        )