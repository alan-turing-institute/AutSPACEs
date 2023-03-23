from django.test import TestCase
import json
from django.contrib.auth.models import Group
from server.apps.main.helpers import reformat_date_string, get_review_status, is_moderator, get_oh_file, make_tags
from openhumans.models import OpenHumansMember
import vcr

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

    @vcr.use_cassette('server/apps/main/tests/fixtures/my_stories.yaml',
                      record_mode='none', filter_query_parameters=['access_token'])
    def test_fetch_by_uuid_sucesss(self):
        """
        Test that fetching an OH file by UUID works. 
        Should succeed if no duplicate UUID in account
        """
        target_uuid = "ebad2890-bc43-11ed-95a4-0242ac130003"
        response = get_oh_file(self.moderator_user, target_uuid)
        self.assertEqual(response['id'], 63199447)


    @vcr.use_cassette('server/apps/main/tests/fixtures/my_stories_duplicate_uuid.yaml',
                      record_mode='none', filter_query_parameters=['access_token'])
    def test_fetch_by_uuid_failure(self):
        """
        Test that fetching an OH file by UUID works. 
        Should faile due to duplicate UUID in account
        """
        target_uuid = "ebad2890-bc43-11ed-95a4-0242ac130003"
        with self.assertRaises(Exception): 
            get_oh_file(self.moderator_user, target_uuid)


    def test_make_tags(self):

        # Create mock set of tags 
        # Mock tags include 3 true items from the list, 2 false items from the list
        tag_data = {'abuse': True, 'violence': True,
                    'drug': False, 'mentalhealth': False,'negbody': True,
                    'other': '',
                    'moderation_status': 'approved',
                    'moderation_comments': ''
                    }
        returned_data = make_tags(tag_data)
        print(returned_data)
        self.assertIn('abuse',returned_data)
        self.assertIn('negative body', returned_data)
        self.assertNotIn('mental health', returned_data)
