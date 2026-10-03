from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from cafe.models import User, Club, ClubMembership
from cafe.models.id_utils import generate_club_id, generate_user_id

import random

import names

NUMBER_OF_TEST_USERS = 50
NUMBER_OF_TEST_CLUBS = 10

class Command(BaseCommand):
    help = "Creates test data"

    def handle(self, *args, **options):
        try:
            # superuser
            superuser = User.objects.create_superuser(
                id="uadmin",
                email=None,
                username="uadmin",
                display_name="Marina Distort",
                password="admin"
            )
            superuser.save()
        except IntegrityError:
            self.stdout.write(self.style.WARNING("Superuser 'uadmin' already exists."))
        
        # users. only create if there are none yet.
        # we check for <=1 because of the superuser we just created.
        if User.objects.count() <= 1:
            for _ in range(NUMBER_OF_TEST_USERS):
                user = User.objects.create_user(
                    username=generate_user_id(),
                    display_name=names.get_full_name(),
                    email=None
                )
            user.save()
        else:
            self.stdout.write(self.style.WARNING("Test users already exist. Skipping user creation."))

        # ditto with clubs.
        if Club.objects.count() == 0:
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
        else:
            self.stdout.write(self.style.WARNING("Test clubs already exist. Skipping club creation."))
        
        # special club for unowned levels
        try:
            unowned_club = Club(
                id="csteward",
                name="Steward"
            )
            unowned_club.save()
        except IntegrityError:
            self.stdout.write(self.style.WARNING("Steward club already exists."))

        # special user for unowned levels
        try:
            unowned_user = User(
                id="usteward",
                username="usteward",
                display_name="Steward",
                email=None
            )
            unowned_user.save()
        except IntegrityError:
            self.stdout.write(self.style.WARNING("Steward user already exists."))

        try:
            pharmacy_club = Club(
                id="cpharmacy",
                name="Peer Reviewers"
            )
            pharmacy_club.save()
        except IntegrityError:
            self.stdout.write(self.style.WARNING("The Peer Reviewers club already exists."))