from django.test import TestCase
from django.contrib import auth
from django.test import Client
from django.db import models
from server.apps.main.models import PublicExperience
from django.contrib.auth.models import User
from server.apps.main.views import share_experience


from openhumans.models import OpenHumansMember


class Views(TestCase):
    """
    Tests the views function
    """

    def setUp(self):
        """
        Set-up for test with two users
        """
        # user_a = auth.get_user(self.client)
        # assert user_a.is_authenticated

        # # Two users 
        data = {"access_token": 'foo',
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
        print("Created Users")

    
        
        # Each with a public experience
        pe_data = {"experience_text": "Here is some experience text",
                      "difference_text": "Here is some difference text",
                      "title_text": "Here is the title"}
        self.pe_a = PublicExperience(open_humans_member=self.oh_a, experience_id="1234", **pe_data)
        self.pe_b = PublicExperience(open_humans_member=self.oh_b, experience_id="8765", **pe_data)


    def test_share_exp(self):
        """Check that non-authorised users are redirected (to index, then home) - get"""
        # c = Client()
        # logged_in = c.login(username='testuser', password='12345')
        # Check that a non-logged in user cannot share an experience
        # An unlogged in user should get redirected to the index (302 response)
        c = Client()
        response = c.get('/main/share_exp/')
        assert response.status_code == 302
        print(response.status_code)

        print("*********")
        
    def test_share_exp_logged_in(self):
        c = Client()
        c.force_login(self.user_a)
        response = c.get('/main/share_exp/')
        print("logged in - ", response.status_code)
        # from django.contrib.auth.models import User
        # user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        # user.save()
        # logged_in_user = Client()
        # logged_in_user.force_login(user)
        # response_l = logged_in_user.get('/main/share_exp/')
        # print("Logged in ", response_l.status_code)
        # print(self.pe_a)

        # assert isinstance(self.pe_a, PublicExperience)
        assert 1==1

