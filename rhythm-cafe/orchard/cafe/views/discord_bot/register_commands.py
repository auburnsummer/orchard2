"this is normallly invoked from updatediscordslashcommands.py"

import httpx

from orchard.settings import DISCORD_CLIENT_ID

url = f"https://discord.com/api/v10/applications/{DISCORD_CLIENT_ID}/commands"

# url = f"https://discord.com/api/v10/applications/{DISCORD_CLIENT_ID}/guilds/1129267465046732810/commands"
COMMANDS = [
    {
        "name": "version",
        "type": 1,
        "description": "Show the version of the Rhythm Cafe bot"
    }
]

def register_commands(token):
    resp = httpx.put(url, headers={
        'Authorization': f"Bot {token}"
    }, json=COMMANDS)
    print(resp.json())
    resp.raise_for_status()