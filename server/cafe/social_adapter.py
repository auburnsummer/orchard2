from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CafeSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.email:
            user.email = f"{user.id}@cafe.invalid"
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data
        if 'global_name' in extra_data and extra_data['global_name']:
            user.display_name = extra_data['global_name']
        elif 'username' in extra_data and extra_data['username']:
            user.display_name = extra_data['username']
        else:
            user.display_name = "Unknown"
        user.save()

