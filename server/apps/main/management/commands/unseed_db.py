from django.core.management.base import BaseCommand
from server.apps.main.models import PublicExperience
from server.apps.users.models import UserProfile
from django.contrib.auth.models import User
from server.apps.users.helpers import delete_user

class Command(BaseCommand):
    help = "Restore DB and OH account to initial settings"

    def handle(self, *args, **options):

        # Delete user added stories from OH and DB and delete the user
        for up in UserProfile.objects.all():
            delete_user(user=up.user, delete_oh_data=True)

        # Delete the seeded stories from the DB
        for p in PublicExperience.objects.all():
            p.delete()

        # Delete seeded user
        for u in User.objects.all():
            if u.username == "999999999_openhumans":
                u.delete()



