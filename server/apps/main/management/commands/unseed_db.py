from django.core.management.base import BaseCommand
from server.apps.main.models import PublicExperience
from server.apps.users.models import UserProfile
from django.contrib.auth.models import User
from server.apps.users.helpers import delete_user

class Command(BaseCommand):
    help = "Restore DB and OH account to initial settings"

    def handle(self, *args, **options):

        # Delete user added stories from OH and DB and delete the user
        for u in User.objects.all():
            if u.username == "999999999_openhumans":
                u.delete()
            else:
                delete_user(user=u, delete_oh_data=True)



