from datetime import timedelta
from cafe.views.discord_bot.handlers.add import addlevel_signer
from django.core.signing import BadSignature

from django.core.exceptions import BadRequest, ObjectDoesNotExist

from cafe.models import Club
from cafe.models.club import is_at_least_admin
from oauthlogin.models import OAuthConnection

def _user_allowed(discord_user_id, user, club):
    # a. the user is linked to the discord account that posted the message.
    try:
        OAuthConnection.objects.get(
            provider_key='discord',
            provider_user_id=discord_user_id,
            user=user
        )
        return True
    except OAuthConnection.DoesNotExist:
        # we should try b as well
        pass
    
    # b. the user is an admin or owner of the club.
    return is_at_least_admin(user, club)

def check_if_ok_to_continue(code, user):
    # 1. the code must be valid.
    try:
        result = addlevel_signer.unsign_object(code, max_age=timedelta(days=7))
    except BadSignature:
        raise BadRequest("Code invalid, try running command again")

    # 2. the club must exist.
    club_id = result['club_id']
    try:
        club = Club.objects.get(id=club_id)
    except Club.DoesNotExist:
        raise ObjectDoesNotExist("club does not exist")
    
    # 3. one of these two conditions must be true:
    #    a. the user is linked to the discord account that posted the message.
    #    b. the user is an admin or owner of the club.
    discord_user_id = result['discord_user_id']

    if not _user_allowed(discord_user_id, user, club):
        raise BadRequest("User does not have permissions to do this action")

    return None