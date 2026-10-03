ALLOWED_WEBHOOK_DOMAINS = [
    "discord.com",
    "discordapp.com",
    "canary.discord.com",
    "ptb.discord.com",
    "webhook.site"
]


def is_allowed_webhook_url(url: str) -> bool:
    return any(url.startswith(f"https://{domain}/") for domain in ALLOWED_WEBHOOK_DOMAINS)
