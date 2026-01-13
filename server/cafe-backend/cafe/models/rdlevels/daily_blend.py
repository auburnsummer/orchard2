from django.db import models
from vitals.msgspec_schema import datetime
from cafe.models.rdlevels.rdlevel import RDLevel

def get_todays_blend():
    today = datetime.today()
    try:
        daily_blend = DailyBlend.objects.get(featured_date=today)
        return daily_blend.level
    except DailyBlend.DoesNotExist:
        # get the most recent past blend
        past_blends = DailyBlend.objects.filter(featured_date__lt=today).order_by('-featured_date')
        if past_blends.exists():
            return past_blends.first().level
        return None

class DailyBlend(models.Model):
    """
    Represents the blended level for a specific date.
    Only one level can be blended per day.
    """
    level = models.ForeignKey(RDLevel, on_delete=models.CASCADE)
    featured_date = models.DateField(unique=True, db_index=True)
    blended = models.BooleanField(default=False)

    def to_dict(self):
        return {
            "level": self.level.to_dict(),
            "featured_date": self.featured_date.isoformat(),
            "blended": self.blended,
        }

    class Meta:
        ordering = ['-featured_date']

    def __str__(self):
        return f"{self.level} - {self.featured_date} [{"Blended" if self.blended else "Not Blended"}]"
