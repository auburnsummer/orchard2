from typing import Any
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, UserManager
from cafe.libs.gen_id import IDType, gen_id

from .user_profile import get_default_user_profile
from .utils import create_pk_field

class CafeUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        For compatability with other parts of the django ecosystem, we do some trickery here.

        Orchard always uses opaque usernames. The actual "name" of the user is first_name. (we don't
        render last_name anywhere.)
        If username is given, and first_name is not, we make the given username the first_name and
        generate a new opaque username.

        If first_name is given, we assume it's code that is aware of our system, and leave it as-is.
        """
        if extra_fields.get("first_name") is None:        
            extra_fields["first_name"] = username
            username = gen_id(IDType.USER)

        return super().create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if extra_fields.get("first_name") is None:        
            extra_fields["first_name"] = username
            username = gen_id(IDType.USER)

        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    """
    User. Compared to the base django User, we're:
     - username is always opaque
     - only the first name is used
     - emails are unique
    """
    username = create_pk_field(IDType.USER)
    email = models.EmailField(unique=True)
    first_name = models.CharField(blank=False, max_length=100)

    REQUIRED_FIELDS = ["first_name", "email"]

    def get_full_name(self) -> str:
        return self.first_name
    
    def get_short_name(self) -> str:
        return self.first_name

    def __str__(self):
        return f"{self.first_name} ({self.username})"
    
    @property
    def profile(self):
        """
        Return the profile of the user. If the user doesn't have a profile,
        creates an ephemeral one. You can save the ephemeral profile but make sure it's
        stored in a variable, because each call to this will make a new ephemeral profile, e.g.

        ```
        new_profile = user.profile
        new_profile.theme_pref = '...'
        new_profile.save()
        ```
        """
        try:
            return self.userprofile
        except ObjectDoesNotExist:
            return get_default_user_profile(self)
    
    objects = CafeUserManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(username__startswith="u_"),
                name="cafe__user__username_startswith_u_"
            )
        ]