from django.test import TestCase
import json
from django.contrib.auth.models import Group
from server.apps.main.helpers import reformat_date_string, get_review_status, \
    is_moderator, make_tags, extract_experience_details, delete_single_file_and_pe, delete_PE, \
    public_experience_model_to_form, process_trigger_warnings, update_public_experience_db, \
    get_oh_metadata, get_oh_file, get_oh_combined, moderate_page, choose_moderation_redirect, \
    extract_triggers_to_show, get_message, message_wrap, number_by_review_status, get_carousel_stories, \
    pick_research_message, get_story_privacy_and_research_for_session

from openhumans.models import OpenHumansMember
from server.apps.main.models import PublicExperience, ExperienceHistory
from server.apps.main.forms import ModerateExperienceForm
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
        self.non_moderator_user = OpenHumansMember.create(oh_id="12345678",data=data)
        self.non_moderator_user.save()
        self.moderator_user = OpenHumansMember.create(oh_id="23456789",data=data)
        # create second group for moderator user to create edge-case
        self.other_group = Group.objects.create(name='SecondGroup')
        # add moderator to second group
        self.other_group.user_set.add(self.moderator_user.user)
        # create moderator group and add moderator user
        self.moderator_group = Group.objects.create(name='Moderators')
        self.moderator_group.user_set.add(self.moderator_user.user)
        self.moderator_user.save()

        approved = {
            "experience_text": "approved",
            "difference_text": "approved",
            "title_text": "approved",
            "moderation_status": "approved",
        }
        approved_with_trigger = {
            "experience_text": "trigger",
            "difference_text": "trigger",
            "title_text": "trigger",
            "moderation_status": "approved",
            "abuse": True,
        }
        rejected = {
            "experience_text": "rejected",
            "difference_text": "rejected",
            "title_text": "rejected",
            "moderation_status": "rejected",
        }
        self.pe_a = PublicExperience.objects.create(
            open_humans_member=self.non_moderator_user, experience_id="1234_1", **approved
        )
        self.pe_b = PublicExperience.objects.create(
            open_humans_member=self.non_moderator_user, experience_id="1234_2", **approved_with_trigger
        )
        self.pe_c = PublicExperience.objects.create(
            open_humans_member=self.non_moderator_user, experience_id="1234_3", **rejected
        )

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
    def test_fetch_by_uuid_successs(self):
        """
        Test that fetching an OH file by UUID works.
        Should succeed if no duplicate UUID in account
        """
        target_uuid = "ebad2890-bc43-11ed-95a4-0242ac130003"
        response = get_oh_metadata(self.moderator_user, target_uuid)
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
            get_oh_metadata(self.moderator_user, target_uuid)

    @vcr.use_cassette('server/apps/main/tests/fixtures/get_oh_file.yaml',
                      record_mode='none', filter_query_parameters=['access_token'])
    def test_fetch_oh_file(self):
        """
        Test that fetching an OH file.
        """
        target_url = "https://www.openhumans.org/data-management/datafile-download/63968911/?key=8859abff-0967-4a0d-8196-cbda2dc8224f"
        response = get_oh_file(target_url)
        self.assertIn("data", response)
        self.assertEqual(response["data"]["experience_text"],"Experience text")
        self.assertEqual(response["data"]["difference_text"],"Difference text")
        self.assertEqual(response["data"]["title_text"],"Title text")
        self.assertEqual(response["data"].get("description"),None)
        self.assertEqual(response["data"].get("research"),False)
        self.assertEqual(response["data"].get("viewable"),False)
        self.assertNotIn("tags", response)
        self.assertNotIn("metadata", response)

    @vcr.use_cassette('server/apps/main/tests/fixtures/get_oh_combined.yaml',
                      record_mode='none', filter_query_parameters=['access_token'])
    def test_fetch_oh_combined(self):
        """
        Test that fetching an OH file in combined form works.
        """
        target_uuid = "e2ba9bd8-d2ea-11ed-99e8-0242ac140003"
        response = get_oh_combined(self.moderator_user, target_uuid)
        # Content extracted from the file
        self.assertEqual(response["experience_text"],"Experience text")
        self.assertEqual(response["difference_text"],"Difference text")
        self.assertEqual(response["title_text"],"Title text")
        # Content extracted from the metadata
        self.assertEqual(response["research"],False)
        self.assertEqual(response["viewable"],False)
        self.assertEqual(response["moderation_status"],"not reviewed")
        self.assertEqual(response["drug"],False)
        self.assertEqual(response["abuse"],False)
        self.assertEqual(response["negbody"],False)
        self.assertEqual(response["violence"],False)
        self.assertEqual(response["mentalhealth"],False)
        self.assertEqual(response["other"],"Topic")
        # Content that shouldn't be present
        self.assertNotIn("descriptions", response)
        self.assertNotIn("tags", response)
        self.assertNotIn("metadata", response)
        self.assertNotIn("data", response)

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
                    'moderation_comments': '',
                    'viewable': False,
                    'research': False,
                    }
        returned_data = make_tags(tag_data)
        self.assertNotIn('abuse',returned_data)
        self.assertNotIn('negative body', returned_data)
        self.assertNotIn('mental health', returned_data)
        self.assertIn('not public',returned_data)
        self.assertIn('non-research',returned_data)
        self.assertEqual(len(returned_data), 2)

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


    def test_public_experience_model_to_form(self):
        """
        Test that turning a PE object into a moderation form works
        Also test that subsequent processing of trigger warnings works!
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
        self.form = public_experience_model_to_form(self.public_experience)
        # assert returned form is of right class
        self.assertIsInstance(self.form, ModerateExperienceForm)
        # test processing of trigger warnings
        # remove things which wouldn't be submitted in actual form:
        self.form.data.pop('experience_text')
        self.form.data.pop('difference_text')
        self.form.data.pop('title_text')
        self.form.data.pop('experience_id')
        self.form.data.pop('open_humans_member')
        self.form.data.pop('viewable')
        processed_triggers = process_trigger_warnings(self.form)
        trigger_keys = list(processed_triggers.keys())
        expected_keys = ['abuse','drug', 'mentalhealth', 'negbody', 'other', 'violence']
        for k in expected_keys:
            self.assertIn(k, trigger_keys)


    def test_update_public_experience(self):
        """
        Test update PE in DB function
        """
        # data dict for creating PE
        self.pe_data = {
            'experience_text': "foo",
            'difference_text': "bar",
            'title_text': 'title',
            'experience_id': 'foobar_id',
            'viewable': True
        }
        # record initial PE and PEH objects in the database
        initial_experiences = len(PublicExperience.objects.all())
        initial_histories = len(ExperienceHistory.objects.all())
        # create new PE
        update_public_experience_db(self.pe_data, "foobar_id" ,self.non_moderator_user,self.non_moderator_user)
        # check that PE exists
        self.assertEqual(len(PublicExperience.objects.all()),initial_experiences + 1)
        pe = PublicExperience.objects.get(experience_id='foobar_id')
        # check that moderation status is "in review"
        self.assertEqual(pe.moderation_status, 'not reviewed')
        # check that this and only this PEH object exists
        self.assertEqual(len(ExperienceHistory.objects.filter(experience=pe)),initial_histories + 1)
        # check that EH object marks creation
        peh = ExperienceHistory.objects.filter(experience=pe)[0]
        self.assertEqual(peh.change_type,"Make Public")
        # mark experience as moderation-approved
        pe.moderation_status = 'approved'
        pe.save()
        # make new edit, should reset moderation status
        self.pe_data['experience_id'] = 'foobar_id'
        self.pe_data['viewable'] = True
        update_public_experience_db(self.pe_data, "foobar_id" ,self.non_moderator_user,self.non_moderator_user)
        # check moderation did reset properly
        pe = PublicExperience.objects.get(experience_id='foobar_id')
        self.assertEqual(pe.moderation_status, 'not reviewed')
        # check that two history objects exists
        self.assertEqual(len(ExperienceHistory.objects.filter(experience=pe)),initial_histories + 2)
        # get newest PEH object, check it's "Edit"
        peh = ExperienceHistory.objects.all().order_by('changed_at')[1]
        self.assertEqual(peh.change_type,"Edit")
        # test moderatation edit
        self.pe_data['viewable'] = True
        self.pe_data['moderation_status'] = 'approved'
        update_public_experience_db(self.pe_data, "foobar_id", self.non_moderator_user, self.moderator_user,
                                    change_type='Moderate',change_comments='I left a comment')
        # check updated PE & latest PEH object
        pe = PublicExperience.objects.get(experience_id='foobar_id')
        self.assertEqual(pe.moderation_status, 'approved') # is now approved
        self.assertEqual(len(ExperienceHistory.objects.filter(experience=pe)),initial_histories + 3) # got 3 history entries now
        peh = ExperienceHistory.objects.all().order_by('changed_at')[2]
        # check details of PEH & PE
        self.assertEqual(pe.open_humans_member.oh_id,str(self.non_moderator_user.oh_id)) # exp owned by owner
        self.assertEqual(peh.changed_by.oh_id,self.moderator_user.oh_id) # exp last changed by moderator
        self.assertEqual(peh.change_type,'Moderate') # last operation was moderate
        # check everything gets deleted if user makes story non-public
        update_public_experience_db(self.pe_data, "foobar_id" ,self.non_moderator_user,self.non_moderator_user)
        self.assertEqual(len(PublicExperience.objects.all()),initial_experiences) # should be no additional public experience
        self.assertEqual(len(ExperienceHistory.objects.all()),initial_histories) # should be no additional history

    def test_moderation_redirect(self):
        result = choose_moderation_redirect("not moderated")
        self.assertEqual(result, "pending")

        result = choose_moderation_redirect("in review")
        self.assertEqual(result, "pending")

        result = choose_moderation_redirect("approved")
        self.assertEqual(result, "approved")

        result = choose_moderation_redirect("rejected")
        self.assertEqual(result, "rejected")

        result = choose_moderation_redirect("something else")
        self.assertEqual(result, "pending")

        result = choose_moderation_redirect(None)
        self.assertEqual(result, "pending")

    def test_extract_triggers_to_show(self):
        # Test the right trigger warnings are allowed
        allowed_triggers = {'abuse', 'violet', 'dasies', 'mentalhealth', 'nigella', 'orchids'}
        trigger_list = extract_triggers_to_show(allowed_triggers)
        assert('abuse' in trigger_list and 'mentalhealth' in trigger_list)
        assert('violence' not in trigger_list and 'drugs' not in trigger_list
               and 'negbody' not in trigger_list and 'other' not in trigger_list)

    def test_moderator_message_exists(self):
        """
        Tests that the message sent to users when the moderation status changes
        can be read in from file correctly.
        """
        # Read in the message
        subject, message = get_message("mod_message.txt")
        # Let's make some assumptions about a minimal length subject and message
        assert len(subject) > 4
        assert len(message) > 4
        # Let's assume a message that doesn't state where it's coming from isn't doing its job
        self.assertIn('AutSPACEs', message)

    def test_message_read_error(self):
        """
        Tests that if there's an IO error reading a message template, the
        subject and message will be returned as None.
        """
        # This will return a pair of Nones if it fails
        subject, message = get_message("")
        # Check that only Nones are returned
        assert not subject
        assert not message

    def test_message_wrap(self):
        """
        Test that the message wrapping code wraps to the given line length but leaves
        paragraph breaks (empty lines) alone.
        """
        text = "This is a very long long string. "
        length = len(text)
        text = text * 10
        # Ensure paragraph breaks are retained
        text = '\n\n'.join([text] * 3)
        text = message_wrap(text, length)
        assert text.count("\n") == 31
        for line in text.split("\n"):
            assert len(line) <= length

    def test_number_by_review_status(self):
        # make minimal working example of files
        files = []
        # one of each moderation status
        poss_mod_status = ["approved", "not reviewed", "rejected", "in review"]
        for p in poss_mod_status:
            files.append({'metadata': {'data': {'moderation_status': p, 'viewable': True}}})

        # add another rejected story
        files.append({'metadata': {'data': {'moderation_status': 'rejected', 'viewable': True}}})
        
        # two private stories
        for _ in range(2):
            files.append({'metadata':{'data':{'viewable': False, 'moderation_status': 'not reviewed'}}})

        status = number_by_review_status(files=files)

        self.assertEqual(status['private'], 2)
        self.assertEqual(status['approved'], 1)
        self.assertEqual(status['not_reviewed'], 1)
        self.assertEqual(status['rejected'], 2)
        self.assertEqual(status['in_review'], 1)
        self.assertEqual(status['moderated'],3)

        
    def test_carousel_stories_nofile(self):
        """
        Test that if the carousel fils is missing None is returned.
        """
        # File doesn't exist
        stories = get_carousel_stories(filename="tests/carousel-nonexistent.json")
        assert not stories

    def test_carousel_stories_appropriate_stories(self):
        """
        Test that appropriate stories can appear in the carousel.
        """
        # Request three stories, all appropriate
        stories = get_carousel_stories(filename="tests/carousel-test01.json")
        assert len(stories) == 3
        for story in stories:
            assert len(story["title_summary"]) <= 14
            assert len(story["experience_summary"]) <= 24
            assert len(story["title_summary"]) > 0
            assert len(story["experience_summary"]) > 0
            assert len(story["title"]) > 0
            assert len(story["experience"]) > 0
            assert len(story["difference"]) > 0
            assert len(story["image"]) > 0
            assert len(story["uuid"]) > 0

    def test_carousel_stories_inappropriate_stories(self):
        """
        Test that no inappropriate stories (rejected or with trigger warnings)
        will appear in the carousel.
        """
        # Request five stories but only two are inappropriate
        stories = get_carousel_stories(filename="tests/carousel-test02.json")
        assert len(stories) == 2
        for story in stories:
            assert len(story["title_summary"]) <= 14
            assert len(story["experience_summary"]) <= 24
            assert len(story["title_summary"]) > 0
            assert len(story["experience_summary"]) > 0
            assert len(story["title"]) > 0
            assert len(story["experience"]) > 0
            assert len(story["difference"]) > 0
            assert len(story["image"]) > 0
            assert len(story["uuid"]) > 0
            assert story["title"] != "rejected"
            assert story["title"] != "trigger"
            assert "placeholder" in story["uuid"]

    def test_carousel_stories_missing_details(self):
        """
        Test that if the caoursel file has poorly formed entries they are skipped
        but without impacting the well-formed entries.
        """
        # Request five stories but only one is well-formed
        stories = get_carousel_stories(filename="tests/carousel-test03.json")
        assert len(stories) == 1
        for story in stories:
            assert len(story["title_summary"]) <= 14
            assert len(story["experience_summary"]) <= 24
            assert len(story["title_summary"]) > 0
            assert len(story["experience_summary"]) > 0
            assert len(story["title"]) > 0
            assert len(story["experience"]) > 0
            assert len(story["difference"]) > 0
            assert len(story["image"]) > 0
            assert len(story["uuid"]) > 0
            assert story["title"] != "rejected"
            assert story["title"] != "trigger"
            assert "placeholder" in story["uuid"]

    def test_carousel_stories_too_many(self):
        """
        Test that if there are too many real stories available for the carousel
        the correct number is still returned. Also tests the exception case where
        the uuid is missing.
        """
        # Request five stories but only one is well-formed
        stories = get_carousel_stories(filename="tests/carousel-test04.json")
        assert len(stories) == 1
        for story in stories:
            assert len(story["title_summary"]) <= 14
            assert len(story["experience_summary"]) <= 24
            assert len(story["title_summary"]) > 0
            assert len(story["experience_summary"]) > 0
            assert len(story["title"]) > 0
            assert len(story["experience"]) > 0
            assert len(story["difference"]) > 0
            assert len(story["image"]) > 0
            assert len(story["uuid"]) > 0
            assert story["title"] != "rejected"
            assert story["title"] != "trigger"
            assert "placeholder" not in story["uuid"]

    def test_pick_research_message(self):
        """
        Test that pick_research_message returns correct messages
        """
        # check for non-1st-hand account
        message = pick_research_message("False",'irrelevant')
        self.assertIn("share the experience of an autistic individual with researchers",message)
        # check other responses
        options = ["", "yes", "no", "unspecified"]
        answers = []
        for o in options:
            message = pick_research_message("True", o)
            # assert doesn't give 'fallback' response
            self.assertNotIn("Thank you for sharing your story", message)
            answers.append(message)
        # assert all responses are different
        assert len(answers) == len(set(answers))
        # assert fallback works
        message = pick_research_message("True", 'failmepls')
        self.assertIn("Thank you for sharing your story", message)

    def test_get_story_privacy_and_research_for_session(self):
        """
        Test that privacy & research session settings work 
        """
        data = {'viewable': False, 'research': True}
        conf, pr, rr = get_story_privacy_and_research_for_session(data, 'blabla')
        self.assertEqual(pr, False)
        self.assertEqual(rr, True)

        data = {'viewable': False, 'research': False}
        conf, pr, rr = get_story_privacy_and_research_for_session(data, 'blabla')
        self.assertEqual(conf, "Your blabla experience was saved")
