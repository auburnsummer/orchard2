from datetime import timedelta
from operator import ge
from cafe.views.discord_bot.handlers.add import addlevel_signer
from django.core.signing import BadSignature

from django.core.exceptions import BadRequest, ObjectDoesNotExist

from cafe.models import Club, User
from cafe.models.club import is_at_least_admin
from cafe.models.rdlevel_prefill import RDLevelPrefillResult
from oauthlogin.models import OAuthConnection

from cafe.libs.gen_id import gen_id, IDType

from loguru import logger

import datetime

import rules

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

def get_or_create_user_for_discord_user(discord_user_id, name_hint):
    "must be called from POST request"
    try:
        oauth_connection = OAuthConnection.objects.get(
            provider_key='discord',
            provider_user_id=discord_user_id,
        )
        return oauth_connection.user
    except OAuthConnection.DoesNotExist:
        username = gen_id(IDType.USER)
        user = User.objects.create_user(username=username, first_name=name_hint)
        user.save()
        # create a "synthetic" connection with an expired token
        # since this user never actually logged into discord, we don't have a real discord token...
        # but by setting an expired one, it will force a refresh if/when they actually log in.
        connection = OAuthConnection.objects.create(
            user=user,
            provider_key='discord',
            provider_user_id=discord_user_id,
            access_token='dummyvalue',
            access_token_expires_at=datetime.datetime.fromtimestamp(1)
        )
        connection.save()
        return user

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
        raise Club.DoesNotExist("club does not exist")
    
    # 3. one of these two conditions must be true:
    #    a. the user is linked to the discord account that posted the message.
    #    b. the user is an admin or owner of the club.
    discord_user_id = result['discord_user_id']

    if not _user_allowed(discord_user_id, user, club):
        raise BadRequest("User does not have permissions to do this action")

    return None

@rules.predicate
def ok_to_continue_rule(user, code):
    try:
        check_if_ok_to_continue(code, user)
        return True
    except Exception as e:
        return False

@rules.predicate
def can_access_prefill(user, prefill: RDLevelPrefillResult):
    if user == prefill.user:
        return True
    if is_at_least_admin(user, prefill.club):
        return True
    return False

rules.add_perm('prefill.can_access_prefill', can_access_prefill)
    
rules.add_perm('prefill.ok', ok_to_continue_rule)