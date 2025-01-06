from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Q, CharField, CheckConstraint, EmailField

from .id_utils import generate_user_id, USER_ID_PREFIX

class CafeUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        return super().create_user(username, email=None, password=password, **extra_fields)
    
    def create_superuser(self, username, password, **extra_fields):
        return super().create_superuser(username, email=None, password=password, **extra_fields)

class User(AbstractUser):
    """
    Custom user model for rcafe. Compared to the default Django user model:

     - The PK is replaced with an ID field that starts with "u".
     - the username field still exists, for compat with the rest of the Django ecosystem, but we don't use it.
     - instead, the display_name field is used for the user's display name, and most things are hooked up to that.
    """
    id = CharField(max_length=10, primary_key=True, default=generate_user_id)
    username = CharField(max_length=150, unique=False, blank=True)
    display_name = CharField(max_length=150, unique=False, blank=True)
    email = EmailField(default=None, null=True, unique=True, blank=True)

    def get_full_name(self) -> str:
        return self.display_name
    
    def get_short_name(self) -> str:
        return self.display_name

    def __str__(self):
        return f"{self.display_name} ({self.id})"
    
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