from datetime import datetime
import httpx
from huey.contrib.djhuey import db_task, periodic_task
from huey import crontab
import random
import jsonata

from cafe.models.rdlevels.daily_blend import DailyBlend, get_blend_date
from cafe.models.rdlevels.daily_blend_configuration import DailyBlendConfiguration

def todays_blend_or_pool():
    today = get_blend_date()
    from cafe.models.rdlevels.daily_blend import DailyBlend
    try:
        daily_blend = DailyBlend.objects.get(featured_date=today)
        return daily_blend
    except DailyBlend.DoesNotExist:
        # get something from the pool
        from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
        pool = DailyBlendRandomPool.objects.all()
        if pool.count() == 0:
            return None
        pool_entry = random.choice(pool)
        # make a DailyBlend for today with this level
        daily_blend = DailyBlend.objects.create(
            level=pool_entry.level,
            featured_date=today,
            blended=False
        )
        # remove from pool
        pool_entry.delete()
        return daily_blend
    
def blend_blend(blend: DailyBlend):
    config = DailyBlendConfiguration.get_config()
    webhook_urls = config.webhook_urls
    jsonata_script = config.jsonata_script
    evaluator = jsonata.Jsonata(jsonata_script)
    level_dict = blend.level.to_dict()
    payload = evaluator.evaluate(level_dict)
    for url in webhook_urls.splitlines():
        url = url.strip()
        if url == "":
            continue
        httpx.post(url, json=payload)

@db_task(priority=200)
def run_daily_blend_task(force: bool = False):
    blend = todays_blend_or_pool()
    if blend is None:
        raise ValueError("No daily blend available and pool is empty")
    
    if blend.blended and not force:
        return  # already blended

    blend_blend(blend)

# at 5:00 AM GMT every day, run the task to blend the daily blend
# actually 5:01 to be safe, since the blend updates at 5:00 AM GMT and we want to make sure we get the new blend
@periodic_task(crontab(hour=5, minute=1, strict=True), priority=200, expires=3600)
def daily_blend_schedule():
    run_daily_blend_task(False)