from django.urls import reverse


def user(request):
    if request.user.is_authenticated:
        return {
            "authenticated": True,
            "id": request.user.id,
            "username": request.user.username,
        }
    else:
        return {
            "authenticated": False
        }