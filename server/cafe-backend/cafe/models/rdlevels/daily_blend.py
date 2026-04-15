from django.db import models
from django.utils import timezone
from datetime import timedelta
from cafe.models.rdlevels.rdlevel import RDLevel

BLEND_CUTOFF_HOUR = 4  # 4:00 AM GMT cutoff for daily blend updates

def get_blend_date():
    """
    Get the current blend date based on 4:00 AM GMT cutoff.
    The blended level updates at 0400 GMT, so before that time,
    the "current" blend date is still yesterday.
    """
    now_utc = timezone.now()
    cutoff_hour = BLEND_CUTOFF_HOUR
    
    if now_utc.hour < cutoff_hour:
        # Before 4:00 AM GMT, use yesterday's date
        return (now_utc - timedelta(days=1)).date()
    else:
        # After 4:00 AM GMT, use today's date
        return now_utc.date()

def get_todays_blend():
    blend_date = get_blend_date()
    try:
        daily_blend = DailyBlend.objects.get(featured_date=blend_date)
        return daily_blend.level
    except DailyBlend.DoesNotExist:
        # get the most recent past blend
        past_blends = DailyBlend.objects.filter(featured_date__lt=blend_date).order_by('-featured_date')
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
