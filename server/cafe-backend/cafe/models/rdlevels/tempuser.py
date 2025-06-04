from cafe.models import User
from allauth.socialaccount.models import SocialAccount

from cafe.models.id_utils import generate_user_id

def get_or_create_discord_user(discord_user_id: str, discord_username: str) -> User:
    sa = SocialAccount.objects.filter(uid=discord_user_id, provider='discord').first()
    if sa:
        return sa.user

    user_id = generate_user_id()
    new_user = User.objects.create_user(
        username=user_id,
        display_name=discord_username,
        email=f"{user_id}@cafe.invalid"
    )
    new_user.save()
    social_account = SocialAccount.objects.create(
        user=new_user,
        provider="discord",
        uid=discord_user_id
    )
    social_account.save()
    return new_user