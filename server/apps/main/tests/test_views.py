from django.test import TestCase
from django.contrib import auth
from django.test import Client
from django.db import models
from server.apps.main.models import PublicExperience
from django.contrib.auth.models import User
from server.apps.main.views import share_experience
import vcr
import urllib


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
        self.pe_a = PublicExperience(open_humans_member=self.oh_a, experience_id="1234", **pe_data)
        self.pe_b = PublicExperience(open_humans_member=self.oh_b, experience_id="8765", **pe_data)

    # For the tests for share_exp the plan is to go through the if statements sequentially
    # and put in tests for each eventuality - hence editing an experience may come before writing one
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

    # TODO - there is no contingency for form.is_valid() == False at the moment
    # Does there need to be?
    def test_share_exp_submitting_edited_experience(self):
        """
        Test that user can submit an edited a story of their own
        logic:
            request.user.is_authenticated == True
            request.method == "POST"
            form.is_valid() == True
            uuid == True
        """
        # Need to confirm that the call is made to open humans to delete the single file with the given uuid
        # Need to confirm upload of the (cleaned) data to that user's OH account
        # Need to confirm update of the PE database
        # Need to confirm redirection to confirm page
        pass
    
    @vcr.use_cassette('server/apps/main/tests/fixtures/share_experiences.yaml',
                      record_mode='none', filter_query_parameters=['access_token'])
    def test_share_exp_submit_new_experience(self):
        """
        Test that user can submit a new experience of their own
        logic:
            request.user.is_authenticated == True
            request.method == "POST"
            form.is_valid() == True
            uuid == False

        """
        # Need to confirm creation of a new UUID
        # Need to confirm upload of the (cleaned) data to that user's OH account
        # Need to confirm update of the PE database 
        # Need to confirm redirection to confirm page

        c = Client()
        c.force_login(self.user_a)
        
        response = c.post("/main/share_exp/",
                          {"experience_text": "Here is some experience text", 
                           "difference_text": "Here is some difference text",
                           "title_text": "Title text here",
                           "open_humans_member": self.oh_a},
                        follow=True)
        

    
        pass

    def test_share_exp_load_existing_experience_for_editing(self):
        """
        Test that the share experience form is populated with the appropriate fields
        from that user's specific PublicExperience.
        logic:
            request.user.is_authenticated == True
            request.method == "GET"
            uuid == True
        """
        # Need to confirm that the PublicExperience object exists
        # Need to confirm that the contents of the sharedExperienceForm metadata aligns with the contents of the PublicExperience object
        # Need to make a small change
        # Need to ensure that small change is present in the context sent to "main/share_experiences.html"
        pass

    def test_share_exp_load_blank_form(self):
        """
        Test that a blank share experience form is loaded.
        logic:
            request.user.is_authenticated == True
            request.method == "GET"
            uuid == False
        """
        # Need to confirm that the SharedExperienceForm is empty
        # Need to populate with minimal example
        # Need to ensure that small change is present in the context sent to "main/share_experiences.html"
        pass



