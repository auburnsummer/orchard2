from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

from cafe.libs.discord_oauth import get_discord_user_from_oauth
from cafe.models import User

from django.forms import widgets

from oauthlogin.providers import get_provider_keys

def get_discord_user_from_connection(connection):
    if connection.access_token_expired():
        connection.refresh_access_token()
    user = get_discord_user_from_oauth(connection.access_token)
    return user

@login_required
def connections(request):
    disc_connections = request.user.oauth_connections.all().filter(provider_key__exact="discord")
    connection_map = { connection.provider_user_id: get_discord_user_from_connection(connection) for connection in disc_connections}

    render_data = {
        "oauth_provider_keys": get_provider_keys(),
        "connection_map": connection_map
    }

    return render(request, "cafe/profile/connections.jinja", render_data)
