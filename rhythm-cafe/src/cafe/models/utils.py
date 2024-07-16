from django.db import models
from cafe.libs.gen_id import default_id, IDType

def create_pk_field(id_type: IDType, **kwargs):
    return models.CharField(default=default_id(id_type), max_length=24, primary_key=True, **kwargs)