from django.middleware.csrf import get_token

def csrf_token(request):
    return get_token(request)