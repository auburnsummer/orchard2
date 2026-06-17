from datetime import date
import json
import textwrap

from django.urls import reverse
from huey.contrib.djhuey import task
from cafe.models.rdlevels.blend_pool import BlendPool
from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
from cafe.models.rdlevels.daily_blend import DailyBlend
from cafe.models.rdlevels.daily_blend_configuration import DailyBlendConfiguration
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User, try_get_avatar
from cafe.webhooks import is_allowed_webhook_url

import httpx
from loguru import logger
from orchard.settings import DOMAIN_URL

def _common_rdlevel_pool_fields(rdlevel: RDLevel, pool: BlendPool):
    title = f"{rdlevel.song} ({rdlevel.song_alt})" if rdlevel.song_alt else rdlevel.song
    level_link = DOMAIN_URL + reverse("cafe:level_view", args=[rdlevel.id])
    pool_link = DOMAIN_URL + reverse("cafe:blend_pool", args=[pool.id])
    return {
        "title": title,
        "description": textwrap.dedent(f"""
            by **{",".join(rdlevel.authors)}**
            Pool: **[{pool.name}]({pool_link})**
        """),
        "url": level_link,
        "thumbnail": {
            "url": rdlevel.thumb_url,
        },
    }

def _user_fields(user: User, verb: str):
    return {
        "footer": {
            "text": f"{verb} by {user.display_name}",
            "icon_url": try_get_avatar(user),
        }
    }

def rdlevel_added_to_pool(rdlevel: RDLevel, pool: BlendPool, user: User):
    return {
        "embeds": [
            {
                **_common_rdlevel_pool_fields(rdlevel, pool),
                "color": 0x00ff00,
                "author": {"name": "Blend Pool Level Added"},
                **_user_fields(user, "Added"),
            }
        ]
    }

def rdlevel_removed_from_pool(rdlevel: RDLevel, pool: BlendPool, user: User):
    return {
        "embeds": [
            {
                **_common_rdlevel_pool_fields(rdlevel, pool),
                "color": 0xff0000,
                "author": {"name": "Blend Pool Level Removed"},
                **_user_fields(user, "Removed"),
            }
        ]
    }

def daily_blend_descriptor(blend: DailyBlend):
    if blend.pool:
        pool_link = DOMAIN_URL + reverse("cafe:blend_pool", args=[blend.pool.id])
        return f"Pool: **[{blend.pool.name}]({pool_link})**"
    elif blend.level:
        level_link = DOMAIN_URL + reverse("cafe:level_view", args=[blend.level.id])
        return f"Level: **[{blend.level.song}]({level_link})**"
    else:
        raise ValueError("Tried to get description of a DailyBlend with no level or pool")

def blend_schedule_changed(date: date, prev: DailyBlend | None, new: DailyBlend | None, user: User):
    description = textwrap.dedent(f"""
        **Was**
        {daily_blend_descriptor(prev) if prev else "None"}
        **Now**
        {daily_blend_descriptor(new) if new else "None"}
    """)
    return {
        "embeds": [
            {
                "author": {"name": "Blend Schedule Update"},
                "title": f"{date.strftime('%m %B %Y')}",
                "description": description,
                "color": 0x00ff00,
                **_user_fields(user, "Updated"),
            }
        ]
    }

@task()
def report_blend_change(data: dict):
    config = DailyBlendConfiguration.get_config()

    reporting_webhook_url = config.reporting_webhook_url

    if not reporting_webhook_url:
        logger.warning("No reporting webhook URL configured, skipping blend change report")
        return

    if not is_allowed_webhook_url(reporting_webhook_url):
        logger.warning("Reporting webhook URL is not allowed, skipping blend change report")
        return
    
    logger.info(json.dumps(data))

    r = httpx.post(reporting_webhook_url, json=data)
    r.raise_for_status()
