from __future__ import annotations
from typing import TYPE_CHECKING
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Q, CharField, CheckConstraint, EmailField, QuerySet

from .id_utils import generate_user_id, USER_ID_PREFIX

if TYPE_CHECKING:
    from cafe.models.clubs.club_membership import ClubMembership 
    from django.db.models.manager import RelatedManager

class CafeUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = super().create_user(username, password=password, **extra_fields)
        if user.email == "":
            user.email = None
            user.save()
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        user = super().create_superuser(username, password=password, **extra_fields)
        if user.email == "":
            user.email = None
            user.save()
        return user


class User(AbstractUser):
    """
    Custom user model for rcafe. Compared to the default Django user model:

     - The PK is replaced with an ID field that starts with "u".
     - the username field still exists, for compat with the rest of the Django ecosystem, but we don't use it.
     - instead, the display_name field is used for the user's display name, and most things are hooked up to that.
     - ...generally speaking, if a Django integration is a good citzen and uses the get_short_name() function it
       shouldn't need to know about this display_name/username trickery.
    """
    id = CharField(max_length=10, primary_key=True, default=generate_user_id)
    username = CharField(max_length=150, unique=False, blank=True)
    display_name = CharField(max_length=150, unique=False, blank=True)
    email = EmailField(default=None, null=True, unique=True, blank=True)
    theme_preference = CharField(choices={
        'light': 'Light',
        'dark': 'Dark',
        'system': 'System'
    }, max_length=100, default='light')

    # from cafe.ClubMembership
    memberships: RelatedManager[ClubMembership]

    def get_full_name(self) -> str:
        return self.display_name
    
    def get_short_name(self) -> str:
        return self.display_name

    def __str__(self):
        return f"{self.display_name} ({self.id})"

    def to_dict_private(self):
        return {
            "authenticated": True,
            "id": self.id,
            "displayName": self.get_short_name(),
            "avatarURL": try_get_avatar(self),
            "theme_preference": self.theme_preference,
            "is_superuser": self.is_superuser,
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "displayName": self.get_short_name(),
            "avatarURL": try_get_avatar(self),
        }

    objects = CafeUserManager()

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["username", "display_name"]

    class Meta:
        constraints = [
            CheckConstraint(
                name="cafe__user_id_starts_with_u",
                check=Q(id__startswith=USER_ID_PREFIX),
            )
        ]

def try_get_avatar(user):
    try:
        social_account = SocialAccount.objects.get(user=user)
        avatar_url = social_account.get_avatar_url()
        if avatar_url:
            return avatar_url
        else:
            return None
    except SocialAccount.DoesNotExist:
        return None