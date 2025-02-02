from huey.contrib.djhuey import db_periodic_task, db_task
from orchard.settings import DISCORD_BOT_TOKEN

import httpx

from loguru import logger

@db_task()
def update_discord_guild_name(guild_id: str):
    # This task executes queries. Once the task finishes, the connection
    # will be closed
    from cafe.models.discord_guild import DiscordGuild

    client = httpx.Client()
    response = client.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers={
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}"
    })
    if response.status_code != 200:
        logger.error(f"Failed to get guild name for guild {guild_id} due to non-200 status code {response.status_code}")
        return
    
    data = response.json()
    name = data['name']
    DiscordGuild.objects.filter(id=guild_id).update(name=name)
    client.close()