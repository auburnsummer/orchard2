from rules.contrib.models import RulesModel

from django.db import models

from django.db.models import Q

class DailyBlendRandomPool(RulesModel):
    level = models.ForeignKey('cafe.RDLevel', on_delete=models.CASCADE)
    pool = models.ForeignKey('cafe.BlendPool', on_delete=models.CASCADE)
    tickets = models.IntegerField(default=1)

    def to_dict(self):
        return {
            "level": self.level.to_dict(),
            "pool": self.pool.to_dict(),
            "tickets": self.tickets
        }

    def __str__(self):
        return f"In pool {self.pool}, {self.level}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="tickets_greater_than_zero",
                condition=Q(tickets__gt=0)
            )
        ]