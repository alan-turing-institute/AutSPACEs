from django.test import TestCase, RequestFactory, Client
from django.conf import settings
from open_humans.models import OpenHumansMember
from server.apps.main.models import PublicExperience



class ViewTest(TestCase):
    def setUp(self):
        settings.DEBUG = True
        settings.OPENHUMANS_CLIENT_ID = "A_CLIENT_ID"
        settings.OPENHUMANS_CLIENT_SECRET = "A_CLIENT_SECRET"
        settings.OPENHUMANS_APP_BASE_URL = "http://localhost:8000/openhumans/complete"
        self.factory = RequestFactory()
        self.oh_member = OpenHumansMember.create(
                            oh_id=1234,
                            oh_username='User_A',
                            access_token='foobar',
                            refresh_token='bar',
                            expires_in=36000)
        self.oh_member.save()