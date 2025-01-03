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
    Custom user model for rcafe. Compared to the default Django user model,
    this model has a unique ID and usernames are not unique.
    """
    id = CharField(max_length=10, primary_key=True, default=generate_user_id)
    username = CharField(max_length=150, unique=False)
    email = EmailField(default=None, null=True, unique=True, blank=True)

    def get_full_name(self) -> str:
        return self.username
    
    def get_short_name(self) -> str:
        return self.username

    def __str__(self):
        return f"{self.username} ({self.id})"
    
    objects = CafeUserManager()

    USERNAME_FIELD = "id"

    REQUIRED_FIELDS = ["username"]

    class Meta:
        constraints = [
            CheckConstraint(
                name="cafe__user_id_starts_with_u",
                check=Q(id__startswith=USER_ID_PREFIX),
            )
        ]