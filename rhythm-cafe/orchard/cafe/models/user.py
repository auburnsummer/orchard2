from django.db import models
from django.contrib.auth.models import AbstractUser
from cafe.libs.gen_id import IDType

from .utils import create_pk_field

class User(AbstractUser):
    """
    User. Compared to the base django User, we're:
     - username is always opaque
     - instead of first and last name, we're using a display name
     - emails are unique
    """
    username = create_pk_field(IDType.USER)
    display_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, blank=True, null=True)

    REQUIRED_FIELDS = ["display_name"]

    def get_full_name(self) -> str:
        return self.display_name
    
    def get_short_name(self) -> str:
        return self.display_name
    
    def __str__(self):
        return f"{self.display_name} ({self.username})"