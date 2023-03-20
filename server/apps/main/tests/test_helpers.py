from django.test import TestCase
import vcr
import requests
from server.apps.main.helpers import reformat_date_string

class StoryHelper(TestCase):
    """
    Tests for the story page helpers
    """

    @vcr.use_cassette("server/apps/main/tests/fixtures/my_stories.yaml")
    def setUp(self):
        r = requests.get("https://www.openhumans.org/api/direct-sharing/project/exchange-member/")
        self.context = {"files" : r.json()['data']}


    def test_reformat_date(self):
        """
        Test that formating OH timestamp to native time object works
        """
        year = int(self.context['files'][0]['created'][:4])
        returned_context = reformat_date_string(self.context)
        self.assertEqual(returned_context['files'][0]['created'].year,year)

    def test_get_review_status(self):
        pass