from datetime import date
import json
import textwrap

from django.urls import reverse
from huey.contrib.djhuey import task
from cafe.models.rdlevels.blend_pool import BlendPool
from cafe.models.rdlevels.daily_blend import DailyBlend
from cafe.models.rdlevels.daily_blend_configuration import DailyBlendConfiguration
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User, try_get_avatar
from cafe.webhooks import is_allowed_webhook_url

import httpx
from loguru import logger
from orchard.settings import DOMAIN_URL

from difflib import unified_diff

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
                "title": f"{date.strftime(r'%d %B %Y')}",
                "description": description,
                "color": 0x00ff00,
                **_user_fields(user, "Updated"),
            }
        ]
    }

def blend_paused(paused: bool, user: User):
    return {
        "embeds": [
            {
                "author": {"name": "Blend Schedule Paused" if paused else "Blend Schedule Unpaused"},
                "color": 0xffff00,
                **_user_fields(user, "Updated"),
            }
        ]
    }

def webhook_urls_changed(old_urls: str, new_urls: str, user: User):
    diff = unified_diff(old_urls.splitlines(), new_urls.splitlines(), lineterm="")
    description = textwrap.dedent(f"""
        ```diff
        {'\n'.join(diff)}
        ```                     
    """)
    return {
        "embeds": [
            {
                "author": {"name": "Blend Webhook URLs Updated"},
                "description": description,
                "color": 0x00ff00,
                **_user_fields(user, "Updated"),
            }
        ]
    }

def jsonata_changed(old_script: str, new_script: str, user: User):
    diff = unified_diff(old_script.splitlines(), new_script.splitlines(), lineterm="")
    description = textwrap.dedent(f"""
        ```diff
        {'\n'.join(diff)}
        ```                     
    """)
    return {
        "embeds": [
            {
                "author": {"name": "Blend JSONata Script Updated"},
                "description": description,
                "color": 0x00ff00,
                **_user_fields(user, "Updated"),
            }
        ]
    }

def reporting_url_changed(new_url: str, user: User):
    return {
        "embeds": [
            {
                "author": {"name": "Blend Reporting Webhook URL Updated"},
                "description": f"New URL: `{new_url}`",
                "color": 0x00ff00,
                **_user_fields(user, "Updated"),
            }
        ]
    }

def blend_pool_deleted(pool_name: str, user: User):
    return {
        "embeds": [
            {
                "author": {"name": "Blend Pool Deleted"},
                "title": pool_name,
                "description": f"Pool **{pool_name}** was deleted.",
                "color": 0xff0000,
                **_user_fields(user, "Deleted"),
            }
        ]
    }

def blend_pool_name_changed(old_name: str, new_name: str, user: User):
    return {
        "embeds": [
            {
                "author": {"name": "Blend Pool Renamed"},
                "description": f"**{old_name}** was renamed to **{new_name}**.",
                "color": 0x00ff00,
                **_user_fields(user, "Renamed"),
            }
        ]
    }

def blend_pool_weighting_system_changed(pool_name: str, old_system: str, new_system: str, user: User):
    description = f"**{pool_name}** weighting system was changed from `{old_system}` to `{new_system}`."
    return {
        "embeds": [
            {
                "author": {"name": "Blend Pool Weighting System Updated"},
                "description": description,
                "color": 0x00ff00,
                **_user_fields(user, "Updated"),
            }
        ]
    }

def blend_pool_member_tickets_changed(rdlevel: RDLevel, pool: BlendPool, new_tickets: int, user: User):
    description = f"Tickets for **{rdlevel.song}** in pool **{pool.name}** were changed to `{new_tickets}`."
    return {
        "embeds": [
            {
                "author": {"name": "Blend Pool Member Tickets Updated"},
                "description": description,
                "color": 0x00ff00,
                **_user_fields(user, "Updated"),
            }
        ]
    }

@task()
def report_blend_change(data: dict, override_webhook_url: str | None = None):
    config = DailyBlendConfiguration.get_config()

    reporting_webhook_url = override_webhook_url or config.reporting_webhook_url

    if not reporting_webhook_url:
        logger.warning("No reporting webhook URL configured, skipping blend change report")
        return

    if not is_allowed_webhook_url(reporting_webhook_url):
        logger.warning("Reporting webhook URL is not allowed, skipping blend change report")
        return
    
    r = httpx.post(reporting_webhook_url, json=data)
    r.raise_for_status()
