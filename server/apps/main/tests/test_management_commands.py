from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from openhumans.models import OpenHumansMember
from server.apps.main.models import PublicExperience

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
        # check there's still only single OHM + 7 PEs
        oh_members_after = OpenHumansMember.objects.all()
        assert len(oh_members_after) == 1
        pe_after = PublicExperience.objects.all()
        assert len(pe_after) == 7