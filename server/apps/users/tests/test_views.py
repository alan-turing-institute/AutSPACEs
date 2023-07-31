from django.test import TestCase
from django.conf import settings
from django.test import Client

from openhumans.models import OpenHumansMember

from server.apps.users.models import UserProfile
from server.apps.users.helpers import (
    user_profile_exists,
    user_submitted_profile,
)

class ViewTests(TestCase):
    """
    Tests the view functions.
    """

    def setUp(self):
        """
        Set-up for test with three users.
        """
        settings.DEBUG = True

        # Placeholder data
        data = {"access_token": "123456", "refresh_token": "bar", "expires_in": 36000}

        # Create user A
        self.oh_a = OpenHumansMember.create(oh_id=12345679, data=data)
        self.oh_a.save()
        self.user_a = self.oh_a.user
        self.user_a.openhumansmember = self.oh_a
        self.user_a.set_password("password_a")
        self.user_a.save()
        # Create user B
        self.oh_b = OpenHumansMember.create(oh_id=87654323, data=data)
        self.oh_b.save()
        self.user_b = self.oh_b.user
        self.user_b.openhumansmember = self.oh_b
        self.user_b.set_password("password_b")
        self.user_b.save()
        # Create user C
        self.oh_c = OpenHumansMember.create(oh_id=81726355, data=data)
        self.oh_c.save()
        self.user_c = self.oh_c.user
        self.user_c.openhumansmember = self.oh_b
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
        # Create a user profile
        up_b_data = {
           "profile_submitted": False,
           "autistic_identification": "childhood",
           "age_bracket": "26-35",
           "age_public": False,
           "gender": "Female",
           "gender_self_identification": "abcdabcd",
           "gender_public": False,
           "description": "Companion",
           "description_public": False,
           "comms_review": True,
           "abuse": False,
           "violence": True,
           "drug": False,
           "mentalhealth": False,
           "negbody": False,
           "other": True,
        }
        self.up_b = UserProfile.objects.create(user=self.user_b, **up_b_data)

    def test_profile_auth(self):
        """
        Check that the user profile page can only be accessed when the user is
        logged in.
        """
        c = Client()
        unauthorised_response = c.get("/users/profile/")
        # Redirect when logged out
        assert unauthorised_response.status_code == 302
        c.force_login(self.user_a)
        response = c.get("/users/profile/")
        assert response.status_code == 200

    def test_profile_created(self):
        """
        Check that the user profile is created when the user logs in, that the
        user is redirected to the appropriate pages, and that the
        user_profile_exists function returns different values before and after
        the first time the user is logged in.
        """

        # First forced login without creating user profile
        assert not user_profile_exists(self.user_c)
        c = Client()
        c.force_login(self.user_c)
        response = c.get("/users/profile/")
        assert response.status_code == 200
        # GET request should not create profile
        assert not user_profile_exists(self.user_c)
        c.logout()

        # Second valid login redirects to profile page
        unauthorised_response = c.get("/users/profile/")
        assert not user_profile_exists(self.user_c)
        # Redirect when logged out
        assert unauthorised_response.status_code == 302
        # Profile not created when logged out
        assert not user_profile_exists(self.user_c)
        c.force_login(self.user_c)
        assert not user_profile_exists(self.user_c)
        response = c.get("/main/login/")
        # Redirects to profile page
        assert response.status_code == 302
        self.assertRedirects(response, "/users/greetings/", status_code=302, target_status_code=200, fetch_redirect_response=False)
        assert user_profile_exists(self.user_c)
        response = c.get("/users/greetings/")
        assert response.status_code == 200
        # Check the greeting is shown
        self.assertContains(response, "Welcome")
        # Profile created when logged in
        assert user_profile_exists(self.user_c)

        # Third valid login redirects elsewhere
        c.post("/main/logout/")
        logged_out_response = c.get("/main/share_exp/", follow=True)
        self.assertTemplateUsed(logged_out_response, "main/home.html")
        c.force_login(self.user_c)

        response = c.get("/main/login/")
        # Login redirects to the overview page
        assert response.status_code == 302
        self.assertRedirects(response, "/main/overview", status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_profile_submit(self):
        """
        Check that the user profile can be updated by POSTing to the user
        profile page, and that the "user profile submitted" flag is updated as
        a result.
        """
        # Fresh user profile has never been submitted
        assert not user_submitted_profile(self.user_a)
        c = Client()
        c.force_login(self.user_a)
        response = c.get("/users/profile/")
        assert response.status_code == 200
        # Still the case
        assert not user_submitted_profile(self.user_a)
        up_a = UserProfile.objects.get(user=self.user_a)
        assert up_a.description == "Timelord"
        assert up_a.comms_review == False
        # Submit an update
        response = c.post(
            "/users/profile/",
            {
                "autistic_identification": "yes",
                "description": "Described",
                "comms_review": True,
            },
            follow=True,
        )

        # Check the profile has been updated
        up_a = UserProfile.objects.get(user=self.user_a)
        assert up_a.description == "Described"
        assert up_a.comms_review == True
        # Check the flag for submitting the profile has been set
        assert user_submitted_profile(self.user_a)

    def test_profile_rendering(self):
        """
        Check that profile values are rendered on the profile page.
        """
        c = Client()
        c.force_login(self.user_b)
        response = c.get("/users/profile/")
        assert response.status_code == 200
        self.assertContains(response, "Companion")
        self.assertContains(response, "abcdabcd")
        self.assertContains(response, "26-35")

