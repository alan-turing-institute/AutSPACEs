from django.test import TestCase
import json
from django.contrib.auth.models import Group
from server.apps.main.helpers import reformat_date_string, get_review_status, is_moderator
from openhumans.models import OpenHumansMember

class StoryHelper(TestCase):
    """
    Tests for the story page helpers
    """

    def setUp(self):
        '''
        Set-up for test with basic variables etc.
        '''
        # Load context data from JSON rather than VCR, as should be independent
        # of using external fixtures. Basic JSON contains 4 experiences for testing
        with open("server/apps/main/tests/fixtures/helper-context.json") as f:
            self.context = json.load(f)
        data = {"access_token": 'foo',
        "refresh_token": 'bar',
        "expires_in": 36000}
        self.non_moderator_user = OpenHumansMember.create(oh_id=12345678,data=data)
        self.moderator_user = OpenHumansMember.create(oh_id=23456789,data=data)
        # create second group for moderator user to create edge-case
        self.other_group = Group.objects.create(name='SecondGroup')
        # add moderator to second group
        self.other_group.user_set.add(self.moderator_user.user)
        # create moderator group and add moderator user
        self.moderator_group = Group.objects.create(name='Moderators')
        self.moderator_group.user_set.add(self.moderator_user.user)


    def test_reformat_date(self):
        """
        Test that formating OH timestamp to native time object works
        """
        year = int(self.context['files'][0]['created'][:4])
        returned_context = reformat_date_string(self.context)
        self.assertEqual(returned_context['files'][0]['created'].year,year)

    def test_get_review_status(self):
        """
        Test that correctly enumerates different status options
        """
        statuses = get_review_status(self.context['files'])
        self.assertEqual(statuses["n_not_reviewed"],4)
        self.assertEqual(statuses["n_viewable"],4)
        self.assertEqual(statuses["n_moderated"],0)

    def test_moderator_check(self):
        """
        Test that only users in moderator-group return True. 
        Also ensure that it works for users in >1 group
        """
        self.assertFalse(is_moderator(self.non_moderator_user.user)) # non-moderator should be false
        self.assertTrue(is_moderator(self.moderator_user.user)) # moderator user should be true