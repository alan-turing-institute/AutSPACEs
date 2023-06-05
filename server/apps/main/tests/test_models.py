from django.test import TestCase
from django.conf import settings
from server.apps.main.models import PublicExperience

from openhumans.models import OpenHumansMember


class ModelsTest(TestCase):
    """
    Tests the views function
    """
    
    def setUp(self):
        """
        Set-up for test with two users
        """
        settings.DEBUG = True
        # One user 
        data = {"access_token": 'foo',
        "refresh_token": 'bar',
        "expires_in": 36000}
        self.placeholder_user = OpenHumansMember.create(oh_id=12345678,data=data)
        self.placeholder_user.save()
        pe_data = {"experience_text": "a",
                   "difference_text": "b",
                   "title_text": "c"}
        PublicExperience.objects.create(open_humans_member = self.placeholder_user, **pe_data)

    def test_model_str(self):
        story_a = PublicExperience.objects.get(title_text = "c")
        assert story_a.__str__() == "a"
    
    def test_model_defaults(self):
        story_a = PublicExperience.objects.get(title_text = "c")
        assert story_a.abuse == False
        assert story_a.drug == False
        assert story_a.mentalhealth == False
        assert story_a.negbody == False
        assert story_a.violence == False
        assert story_a.research == False
        assert story_a.other == ""
        assert story_a.moderation_status == "not reviewed"

