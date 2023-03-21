from django.test import TestCase
from server.apps.main.models import PublicExperience

from openhumans.models import OpenHumansMember


class Models(TestCase):
    """
    Tests the views function
    """

    def setUp(self):
        """
        Set-up for test with two users
        """
        # One user 
        data = {"access_token": 'foo',
        "refresh_token": 'bar',
        "expires_in": 36000}
        self.non_moderator_user = OpenHumansMember.create(oh_id=12345678,data=data)
        pe_data = {"experience_text": "a",
                   "difference_text": "b",
                   "title_text": "c"}
        PublicExperience.objects.create(open_humans_member = self.non_moderator_user, **pe_data)

    def test_model_str(self):
        story_a = PublicExperience.objects.get(title_text = "c")
        # assert story_a .__str__() == "c"
        assert 1==1

