from __future__ import annotations
from typing import TYPE_CHECKING
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.signing import Signer, BadSignature
from django.db.models import Q, CharField, CheckConstraint, EmailField, QuerySet, IntegerField

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
    api_key_iter = IntegerField(default=0)
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
    
    def generate_api_key(self) -> str:
        """
        Generate a new API key for this user, revoking any existing one.
        
        Returns a signed token containing the user ID and iteration number.
        The iteration number is incremented each time a new key is generated,
        automatically invalidating all previous keys.
        """
        # Increment the iteration counter
        self.api_key_iter += 1
        self.save()
        
        # Create a signed token with user_id and iteration
        signer = Signer()
        value = {"user_id": self.id, "iter": self.api_key_iter}
        signed_token = signer.sign_object(value)
        
        return signed_token
    
    def check_api_key(self, signed_token: str) -> bool:
        """
        Check if the provided signed API key is valid for this user.
        
        Validates both the signature and that the iteration number matches.
        """
        try:
            signer = Signer()
            value = signer.unsign_object(signed_token)
            
            # Check that it's for this user and the iteration matches
            return (
                value.get("user_id") == self.id and
                value.get("iter") == self.api_key_iter
            )
            
        except (BadSignature, AttributeError, TypeError):
            return False
    
    @classmethod
    def get_user_from_api_key(cls, signed_token: str) -> "User | None":
        """
        Get the user associated with a signed API key.
        
        Unsigns the token to extract the user ID, looks up that user,
        and validates that the iteration number matches.
        
        Returns None if the token is invalid or doesn't match.
        """
        try:
            signer = Signer()
            value = signer.unsign_object(signed_token)
            
            # Extract user_id from the unsigned object
            user_id = value.get("user_id")
            if not user_id:
                return None
            
            # Look up the user
            user = cls.objects.get(id=user_id)
            
            # Validate the full token (including iteration check)
            if user.check_api_key(signed_token):
                return user
            
        except (BadSignature, cls.DoesNotExist, AttributeError, TypeError):
            pass
        
        return None
    
    def revoke_api_key(self) -> None:
        """
        Revoke the user's API key by incrementing the iteration counter.
        
        This invalidates all previously generated keys without needing to
        track them individually.
        """
        self.api_key_iter += 1
        self.save()

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