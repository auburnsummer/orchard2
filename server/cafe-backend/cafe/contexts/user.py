from cafe.views.types import HttpRequest

def user(request: HttpRequest):
    if request.user.is_authenticated:
        return request.user.to_dict_private()
    else:
        theme_preference = request.session.get("theme_preference", "light")
        return {
            "authenticated": False,
            "theme_preference": theme_preference
        }