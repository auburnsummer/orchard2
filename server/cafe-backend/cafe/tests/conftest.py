import json
from unittest.mock import patch
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.fernet import Fernet
from django.test import Client

@pytest.fixture
def debug():
    import debugpy
    debugpy.listen(("localhost", 5678))
    debugpy.wait_for_client()
    return debugpy.breakpoint

@pytest.fixture
def environment(autouse=True):
    import os
    os.environ.clear()
    os.environ["DJANGO_SECRET_KEY"] = "test_secret_key"
    os.environ["WEBHOOK_ENCRYPTION_KEY"] = Fernet.generate_key().decode()

@pytest.fixture
def client():
    from django.test import Client
    return Client()

@pytest.fixture
def bridge_client():
    """
    Fixture to provide a test client with the X-Requested-With header.
    This causes the django_bridge middleware to return JSON
    """
    from django.test import Client
    return Client(
        headers={
            "X-Requested-With": "DjangoBridge"
        }
    )

@pytest.fixture
def user_with_no_clubs():
    from cafe.models.user import User
    return User.objects.create_user(username=f"unoclubs")

@pytest.fixture
def user_with_buncha_clubs():
    from cafe.models.user import User
    from cafe.models.clubs.club import Club 
    from cafe.models.clubs.club_membership import ClubMembership
    user = User.objects.create_user(username=f"utwoclubs")
    user.save()
    c1 = Club(name="cluba", id="ca")
    c1.save()
    c2 = Club(name="clubb", id="cb")
    c2.save()
    cm1 = ClubMembership(
        user=user,
        club=c1,
        role="owner"
    )
    cm1.save()
    cm2 = ClubMembership(
        user=user,
        club=c2,
        role="admin"
    )
    cm2.save()
    return user

@pytest.fixture
def test_club():
    """Create a test club for general testing"""
    from cafe.models.clubs.club import Club
    return Club.objects.create(id="testclub", name="Test Club")

@pytest.fixture
def valid_invite(test_club):
    """Create a valid admin invite for a test club"""
    from cafe.models.clubs.club_invite import ClubInvite
    from django.utils import timezone
    from datetime import timedelta
    
    return ClubInvite.objects.create(
        club=test_club,
        role="admin",
        expiry=timezone.now() + timedelta(hours=24),
        code="valid_code"
    )

@pytest.fixture
def owner_invite(test_club):
    """Create a valid owner invite for a test club"""
    from cafe.models.clubs.club_invite import ClubInvite
    from django.utils import timezone
    from datetime import timedelta
    
    return ClubInvite.objects.create(
        club=test_club,
        role="owner",
        expiry=timezone.now() + timedelta(hours=24),
        code="owner_code"
    )

@pytest.fixture
def expired_invite(test_club):
    """Create an expired invite for a test club"""
    from cafe.models.clubs.club_invite import ClubInvite
    from django.utils import timezone
    from datetime import timedelta
    from freezegun import freeze_time
    
    with freeze_time("2023-01-01"):
        return ClubInvite.objects.create(
            club=test_club,
            role="admin",
            expiry=timezone.now() + timedelta(hours=1),
            code="expired_code"
        )

@pytest.fixture
def user_with_admin_membership(test_club):
    """Create a user who is an admin of the test club"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    user = User.objects.create_user(username="admin_user")
    ClubMembership.objects.create(
        user=user,
        club=test_club,
        role="admin"
    )
    return user


def follow_bridge_redirect(bridge_client, redirect_response):
    """Utility function to follow a Django-Bridge redirect and return the final response
    
    This allows testing of messages and other state after a redirect occurs.
    
    Args:
        bridge_client: The Django test client with bridge headers
        redirect_response: A response with action='redirect' from a bridge view
        
    Returns:
        The response from following the redirect
        
    Raises:
        ValueError: If the response is not a bridge redirect
    """
    if redirect_response.json().get('action') != 'redirect':
        raise ValueError("Response is not a bridge redirect")
    
    redirect_path = redirect_response.json()['path']
    return bridge_client.get(redirect_path)


@pytest.fixture
def client_with_discord_key():
    """Client with DISCORD_PUBLIC_KEY patched in the entry module."""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # Patch the verify_key directly in the entry module
    with patch('cafe.views.discord_bot.entry.verify_key', public_key):
        yield Client(), private_key

def create_discord_request(payload, private_key, timestamp="1234567890"):
    """Helper function to create a signed Discord request."""
    payload_bytes = json.dumps(payload).encode('utf-8')
    to_sign = timestamp.encode('ascii') + payload_bytes
    signature = private_key.sign(to_sign)
    
    return {
        'data': payload_bytes,
        'content_type': 'application/json',
        'HTTP_X_SIGNATURE_ED25519': signature.hex(),
        'HTTP_X_SIGNATURE_TIMESTAMP': timestamp,
    }

@pytest.fixture
def discord_guild_with_attached_club(test_club):
    from cafe.models.discord_guild import DiscordGuild
    return DiscordGuild.objects.create(
        id="123456789012345678",
        club=test_club
    )

@pytest.fixture
def rdlevel(test_club):
    """Create a test RDLevel for general testing"""
    from cafe.models.rdlevels.rdlevel import RDLevel
    from cafe.models.user import User
    from django.utils import timezone
    from unittest.mock import patch
    
    # Create a user to be the submitter
    submitter = User.objects.create_user(username="test_submitter", display_name="Test Submitter")
    
    # Mock the sync_level_to_typesense task to avoid Redis/Typesense issues in tests
    with patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense'):
        return RDLevel.objects.create(
            artist="Test Artist",
            artist_tokens=["test", "artist"],
            artist_raw="Test Artist",
            song="Test Song", 
            song_alt="Test Song Alt",
            song_raw="Test Song",
            seizure_warning=False,
            description="A test level for testing purposes",
            hue=180.0,
            authors=["Test Author"],
            authors_raw="Test Author",
            max_bpm=120,
            min_bpm=60,
            difficulty=1,
            single_player=True,
            two_player=False,
            last_updated=timezone.now(),
            tags=["test", "example"],
            sha1="test_sha1_hash_12345",
            rdlevel_sha1="test_rdlevel_sha1_hash_12345",
            rd_md5="test_md5_hash_12345",
            is_animated=False,
            rdzip_url="https://example.com/test.rdzip",
            image_url="https://example.com/test_image.jpg",
            thumb_url="https://example.com/test_thumb.jpg",
            icon_url="https://example.com/test_icon.jpg",
            submitter=submitter,
            club=test_club,
            approval=0
        )