from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CafeSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.display_name = sociallogin.account.extra_data.get('global_name')
        user.save()

