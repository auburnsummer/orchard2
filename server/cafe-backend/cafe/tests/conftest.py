import pytest

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