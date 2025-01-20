from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest as DJHttpRequest
from cafe.models.user import User

type MaybeUser = User | AnonymousUser

class HttpRequest(DJHttpRequest):
    "Stub type for view handlers."
    user: MaybeUser

class AuthenticatedHttpRequest(DJHttpRequest):
    "Stub type for view handlers that use @login_required decorator."
    user: User