from django.test import TestCase
from django.contrib import auth
from django.test import Client
from django.db import models
from server.apps.main.models import PublicExperience
from django.contrib.auth.models import User
import vcr
import urllib
from server.apps.main.forms import ShareExperienceForm


from openhumans.models import OpenHumansMember


class Views(TestCase):
    """
    Tests the views function
    """

    def setUp(self):
        """
        Set-up for test with two users
        """
        # Placeholder data
        data = {"access_token": '123456',
        "refresh_token": 'bar',
        "expires_in": 36000}

        # Create user A
        self.oh_a = OpenHumansMember.create(oh_id=12345678,data=data)
        self.oh_a.save()
        self.user_a = self.oh_a.user
        self.user_a.openhumansmember = self.oh_a
        self.user_a.set_password('password_a')
        self.user_a.save()
        # Create user B
        self.oh_b = OpenHumansMember.create(oh_id=87654321,data=data)
        self.oh_b.save()
        self.user_b = self.oh_a.user
        self.user_b.openhumansmember = self.oh_a
        self.user_b.set_password('password_a')
        self.user_b.save()

        # Each with a public experience
        pe_data = {"experience_text": "Here is some experience text",
                      "difference_text": "Here is some difference text",
                      "title_text": "Here is the title"}
        self.pe_a = PublicExperience.objects.create(open_humans_member=self.oh_a, experience_id="1234_1", **pe_data)
        self.pe_a = PublicExperience.objects.create(open_humans_member=self.oh_a, experience_id="1234_2", **pe_data)
        self.pe_b = PublicExperience.objects.create(open_humans_member=self.oh_b, experience_id="8765_1", **pe_data)

    def test_confirm_page(self):
        c = Client()
        c.force_login(self.user_a)
        response = c.get("/main/confirm_page/")
        assert response.status_code == 200

    def test_logout_user(self):
        """
        Test that a user can log themselves out
        """
        c = Client()
        c.force_login(self.user_a)
        logged_in_response = c.get('/main/share_exp/')
        assert logged_in_response.status_code == 200
        logged_out_response = c.post("/main/logout/")
        assert logged_out_response.status_code == 302

    @vcr.use_cassette('server/apps/main/tests/fixtures/view_exp.yaml',
                      record_mode='none',
                      filter_query_parameters=['access_token'],
                      match_on=['path'])
    def test_view_exp_logged_in(self):
        """
        Test that a user can view their experience when logged in and gets redirected to overview when not
        """
        c = Client()
        unauthorised_response = c.get('/main/view/33b30e22-f950-11ed-8488-0242ac140003/')
        assert unauthorised_response.status_code == 302
        c.force_login(self.user_a)
        response = c.get('/main/view/33b30e22-f950-11ed-8488-0242ac140003/', follow=True)
        self.assertContains(response,
                            "This is a simple short story for testing",
                            status_code=200)

    def test_share_exp(self):
        """
        Check that non-authorised users are redirected (to index, then home) - get
        logic:
            request.user.is_authenticated == False
        """
        c = Client()
        response = c.get('/main/share_exp/')
        assert response.status_code == 302
        
    def test_share_exp_logged_in(self):
        """
        Test that logged in members are taken to the correct page
        logic:
            request.user.is_authenticated == True
        """
        c = Client()
        c.force_login(self.user_a)
        response = c.get('/main/share_exp/')
        assert response.status_code == 200

    @vcr.use_cassette('server/apps/main/tests/fixtures/share_experience.yaml',
                      record_mode='none', filter_query_parameters=['access_token'], match_on=['path'])
    def test_share_exp_submit_new_experience(self):
        """
        Test that user can submit a new experience of their own
        logic:
            request.user.is_authenticated == True
            request.method == "POST"
            form.is_valid() == True
            uuid == False

        """
        # Cannot confirm creation of a new UUID
        # Need to confirm upload of the (cleaned) data to that user's OH account [X]
        # Need to confirm update of the PE database [X]
        # Need to confirm redirection to confirm page

        c = Client()
        c.force_login(self.user_a)

        user_a_stories_before = len(PublicExperience.objects.filter(open_humans_member=self.oh_a))

        response = c.post("/main/share_exp/",
                          {"experience_text": "Here is some experience text", 
                           "difference_text": "Here is some difference text",
                           "title_text": "A new story added",
                           "viewable": "True",
                           "open_humans_member": self.oh_a},
                        follow=True)
        
        user_a_stories_after = len(PublicExperience.objects.filter(open_humans_member=self.oh_a))
        
        pe_db_after = PublicExperience.objects.filter(title_text = "A new story added")

        # Check that a story with the title now exists in the database
        assert len(pe_db_after)==1

        # Check that there is one new story for user A
        assert user_a_stories_after == user_a_stories_before + 1

        # Check that there is a redirect after
        assert response.status_code == 200

        
    @vcr.use_cassette('server/apps/main/tests/fixtures/load_to_edit.yaml',
                      record_mode='none',
                      filter_query_parameters=['access_token'],
                      match_on=['path'])
    def test_share_exp_load_to_edit(self):
        """
        Test that the share experience form is populated with the appropriate fields
        from that user's specific PublicExperience.
        logic:
            request.user.is_authenticated == True
            request.method == "GET"
            uuid == True
        """

        c = Client()
        c.force_login(self.user_a)
        response = c.get("/main/edit/33b30e22-f950-11ed-8488-0242ac140003/",
                        follow=True)
        print(response.status_code)
        self.assertContains(response,
                            "This is a simple short story for testing",
                            status_code=200)
        self.assertNotContains(response,
                               "It is certainly an unpleasant thing,")
        



