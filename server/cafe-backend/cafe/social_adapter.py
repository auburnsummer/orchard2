from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CafeSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.email:
            user.email = f"{user.id}@cafe.invalid"
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.display_name = sociallogin.account.extra_data.get('global_name')
        user.save()

