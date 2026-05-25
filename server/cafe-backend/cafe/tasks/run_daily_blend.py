from datetime import datetime
import httpx
from huey.contrib.djhuey import db_task, periodic_task
from huey import crontab
import random
import jsonata

from cafe.models.rdlevels.daily_blend import DailyBlend, get_blend_date
from cafe.models.rdlevels.daily_blend_configuration import DailyBlendConfiguration
from cafe.models.rdlevels.blend_pool import get_default_blend_pool
from cafe.webhooks import is_allowed_webhook_url

def todays_blend_or_default() -> DailyBlend:
    "Get the blend for today, if there isn't one, create one set to the default pool."
    today = get_blend_date()
    from cafe.models.rdlevels.daily_blend import DailyBlend
    try:
        daily_blend = DailyBlend.objects.get(featured_date=today)
        return daily_blend
    except DailyBlend.DoesNotExist:
        # create a default pool object.
        default_pool = get_default_blend_pool()
        daily_blend = DailyBlend.objects.create(
            pool=default_pool,
            featured_date=today,
            blended=False,
            level=None
        )
        return daily_blend

def resolve_pool_blend(blend: DailyBlend):
    "If a DailyBlend is set to a pool, pick a level out of the pool and resolve the DailyBlend to that level."
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
    if blend.level:
        return blend # no change needed, it's already set to a level.
    # blend.pool must be set at this point.
    pool_levels = DailyBlendRandomPool.objects.filter(pool=blend.pool)
    if pool_levels.count() == 0:
        return None
    
    pool_entry = random.choice(pool_levels)
    blend.level = pool_entry.level
    blend.pool = None
    # remove from pool. TODO: make this behaviour adjustable per pool.
    pool_entry.delete()
    blend.save()
    return blend
    
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
        if not is_allowed_webhook_url(url):
            continue
        httpx.post(url, json=payload)

@db_task(priority=200)
def run_daily_blend_task(force: bool = False):
    config = DailyBlendConfiguration.get_config()
    if config.paused:
        return  # daily blend is paused

    blend = todays_blend_or_default()
    resolve_pool_blend(blend)

    if blend.level is None:
        raise ValueError("No daily blend available and pool is empty")
    
    if blend.blended and not force:
        return  # already blended

    blend_blend(blend)

# at 4:00 AM GMT every day, run the task to blend the daily blend
# NOTE TO AUBURN: IF YOU EDIT THIS EDIT get_blend_date IN cafe/models/rdlevels/daily_blend.py TO MATCH THE NEW TIME
@periodic_task(crontab(hour=4, minute=0, strict=True), priority=200, expires=3600)
def daily_blend_schedule():
    run_daily_blend_task(False)