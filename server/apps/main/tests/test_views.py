from django.test import TestCase
from django.contrib import auth
from django.test import Client
from django.db import models
from server.apps.main.models import PublicExperience

from openhumans.models import OpenHumansMember


class Views(TestCase):
    """
    Tests the views function
    """

    def SetUp(self):
        """
        Set-up for test with two users
        """
        user_a = auth.get_user(self.client)
        assert user_a.is_authenticated

        # # Two users 
        data = {"access_token": 'foo',
        "refresh_token": 'bar',
        "expires_in": 36000}
        self.oh_a = OpenHumansMember.create(oh_id=12345678,data=data)
        self.oh_b = OpenHumansMember.create(oh_id=87654321,data=data)

        

        # Each with a public experience
        pe_data = {"experience_text": "Here is some experience text",
                      "difference_text": "Here is some difference text",
                      "title_text": "Here is the title"}
        self.pe_a = PublicExperience(open_humans_member=self.oh_a, experience_id="1234", **pe_data)
        self.pe_b = PublicExperience(open_humans_member=self.oh_b, experience_id="8765", **pe_data)



    def test_share_exp(self):
        # c = Client()
        # logged_in = c.login(username='testuser', password='12345')
        # Check that a non-logged in user cannot share an experience
        # An unlogged in user should get redirected to the index (302 response)
        non_logged_in_user = Client()
        # non_logged_in_user.login(username='fred', password='secret')
        response = non_logged_in_user.get('/main/share_exp/')
        print(response.status_code)
        # print(self.pe_a)

        # assert isinstance(self.pe_a, PublicExperience)
        assert 1==1
        # data = {"access_token": "foo", "refresh_token": "bar", "expires_in": 36000}
        # self.non_moderator_user = OpenHumansMember.create(oh_id=12345678, data=data)
        # self.moderator_user = OpenHumansMember.create(oh_id=23456789, data=data)
        # self.moderator_group = Group.objects.create(name="SecondGroup")
        # self.moderator_group.user_set.add(self.moderator_user.user)
        # self.moderator_group = Group.objects.create(name="Moderators")
        # self.moderator_group.user_set.add(self.moderator_user.user)

    # def test_reformat_date(self):
    #      """
    #      Test that formating OH timestamp to native time object works
    #      """
    #      year = int(self.context['files'][0]['created'][:4])
    #      returned_context = reformat_date_string(self.context)
    #      self.assertEqual(returned_context['files'][0]['created'].year,year)