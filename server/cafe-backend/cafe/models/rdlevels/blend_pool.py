from django.db.models import CharField
from rules.contrib.models import RulesModel
from cafe.models.id_utils import BLENDPOOL_ID_LENGTH, generate_blend_pool_id

DEFAULT_BLEND_POOL_ID = "bdefault"

class BlendPool(RulesModel):
    id = CharField(primary_key=True, max_length=BLENDPOOL_ID_LENGTH, default=generate_blend_pool_id)
    name = CharField(null=False, blank=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __str__(self):
        return f"Blend pool: {self.name} ({self.id})"

def get_default_blend_pool() -> BlendPool:
    return BlendPool.objects.get(id=DEFAULT_BLEND_POOL_ID)
