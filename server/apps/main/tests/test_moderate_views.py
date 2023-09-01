from unittest import mock
from django.test import TestCase, Client, RequestFactory
from openhumans.models import OpenHumansMember
from server.apps.main.models import PublicExperience, ExperienceHistory
from django.contrib.auth.models import Group

from server.apps.main.views import moderate_public_experiences
from server.apps.users.models import UserProfile
import vcr
import json


class ModerationViewTests(TestCase):
    """
    Test that all moderation views work as expected
    Also account for cases that should fail, e.g.
    non-logged in users
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
        self.moderator_user.set_password('testpassword1')
        # create moderator OH object with user profile
        self.moderator_oh_user_with_profile = OpenHumansMember.create(oh_id="34567891",data=data)
        self.moderator_oh_user_with_profile.save()
        # set password for login with Client()
        self.moderator_user_with_profile = self.moderator_oh_user_with_profile.user
        self.moderator_user_with_profile.set_password('testpassword2')
        # create moderator group
        self.moderator_group = Group.objects.create(name='Moderators')
        self.moderator_group.user_set.add(self.moderator_user)
        self.moderator_user.save()
        self.moderator_group.user_set.add(self.moderator_user_with_profile)
        self.moderator_user_with_profile.save()
        # create public expierence that needs review
        pe_data = {
            'experience_text': "test",
            'title_text': "title",
            'open_humans_member': self.non_moderator_ohmember,
            'experience_id': 'test-test-test',
            "first_hand_authorship": "True",
        }
        self.pe_a = PublicExperience.objects.create(**pe_data)

        moderation_history = {
            "changed_by": self.moderator_oh_user,
            "change_comments": "Local moderation comment",
            "change_reply": "Moderation comment",
        }
        self.eh_a = ExperienceHistory.objects.create(
            experience = self.pe_a,
            **moderation_history
        )
        # User profile for user moderator_user_with_profile
        user_profile = {
           "profile_submitted": False,
           "autistic_identification": "unspecified",
           "age_bracket": "18-25",
           "age_public": False,
           "gender": "see_description",
           "gender_self_identification": "",
           "gender_public": False,
           "description": "Timelord",
           "description_public": False,
           "comms_review": False,
           "abuse": False,
           "violence": False,
           "drug": False,
           "mentalhealth": False,
           "negbody": False,
           "other": False,
        }
        self.moderator_profile = UserProfile.objects.create(user=self.moderator_user_with_profile, **user_profile)

    # test moderation pages as logged-out user

    def test_view_moderate_list_logged_out(self):
        """
        Test moderate overview page is not accessible by logged-out users
        """
        c = Client()
        response = c.get("/main/moderate_public_experiences", follow=True)
        self.assertRedirects(response, "/",
                             status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_single_moderation_view_as_guest_get(self):
        """
        Test moderate single experience page isn't accessible to logged-out users
        """
        c = Client()
        response = c.get("/main/moderate/test-test-test/", follow=True)
        self.assertRedirects(response, "/",
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_single_moderation_view_as_guest_post(self):
        """
        Test moderating single experience page fails when done by non-autenticated user
        """

        c = Client()
        response = c.post("/main/moderate/test-test-test/",
                        {"mentalhealth": True, "other":"New trigger",
                        "moderation_status":"approved",
                        "moderation_comments":"amazing story!",
                        },
                        follow=True)
        # assert ending up on right page
        self.assertRedirects(response, "/",
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')
        # test that no changes were made
        pe = PublicExperience.objects.get(experience_id='test-test-test')
        self.assertEqual(pe.mentalhealth,False)
        self.assertEqual(pe.other,"")
        self.assertEqual(pe.moderation_status,"not reviewed")

    # test moderation pages as logged-in but non-moderator user

    def test_view_moderate_list_non_moderator(self):
        """
        Test moderate overview page is not accessible by non-moderator users
        """
        c = Client()
        c.force_login(self.non_moderator_user)
        response = c.get("/main/moderate_public_experiences", follow=True)
        self.assertRedirects(response, "/",
                             status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_view_moderate_list_pending_non_moderator(self):
        """
        Test moderate pending overview page is not accessible by non-moderator users
        """
        c = Client()
        c.force_login(self.non_moderator_user)
        response = c.get("/main/moderation_list", {"status": "pending"}, follow=True)
        self.assertRedirects(response, "/",
                             status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_view_moderate_list_approved_non_moderator(self):
        """
        Test moderate approved overview page is not accessible by non-moderator users
        """
        c = Client()
        c.force_login(self.non_moderator_user)
        response = c.get("/main/moderation_list", {"status": "approved"}, follow=True)
        self.assertRedirects(response, "/",
                             status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_view_moderate_list_rejected_non_moderator(self):
        """
        Test moderate rejected overview page is not accessible by non-moderator users
        """
        c = Client()
        c.force_login(self.non_moderator_user)
        response = c.get("/main/moderation_list", {"status": "rejected"}, follow=True)
        self.assertRedirects(response, "/",
                             status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_single_moderation_view_as_non_moderator_get(self):
        """
        Test moderate single experience page isn't accessible by non-moderators
        """
        c = Client()
        c.force_login(self.non_moderator_user)
        response = c.get("/main/moderate/test-test-test/", follow=True)
        self.assertRedirects(response, "/",
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_single_moderation_view_as_non_moderator_post_pending(self):
        """
        Test moderating single experience page fails when done by non-moderator
        """

        c = Client()
        c.force_login(self.non_moderator_user)

        response = c.post("/main/moderate/test-test-test/",
                        {"mentalhealth": True, "other":"New trigger",
                        "moderation_status":"not moderated",
                        "moderation_comments":"amazing story!",
                        },
                        follow=True)
        # assert ending up on right page
        self.assertRedirects(response, "/",
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')
        # test that no changes were made
        pe = PublicExperience.objects.get(experience_id='test-test-test')
        self.assertEqual(pe.mentalhealth,False)
        self.assertEqual(pe.other,"")
        self.assertEqual(pe.moderation_status,"not reviewed")

    def test_single_moderation_view_as_non_moderator_post_approved(self):
        """
        Test moderating single experience page fails when done by non-moderator
        """

        c = Client()
        c.force_login(self.non_moderator_user)

        response = c.post("/main/moderate/test-test-test/",
                        {"mentalhealth": True, "other":"New trigger",
                        "moderation_status":"approved",
                        "moderation_comments":"amazing story!",
                        },
                        follow=True)
        # assert ending up on right page
        self.assertRedirects(response, "/",
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')
        # test that no changes were made
        pe = PublicExperience.objects.get(experience_id='test-test-test')
        self.assertEqual(pe.mentalhealth,False)
        self.assertEqual(pe.other,"")
        self.assertEqual(pe.moderation_status,"not reviewed")

    def test_single_moderation_view_as_non_moderator_post_rejected(self):
        """
        Test moderating single experience page fails when done by non-moderator
        """

        c = Client()
        c.force_login(self.non_moderator_user)

        response = c.post("/main/moderate/test-test-test/",
                        {"mentalhealth": True, "other":"New trigger",
                        "moderation_status":"rejected",
                        "moderation_comments":"amazing story!",
                        },
                        follow=True)
        # assert ending up on right page
        self.assertRedirects(response, "/",
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'main/home.html')
        # test that no changes were made
        pe = PublicExperience.objects.get(experience_id='test-test-test')
        self.assertEqual(pe.mentalhealth,False)
        self.assertEqual(pe.other,"")
        self.assertEqual(pe.moderation_status,"not reviewed")

    # test moderation pages as logged-in moderator

    def test_view_moderate_list_moderator(self):
        """
        Test moderate overview page is accessible by moderators
        """
        c = Client()
        c.force_login(self.moderator_user)
        response = c.get("/main/moderate_public_experiences", follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderate_public_experiences.html')

    def test_view_moderate_pending_list_moderator(self):
        """
        Test moderate pending overview page is accessible by moderators
        """
        c = Client()
        c.force_login(self.moderator_user)
        response = c.get("/main/moderation_list", {"status": "pending"}, follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')

    def test_view_moderate_approved_list_moderator(self):
        """
        Test moderate approved overview page is accessible by moderators
        """
        c = Client()
        c.force_login(self.moderator_user)
        response = c.get("/main/moderation_list", {"status": "approved"}, follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')

    def test_view_moderate_rejected_list_moderator(self):
        """
        Test moderate rejected overview page is accessible by moderators
        """
        c = Client()
        c.force_login(self.moderator_user)
        response = c.get("/main/moderation_list", {"status": "rejected"}, follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')

    def test_view_moderate_invalid_list_moderator(self):
        """
        Test moderate overview page is accessible by moderators when the status is invalid

        It should default to the "pending" view.
        """
        c = Client()
        c.force_login(self.moderator_user)
        response = c.get("/main/moderation_list", {"status": "unknown"}, follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')

    def test_view_moderate_pending_list_search_moderator(self):
        """
        Test moderate pending overview page with a search parameter
        """
        c = Client()
        c.force_login(self.moderator_user)
        response = c.get("/main/moderation_list", {"status": "pending", "searched": "something"}, follow=True)
        # TODO: Check that the search returns sensible results
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')

    def test_single_moderation_view_as_moderator_get(self):
        """
        Test moderate single experience page is accessible by moderators
        """
        c = Client()
        c.force_login(self.moderator_user)
        response = c.get("/main/moderate/test-test-test/", follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderate_experience.html')


    def test_single_moderation_view_as_moderator_post_missing_data(self):
        """
        Test that the moderation page redirects appropriately even with missing data
        """
        c = Client()
        c.force_login(self.moderator_user)
        self.assertEqual(len(PublicExperience.objects.all()),1)
        # ideally would add a cassette here too
        response = c.post("/main/moderate/test-test-test/",
                          {"mentalhealth": True, "other":"New trigger",
                          "first_hand_authorship": True,
                          "moderation_prior":"approved",
                          "moderation_reply":"[]",
                          },
                          follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')
        # Public experience should be deleted as no longer access on OH
        self.assertEqual(len(PublicExperience.objects.all()),0)

    def test_single_moderation_view_as_moderator_post(self):
        """
        Test moderate single experience page is successfully accessible and editable by moderators
        """

        c = Client()
        c.force_login(self.moderator_user)
        # Test uses cassette to allow fake-upload to OH
        with vcr.use_cassette('server/apps/main/tests/fixtures/moderate_experience.yaml',
                      filter_query_parameters=['access_token'],match_on=['path']):
            response = c.post("/main/moderate/test-test-test/",
                            {"mentalhealth": True, "other":"New trigger",
                            "first_hand_authorship": True,
                            "moderation_status":"approved",
                            "moderation_comments":"amazing story!",
                            "moderation_prior":"not reviewed",
                            },
                            follow=True)
        # assert ending up on right page
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')
        # test that all changes were made
        pe = PublicExperience.objects.get(experience_id='test-test-test')
        self.assertEqual(pe.mentalhealth,True)
        self.assertEqual(pe.other,"New trigger")
        self.assertEqual(pe.moderation_status,"approved")
        # Try injecting additional information that should be immutable
        # Should raise KeyError in form
        with self.assertRaises(KeyError) as ce:
            response = c.post("/main/moderate/test-test-test/",
                            {"mentalhealth": True, "other":"New trigger",
                             "first_hand_authorship": True,
                            "moderation_status":"approved",
                            "moderation_comments":"amazing story!",
                            "moderation_reply":"Moderation reply",
                            "moderation_prior":"not reviewed",
                            "title_text": 'try injection!'
                            },
                            follow=True)
        # Check that key-error was caused by title text
        self.assertEqual(str(ce.exception),"'title_text'")

    def test_single_moderation_view_as_moderator_post_empty_comment(self):
        """
        Test moderation with an empty comment is successful
        """

        c = Client()
        c.force_login(self.moderator_user)
        # Test uses cassette to allow fake-upload to OH
        with vcr.use_cassette('server/apps/main/tests/fixtures/moderate_experience.yaml',
                      filter_query_parameters=['access_token'],match_on=['path']):
            response = c.post("/main/moderate/test-test-test/",
                            {"mentalhealth": True, "other":"New trigger",
                            "first_hand_authorship": True,
                            "moderation_status":"approved",
                            "moderation_comments":"",
                            "moderation_prior":"not reviewed",
                            },
                            follow=True)
        # assert ending up on right page
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')
        # test that all changes were made
        pe = PublicExperience.objects.get(experience_id='test-test-test')
        self.assertEqual(pe.mentalhealth,True)
        self.assertEqual(pe.other,"New trigger")
        self.assertEqual(pe.moderation_status,"approved")
        eh = ExperienceHistory.objects.filter(experience=pe)
        self.assertEqual(len(eh), 2)
        self.assertEqual(eh[1].change_comments, "No Comment Made")
        self.assertEqual(eh[1].change_reply, "")

    def test_single_moderation_view_as_moderator_post_not_reviewed_reply(self):
        """
        Test moderation submitting a "not reviewed" status with moderation reply
        """

        c = Client()
        c.force_login(self.moderator_user)
        # Test uses cassette to allow fake-upload to OH
        with vcr.use_cassette('server/apps/main/tests/fixtures/moderate_experience.yaml',
                      filter_query_parameters=['access_token'],match_on=['path']):
            response = c.post("/main/moderate/test-test-test/",
                            {"mentalhealth": True, "other":"New trigger",
                            "first_hand_authorship": True,
                            "moderation_status":"not reviewed",
                            "moderation_comments":"amazing story!",
                            "moderation_reply":"a reply isn't allowed if not reviewed",
                            "moderation_prior":"rejected",
                            },
                            follow=True)
        # assert ending up on right page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/moderate_experience.html')
        self.assertContains(response, "Stories that are not being reviewed cannot have moderation replies added to them.", status_code=200)

    def post_approval(self, reply):
        """
        Sends and approval message with reply comments and returns the response
        """
        c = Client()
        c.force_login(self.moderator_user)
        # Test uses cassette to allow fake-upload to OH
        with vcr.use_cassette('server/apps/main/tests/fixtures/moderate_experience.yaml',
                      filter_query_parameters=['access_token'],match_on=['path']):
            response = c.post("/main/moderate/test-test-test/",
                            {"mentalhealth": True, "other":"New trigger",
                            "first_hand_authorship": True,
                            "moderation_status":"approved",
                            "moderation_comments":"amazing story!",
                            "moderation_reply": reply,
                            "moderation_prior":"rejected",
                            },
                            follow=True)
        return response

    def test_single_moderation_view_as_moderator_post_approved_red(self):
        """
        Test moderation submitting an "approved" status with "Red" moderation reply
        """

        reply = ('[{'
            '"reason": "Something serious", '
            '"href": "here", '
            '"severity": "red", '
            '"text": "bad stuff"}]'
        )
        response = self.post_approval(reply)

        # assert ending up on right page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/moderate_experience.html')
        self.assertContains(response, "Stories with Red moderation reasons can&#x27;t be given approved status.", status_code=200)

    def test_single_moderation_view_as_moderator_post_approved_amber(self):
        """
        Test moderation submitting an "approved" status with "Amber" moderation reply
        """

        reply = ('[{'
            '"reason": "Something not so serious", '
            '"href": "here", '
            '"severity": "amber", '
            '"text": "triggering stuff"}]'
        )

        response = self.post_approval(reply)

        # assert ending up on right page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')

    def test_single_moderation_view_as_moderator_post_approved_malformed(self):
        """
        Test moderation submitting an "approved" status with malformed JSON moderation reply
        """

        reply = ('malformed [{'
            '"reason": "Something not so serious", '
        )

        response = self.post_approval(reply)

        # assert ending up on right page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')

    @vcr.use_cassette(
        'server/apps/main/tests/fixtures/moderate_experience.yaml',
        record_mode="none",
        filter_query_parameters=['access_token'],
        match_on=['path'],
    )
    def moderate_message(self, status_prior, status_post, comms_review):
        """
        A helper method for testing message sending with different moderation conditions
        """
        # Ensure the user profile has the correct message send flag
        self.moderator_profile.comms_review = comms_review
        self.moderator_profile.save()

        c = Client()
        c.force_login(self.moderator_user_with_profile)
        # Test uses cassette to allow fake-upload to OH
        response = c.post("/main/moderate/test-test-test/",
                        {
                            "mentalhealth": True,
                            "other": "New trigger",
                            "moderation_status": status_post,
                            "moderation_comments": "",
                            "moderation_prior": status_prior,
                        },
                        follow=True)
        # assert ending up on right page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/moderation_list.html')

    @mock.patch('openhumans.models.OpenHumansMember.message')
    def test_single_moderation_view_as_moderator_post_message_approved_send(self, mock_message):
        """
        Test that moderation change emails are sent if a post is approved
        and the user wants them
        """
        self.moderate_message("not moderated", "approved", True)

        # test that the message was sent
        mock_message.assert_called_once()

    @mock.patch('openhumans.models.OpenHumansMember.message')
    def test_single_moderation_view_as_moderator_post_message_rejected_send(self, mock_message):
        """
        Test that moderation change emails are sent if a post is rejected
        and the user wants them
        """
        self.moderate_message("not moderated", "rejected", True)

        # test that the message was sent
        mock_message.assert_called_once()

    @mock.patch('openhumans.models.OpenHumansMember.message')
    def test_single_moderation_view_as_moderator_post_message_no_change_no_send(self, mock_message):
        """
        Test that moderation change emails are not sent if the moderation status
        doesn't change, even if the user wants moderation messages
        """
        self.moderate_message("approved", "approved", True)

        # test that no message was sent
        mock_message.assert_not_called()

    @mock.patch('openhumans.models.OpenHumansMember.message')
    def test_single_moderation_view_as_moderator_post_message_no_send(self, mock_message):
        """
        Test that moderation change emails are not sent if the user doesn't wants them
        even if the moderation status changes
        """
        self.moderate_message("not moderated", "approved", False)

        # test that no message was sent
        mock_message.assert_not_called()
