from cafe.models.user import User
from cafe.views.types import HttpRequest

def user(request: HttpRequest):
    if request.user.is_authenticated:
        assert isinstance(request.user, User)
        return request.user.to_dict_private()
    else:
        theme_preference = request.session.get("theme_preference", "light")
        pr_default_preference = request.session.get("default_pr_preference", "approved")
        return {
            "authenticated": False,
            "theme_preference": theme_preference,
            "default_pr_preference": pr_default_preference,
        }