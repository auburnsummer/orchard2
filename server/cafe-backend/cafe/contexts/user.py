from django.urls import reverse

from allauth.socialaccount.models import SocialAccount

def try_get_avatar(user):
    try:
        social_account = SocialAccount.objects.get(user=user)
        avatar_url = social_account.get_avatar_url()
        if avatar_url:
            return avatar_url
        else:
            return None
    except SocialAccount.DoesNotExist:
        return None

def user(request):
    if request.user.is_authenticated:
        return {
            "authenticated": True,
            "id": request.user.id,
            "displayName": request.user.get_short_name(),
            "avatarURL": try_get_avatar(request.user),
            "theme_preference": request.user.theme_preference
        }
    else:
        return {
            "authenticated": False
        }