"""
"""

from django.core.management.base import BaseCommand, CommandError
from cafe.libs.gen_id import IDType, gen_id

from cafe.models import User

import names

NUMBER_OF_TEST_USERS = 50

class Command(BaseCommand):
    help = "Creates test data"

    def handle(self, *args, **options):
        # superuser
        superuser = User.objects.create_superuser(
            username="u_admin",
            first_name="Admin Admin",
            email="admin@rhythm.cafe",
            password="aaadmin12345!"
        )
        superuser.save()

        # users
        for _ in range(NUMBER_OF_TEST_USERS):
            username = gen_id(IDType.USER)
            user = User.objects.create_user(
                username=username,
                first_name=names.get_full_name(),
                email=f"{username}@cafe.email.invalid"
            )
            user.save()