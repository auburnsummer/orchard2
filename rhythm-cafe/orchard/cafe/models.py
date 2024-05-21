from django.db import models
from django.contrib.auth.models import AbstractUser
from cafe.libs.gen_id import default_id, IDType

def create_pk_field(id_type: IDType):
    return models.CharField(default=default_id(id_type), max_length=24, primary_key=True)

# Create your models here.

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
    
    
class Publisher(models.Model):
    """
    A Publisher is a source where levels come from (RDL, RWU, etc.)

    Users can be admins of Publishers. This is just done via permissions.
    todo: each Publisher should have a permission associated with it.
    """
    id = create_pk_field(IDType.PUBLISHER)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name} ({self.id})"

class RDLevel(models.Model):
    """
    An RDLevel represents a single Rhythm Doctor level.
    """
    id = create_pk_field(IDType.RD_LEVEL)
    song = models.TextField(blank=False)