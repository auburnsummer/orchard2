from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField

class CafeUserManager(UserManager):
    pass

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

    USERNAME_FIELD = "id"

    REQUIRED_FIELDS = ["username"]