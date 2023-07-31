from django.test import TestCase
from django.conf import settings
from django.test import Client

from openhumans.models import OpenHumansMember

from server.apps.users.models import UserProfile
from server.apps.users.helpers import (
    user_profile_exists,
    user_submitted_profile,
)

class ModelTests(TestCase):
    """
    Tests the model functions.
    """

    def setUp(self):
        """
        Set-up for test with three users.
        """
        settings.DEBUG = True

        # Placeholder data
        data = {"access_token": "123456", "refresh_token": "bar", "expires_in": 36000}

        # Create user A
        self.oh_a = OpenHumansMember.create(oh_id=12345678, data=data)
        self.oh_a.save()
        self.user_a = self.oh_a.user
        self.user_a.openhumansmember = self.oh_a
        self.user_a.set_password("password_a")
        self.user_a.save()
        # Create user B
        self.oh_b = OpenHumansMember.create(oh_id=87654321, data=data)
        self.oh_b.save()
        self.user_b = self.oh_b.user
        self.user_b.openhumansmember = self.oh_b
        self.user_b.set_password("password_b")
        self.user_b.save()
        # Create user C
        self.oh_c = OpenHumansMember.create(oh_id=81726354, data=data)
        self.oh_c.save()
        self.user_c = self.oh_c.user
        self.user_c.openhumansmember = self.oh_c
        self.user_c.set_password("password_c")
        self.user_c.save()

        # Create a user profile
        up_a_data = {
           "profile_submitted": False,
           "autistic_identification": "unspecified",
           "age_bracket": "18-25",
           "age_public": False,
           "gender": "see_description",
           "gender_self_identification": "",
           "gender_public": False,
           "description": "Timelord",
           "description_public": False,
           "comms_review": False,
           "abuse": False,
           "violence": False,
           "drug": True,
           "mentalhealth": False,
           "negbody": True,
           "other": False,
        }
        self.up_a = UserProfile.objects.create(user=self.user_a, **up_a_data)
        self.up_b = UserProfile.objects.create(user=self.user_b)

    def test_model_str(self):
        """
        Test that the model returns an appropriate string when printed.
        """
        up_a = UserProfile.objects.get(user=self.user_a)
        assert up_a.__str__() == "Profile for 12345678_openhumans"

    def test_model_set(self):
        """
        Test that we can set the values in the model.
        """
        up_a = UserProfile.objects.get(user=self.user_a)
        assert up_a.description == "Timelord"
        assert up_a.age_bracket == "18-25"
        assert up_a.gender == "see_description"
        assert up_a.abuse == False
        assert up_a.violence == False
        assert up_a.drug == True
        assert up_a.mentalhealth == False
        assert up_a.negbody == True
        assert up_a.other == False

    def test_model_defaults(self):
        """
        Check that the default values are appropriate when an empty model is
        created.
        """
        up_b = UserProfile.objects.get(user=self.user_b)
        assert up_b.description == ""
        assert up_b.age_bracket == "unspecified"
        assert up_b.gender == "unspecified"
        assert up_b.abuse == False
        assert up_b.violence == False
        assert up_b.drug == False
        assert up_b.mentalhealth == False
        assert up_b.negbody == False
        assert up_b.other == False

    def test_profile_exists(self):
        """
        Check that the user_profile_exists helper function returns sensible
        values.
        """
        assert user_profile_exists(self.user_a)
        assert user_profile_exists(self.user_b)
        assert not user_profile_exists(self.user_c)

    def test_user_submitted_profile(self):
        """
        Check that the user_submitted_profile helper function returns sensible
        values.
        """
        assert not user_submitted_profile(self.user_a)
        assert not user_submitted_profile(self.user_b)
        assert not user_submitted_profile(self.user_c)

