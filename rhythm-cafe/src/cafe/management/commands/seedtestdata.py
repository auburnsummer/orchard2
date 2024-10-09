"""
"""

from django.core.management.base import BaseCommand, CommandError
from cafe.libs.gen_id import IDType, gen_id

from cafe.models import User, Club, ClubMembership


import random

import names

NUMBER_OF_TEST_USERS = 50
NUMBER_OF_TEST_CLUBS = 10

class Command(BaseCommand):
    help = "Creates test data"

    def handle(self, *args, **options):
        # superuser
        superuser = User.objects.create_superuser(
            username="u_admin",
            first_name="Marina Distort",
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

        # clubs
        for i in range(NUMBER_OF_TEST_CLUBS):
            club = Club(
                name=f"Club {i}"
            )
            club.save()
            # pick a random number of users to be owners and a random number to be admins.
            number_of_owners = random.choice([1, 1, 1, 2])
            number_of_admins = random.choice([2, 2, 2, 3, 3, 3, 4, 4, 5])
            users = random.sample(list(User.objects.all()), number_of_owners + number_of_admins)
            for j, user in enumerate(users):
                new_membership = ClubMembership(
                    user=user,
                    club=club,
                    role="owner" if j < number_of_owners else "admin"
                )
                new_membership.save()