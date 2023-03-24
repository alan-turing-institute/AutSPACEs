from django.test import TestCase
import json
from django.contrib.auth.models import Group
from server.apps.main.helpers import reformat_date_string, get_review_status, \
    is_moderator, get_oh_file, make_tags, extract_experience_details, delete_single_file_and_pe, delete_PE
from openhumans.models import OpenHumansMember 
from server.apps.main.models import PublicExperience
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
        self.moderator_user.save()


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
        """
        Test make_tags function
        """
        # Create mock set of tags 
        # Mock tags include 3 true items from the list, 2 false items from the list
        tag_data = {'abuse': True, 'violence': True,
                    'drug': False, 'mentalhealth': False,'negbody': True,
                    'other': '',
                    'moderation_status': 'approved',
                    'moderation_comments': ''
                    }
        returned_data = make_tags(tag_data)
        self.assertIn('abuse',returned_data)
        self.assertIn('negative body', returned_data)
        self.assertNotIn('mental health', returned_data)
        #### COMMENT:
        ## MIGHT WANT TO CHANGE make_tags TO ONLY RETURN PRESENT TAGS, 
        ## CAN THEN TEST FOR LEN of LIST=3


    def test_extract_experience_details(self):
        """
        Test that extraction of fixed information works. 
        """
        # Expected keys that should be returned
        expected_keys = ['difference_text', 'experience_id', 'experience_text',
                        'open_humans_member','research', 'title_text', 'viewable']
        # create public experience
        self.public_experience = PublicExperience.objects.create(
            experience_text = 'EXP_TEXT', 
            difference_text = 'DIFF_TEXT', 
            title_text = 'TITLE',
            experience_id = 'TEST_ID',
            open_humans_member = self.moderator_user,
            abuse = True, 
            violence = True,
        )
        self.public_experience.save()
        # get experience results
        exp_details = extract_experience_details(self.public_experience)
        # check all keys are there
        returned_keys = list(exp_details.keys())
        returned_keys.sort()
        self.assertEqual(expected_keys, returned_keys)
        # check relevant data is returned correctly
        self.assertEqual(exp_details['experience_id'], "TEST_ID")
        self.assertEqual(exp_details['open_humans_member'], self.moderator_user.oh_id)


    @vcr.use_cassette('server/apps/main/tests/fixtures/delete.yaml',
                      record_mode='none', filter_query_parameters=['access_token'])    
    def test_delete_file_and_pe(self):
        """
        Test that deleting a public experience through 
        delete_single_file_and_pe deletes both oh OH & local
        """
        self.public_experience = PublicExperience.objects.create(
            experience_text = 'EXP_TEXT', 
            difference_text = 'DIFF_TEXT', 
            title_text = 'TITLE',
            experience_id = 'TEST_ID',
            open_humans_member = self.moderator_user,
            abuse = True, 
            violence = True,
        )
        self.public_experience.save()
        self.assertEqual(1,len(PublicExperience.objects.filter(experience_id='TEST_ID')))
        delete_single_file_and_pe("TEST_ID",self.moderator_user)
        self.assertEqual(0,len(PublicExperience.objects.filter(experience_id='TEST_ID')))

    def test_delete_pe(self):
        """
        Test that deleting a public experience locally works
        """
        self.public_experience = PublicExperience.objects.create(
            experience_text = 'EXP_TEXT', 
            difference_text = 'DIFF_TEXT', 
            title_text = 'TITLE',
            experience_id = 'TEST_ID',
            open_humans_member = self.moderator_user,
            abuse = True, 
            violence = True,
        )
        self.public_experience.save()
        # Assert PE exists        
        self.assertEqual(1,len(PublicExperience.objects.filter(experience_id='TEST_ID')))
        # Try deleting PE from third party, should not delete!
        delete_PE("TEST_ID",self.non_moderator_user)
        self.assertEqual(1,len(PublicExperience.objects.filter(experience_id='TEST_ID')))
        # Try deleting PE from third party, should not delete!
        delete_PE("TEST_ID",self.moderator_user)
        self.assertEqual(0,len(PublicExperience.objects.filter(experience_id='TEST_ID')))