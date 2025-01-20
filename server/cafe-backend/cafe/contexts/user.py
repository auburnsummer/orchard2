from cafe.views.types import HttpRequest

def user(request: HttpRequest):
    if request.user.is_authenticated:
        return request.user.to_dict()
    else:
        return {
            "authenticated": False
        }