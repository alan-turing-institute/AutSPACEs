from django.test import TestCase
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import Group
from server.apps.main.models import PublicExperience
from server.apps.main.helpers import (
    reformat_date_string,
    get_review_status,
    is_moderator,
)
from openhumans.models import OpenHumansMember


class Views(TestCase):
    """
    Tests the views function
    """

    def SetUp(self):
        """
        Set-up for test with two users
        """
        # Two users 
        self.user_a = OpenHumansMember.create(oh_id=1234, access_token="abc", refresh_token="def", expires_in=1000)
        self.user_b = OpenHumansMember.create(oh_id=9876, access_token="xyz", refresh_token="xyz", expires_in=1000)

        # Each with a public experience
        pe_example = {"experience_text": "Here is some experience text",
                      "difference_text": "Here is some difference text",
                      "title_text": "Here is the title",
                      "experience_id": "123_abc",
                      "created_at": models.DateTimeField(auto_now=True)}
        self.pe_a = PublicExperience(open_humans_member=self.user_a, **pe_example)

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