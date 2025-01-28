"this is normallly invoked from updatediscordslashcommands.py"

import httpx

from orchard.settings import DISCORD_CLIENT_ID

url = f"https://discord.com/api/v10/applications/{DISCORD_CLIENT_ID}/commands"

# url = f"https://discord.com/api/v10/applications/{DISCORD_CLIENT_ID}/guilds/1129267465046732810/commands"
COMMANDS = [
    {
        "name": "version",
        "type": 1,
        "description": "Show the version of the Rhythm Cafe bot",
        "default_member_permissions": "0"
    },
    {
        "name": "connectgroup",
        "type": 1,
        "description": "Connect this Discord server to a group",
        "default_member_permissions": "0"
    },
    {
        "name": "viewgroup",
        "type": 1,
        "description": "View this server's connected group",
        "default_member_permissions": "0"
    },
    {
        "name": "Add to Rhythm Café",
        "type": 3,
        "default_member_permissions": "0"
    },
    {
        "name": "Add to Rhythm Café (delegated)",
        "type": 3,
        "default_member_permissions": "0"
    }
]

def register_commands(token):
    resp = httpx.put(url, headers={
        'Authorization': f"Bot {token}"
    }, json=COMMANDS)
    print(resp.json())
    resp.raise_for_status()