from django.db import models

def get_default_user_profile(user):
    return UserProfile(
        user=user,
        theme_pref='light'
    )

class UserProfile(models.Model):
    """
    A UserProfile contains additional information about a User.

    Each User can have up to one UserProfile. A User may not have a UserProfile; in that case,
    it's assumed their profile is the default.
    """
    user = models.OneToOneField(
        'cafe.User',
        on_delete=models.CASCADE,
        primary_key=True
    )
    theme_pref = models.CharField(choices={
        'light': 'Light',
        'dark': 'Dark'
    }, max_length=100)