from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from openhumans.models import OpenHumansMember
from server.apps.main.models import PublicExperience
from server.apps.users.models import UserProfile
import vcr

class SeedDBTest(TestCase):
    def test_seed_empty_db(self):
        """
        Test that correctly populate from empty db (first load)
        """
        oh_members_before = OpenHumansMember.objects.all()
        pe_before = PublicExperience.objects.all()
        assert len(oh_members_before) == 0
        assert len(pe_before) == 0
        call_command("seed_db", file="server/apps/main/tests/fixtures/example_experiences_seed.csv")
        oh_members_after = OpenHumansMember.objects.all()
        assert len(oh_members_after) == 1
        pe_after = PublicExperience.objects.all()
        assert len(pe_after) == 7

    def test_seed_filled_db(self):
        """
        Test that correctly populate from empty db (first load)
        """
        # generate prior OH member & PE
        data = {"access_token": 'foo',
        "refresh_token": 'bar',
        "expires_in": 36000}
        existing_ohm = OpenHumansMember.create(oh_id="12345678",data=data)
        existing_ohm.save()
        pe_data = {
                "title_text": 'foo',
                "experience_text": 'bar',
                "difference_text": 'foobar',
                "moderation_status": "approved",
                "first_hand_authorship": "True",
                }
        PublicExperience.objects.create(open_humans_member=existing_ohm, experience_id=1001, **pe_data)

        # check that there's 1 existing OHM & PE
        oh_members_before = OpenHumansMember.objects.all()
        pe_before = PublicExperience.objects.all()
        assert len(oh_members_before) == 1
        assert len(pe_before) == 1
        # run command
        call_command("seed_db", file="server/apps/main/tests/fixtures/example_experiences_seed.csv")
        # there should now be two OH members and 8 stories
        oh_members_after = OpenHumansMember.objects.all()
        assert len(oh_members_after) == 2
        pe_after = PublicExperience.objects.all()
        assert len(pe_after) == 8
    
    # This is the cassette for testing the user views.py function user_profile_delete which incorporates
    # the helper function used in the unseed command
    @vcr.use_cassette(
        'server/apps/users/tests/fixtures/delete_user.yaml',
        record_mode="none",
        filter_query_parameters=['access_token'],
        match_on=['path'],
    ) 
    def test_unseed_filled_db(self):
        """
        Test that the unseed function works on a seeded db with a user profile and added stories
        """
        # Placeholder data
        data = {"access_token": "123456", "refresh_token": "bar", "expires_in": 36000}

        # Create user A
        oh_a = OpenHumansMember.create(oh_id=12345678, data=data)
        oh_a.save()
        user_a = oh_a.user
        user_a.openhumansmember = oh_a
        user_a.set_password("password_a")
        user_a.save()
        up_a = UserProfile.objects.create(user=user_a, **{"profile_submitted": True})

        pe_data = {
            "experience_text": "Here is some experience text",
            "difference_text": "Here is some difference text",
            "title_text": "Here is the title",
            "first_hand_authorship": "True",
        }

        pe = PublicExperience.objects.create(
            open_humans_member=oh_a, experience_id="112212111122112", **pe_data
        )

        user_profiles_before = UserProfile.objects.all()
        pe_before = PublicExperience.objects.all()

        assert len(user_profiles_before) == 1
        assert len(pe_before) == 1

        # Seed DB with 7 stories (but no additoinal user)
        call_command("seed_db", file="server/apps/main/tests/fixtures/example_experiences_seed.csv")

        user_profiles_after_seed = UserProfile.objects.all()
        pe_after_seed = PublicExperience.objects.all()

        assert len(user_profiles_after_seed) == 1
        assert len(pe_after_seed) == 8

        # "Unseed" the DB
        call_command("unseed_db")

        user_profiles_after_unseed = UserProfile.objects.all()
        pe_after_unseed = PublicExperience.objects.all()

        assert len(user_profiles_after_unseed) == 0
        assert len(pe_after_unseed) == 0


