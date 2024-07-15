from cafe.views.discord_bot.handlers.add import addlevel_signer

from django.core.signing import BadSignature

from django.core.exceptions import BadRequest, ObjectDoesNotExist

from datetime import timedelta

from cafe.models import Club
from django.contrib.auth.decorators import login_required

from oauthlogin.models import OAuthConnection
from cafe.models.club import is_at_least_admin

from django.shortcuts import render

def ok_to_continue(discord_user_id, user, club):
    # one of these two conditions must be true:
    #    a. the user is linked to the discord account that posted the message.
    #    b. the user is an admin or owner of the club.
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

    return is_at_least_admin(user, club)


@login_required
def add(request, code):
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

    if not ok_to_continue(discord_user_id, request.user, club):
        raise BadRequest("User does not have permissions to do this action")
    
    return render(request, "levels/add.jinja", {})
