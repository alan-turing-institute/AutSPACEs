from django.test import TestCase, Client, RequestFactory
from openhumans.models import OpenHumansMember
from django.contrib.auth.models import Group

from server.apps.main.views import moderate_public_experiences
import vcr
import json


class ModerationViewTests(TestCase):
    """
    Test that the moderation views work as expected
    """

    def setUp(self):
        '''
        shared user setup for all moderation tests. 
        requires at least 2 users (moderator, regular user)
        '''
        # shared token data for all test users
        data = {"access_token": 'foo',
        "refresh_token": 'bar',
        "expires_in": 36000}
        # create non-moderator OH object
        self.non_moderator_ohmember = OpenHumansMember.create(oh_id="12345678",data=data)
        self.non_moderator_ohmember.save()
        # set password for login with Client()
        self.non_moderator_user = self.non_moderator_ohmember.user
        self.non_moderator_user.openhumansmember = self.non_moderator_ohmember
        self.non_moderator_user.set_password('testpassword')
        self.non_moderator_user.save()
        # create moderator OH object
        self.moderator_oh_user = OpenHumansMember.create(oh_id="23456789",data=data)
        self.moderator_oh_user.save()
        # set password for login with Client()
        self.moderator_user = self.moderator_oh_user.user
        self.moderator_user.set_password('testpassword')
        # create moderator group
        self.moderator_group = Group.objects.create(name='Moderators')
        self.moderator_group.user_set.add(self.moderator_user)
        self.moderator_user.save()

    def test_view_moderate_list_logged_out(self):
        """
        Test moderate overview page is not accessible by logged-out users
        """
        c = Client()
        response = c.get("/main/moderate_public_experiences", follow=True)
        self.assertRedirects(response, "/", 
                             status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_view_moderate_list_non_moderator(self):
        """
        Test moderate overview page is not accessible by non-moderator users
        """
        c = Client()
        c.force_login(self.non_moderator_user)
        response = c.get("/main/moderate_public_experiences", follow=True)
        self.assertRedirects(response, "/main/overview", 
                             status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_view_moderate_list_moderator(self):
        """
        Test moderate overview page is accessible by moderators
        """
        c = Client()
        c.force_login(self.moderator_user)
        response = c.get("/main/moderate_public_experiences", follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderate_public_experiences.html')