from django.test import TestCase
from django.db import models
from server.apps.main.models import PublicExperience

from openhumans.models import OpenHumansMember


class Models(TestCase):
    """
    Tests the views function
    """

    def SetUp(self):
        """
        Set-up for test with two users
        """
        # One user 
        self.user_a = OpenHumansMember.create(oh_id=1234, access_token="abc", refresh_token="def", expires_in=1000)

        pe_data = {"experience_text": "a",
                   "difference_text": "b",
                   "title_text": "c"}
        PublicExperience.objects.create(open_humans_member = self.user_a, **pe_data)

    def test_model_str(self):
        story_a = PublicExperience.objects.get(title_text = "c")
        assert story_a .__str__() == "c"

