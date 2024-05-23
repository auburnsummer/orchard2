from typing import Any
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, UserManager
from cafe.libs.gen_id import IDType, gen_id

from .utils import create_pk_field

class CafeUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        For compatability with other parts of the django ecosystem, we do some trickery here.

        Orchard always uses opaque usernames. The actual "name" of the user is first_name. If
        username is given, and first_name is not, we make the given username the first_name and
        generate a new opaque username.

        If display_name is given, we assume it's code that is aware of our system, and leave it as-is.
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
    
    objects = CafeUserManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(username__startswith="u_"),
                name="cafe__user__username_startswith_u_"
            )
        ]