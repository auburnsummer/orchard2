from rules.contrib.models import RulesModel

from django.db import models

class DailyBlendRandomPool(RulesModel):
    level = models.ForeignKey('cafe.RDLevel', on_delete=models.CASCADE)
    pool = models.ForeignKey('cafe.BlendPool', on_delete=models.CASCADE)

    def to_dict(self):
        return {
            "level": self.level.to_dict(),
            "pool": self.pool.to_dict()
        }

    def __str__(self):
        return f"In pool {self.pool}, {self.level}"