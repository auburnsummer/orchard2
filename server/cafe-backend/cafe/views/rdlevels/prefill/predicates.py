from typing import TYPE_CHECKING, TypedDict, Literal

from django.core.signing import BadSignature
from django.utils.timezone import timedelta
import rules
from cafe.views.discord_bot.handlers.add import addlevel_signer

from cafe.models import User
from cafe.models.clubs.club import Club

from allauth.socialaccount.models import SocialAccount

def check_if_ok_to_continue(user: User, code: str) -> bool:
    # 1. the code must be valid.
    try:
        result = addlevel_signer.unsign_object(code, max_age=timedelta(days=1))
    except BadSignature:
        return False
    
    # 2. The club must exist.
    if not Club.objects.filter(id=result["club_id"]).exists():
        return False
    
    # 3. one of these two conditions must be true:
    #    a. the user is linked to the discord account that posted the message.
    #    b. the user is an admin or owner of the club.
    discord_user_id = result['discord_user_id']

    discord_social_account = SocialAccount.objects.filter(user=user, provider='discord', uid=discord_user_id).first()
    if discord_social_account:
        return True
    
    club = Club.objects.get(id=result['club_id'])
    return user.has_perm('cafe.create_delegated_levels_for_club', club)

def register_imports():
    rules.add_perm('prefill.ok', check_if_ok_to_continue)