from django.db.models import Manager
from django.db import models
from django.utils import timezone
from datetime import timedelta, date
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.rdlevels.blend_pool import BlendPool
from django.db.models import Q

BLEND_CUTOFF_HOUR = 4  # 4:00 AM GMT cutoff for daily blend updates

def get_blend_date() -> date:
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


def get_todays_blend() -> RDLevel | None:
    blend_date = get_blend_date()
    try:
        daily_blend = DailyBlend.objects.get(featured_date=blend_date)
        if daily_blend.level:
            return daily_blend.level
        # the DailyBlend obj must be only set to a pool and hasn't resolved to a level yet.
        # it should resolve after the blend task runs. just show the previous one in the meantime.
        raise DailyBlend.DoesNotExist 
    except DailyBlend.DoesNotExist:
        # get the most recent past blend
        past_blends = DailyBlend.objects.filter(featured_date__lt=blend_date, level__isnull=False).order_by('-featured_date')
        first = past_blends.first()
        if first:
            return first.level
        return None

class DailyBlend(models.Model):
    """
    Represents the blended level or pool for a specific date.
    Only one level can be blended per day.
    """
    level = models.ForeignKey(RDLevel, on_delete=models.CASCADE, null=True)
    pool = models.ForeignKey(BlendPool, on_delete=models.CASCADE, null=True)
    featured_date = models.DateField(unique=True, db_index=True)
    blended = models.BooleanField(default=False)

    def to_dict(self):
        return {
            "level": self.level.to_dict() if self.level else None,
            "pool": self.pool.to_dict() if self.pool else None,
            "featured_date": self.featured_date.isoformat(),
            "blended": self.blended,
        }

    class Meta:
        ordering = ['-featured_date']
        constraints = [
            models.CheckConstraint(
                name="at_least_one_of_level_or_pool_is_not_null",
                condition=Q(level_id__isnull=False) | Q(pool_id__isnull=False)
            )
        ]

    def __str__(self):
        return f"{self.level or self.pool} - {self.featured_date} [{"Blended" if self.blended else "Not Blended"}]"

    objects: Manager["DailyBlend"]

