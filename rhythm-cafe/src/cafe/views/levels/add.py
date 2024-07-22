from cafe.views.discord_bot.handlers.add import addlevel_signer

from django.core.signing import BadSignature

from django.core.exceptions import BadRequest, ObjectDoesNotExist

from datetime import timedelta

from cafe.models import Club
from django.contrib.auth.decorators import login_required

from oauthlogin.models import OAuthConnection
from cafe.models.club import is_at_least_admin

from django.shortcuts import render

from .check import check_if_ok_to_continue

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
    # throws if we can't continue
    check_if_ok_to_continue(code, request.user)
    
    render_data = {
        "code": code
    }
    
    return render(request, "cafe/levels/add.jinja", render_data)
