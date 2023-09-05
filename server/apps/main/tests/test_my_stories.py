from django.test import RequestFactory, TestCase, Client
from django.core.paginator import Paginator
from server.apps.main.helpers import filter_by_tag, filter_by_moderation_status, filter_in_review, paginate_stories

# ------ test story filters -------- #

class StoryFiltersTestCase(TestCase):
    def setUp(self):
        self.files = [
            {
                'metadata': {
                    'tags': ['tag1', 'tag2'],
                    'data': {'moderation_status': 'approved'}
                }
            },
            {
                'metadata': {
                    'tags': ['tag2', 'tag3'],
                    'data': {'moderation_status': 'pending'}
                }
            },
            {
                'metadata': {
                    'tags': ['tag3', 'tag4'],
                    'data': {'moderation_status': 'rejected'}
                }
            },
            {
                'metadata': {
                    'tags': ['public'],
                    'data': {'moderation_status': 'not reviewed'}
                }
            },
            {
                'metadata': {
                    'tags': ['tag5'],
                    'data': {'moderation_status': 'in review'}
                }
            },
            {
                'metadata': {
                    'tags': ['tag6'],
                    'data': {'moderation_status': 'not reviewed'}
                }
            },
            {
                'metadata': {
                    'tags': ['tag7'],
                    'data': {'moderation_status': 'approved'}
                }
            },
        ]

    def test_filter_by_tag(self):
        filtered_files = filter_by_tag(self.files, 'tag2')
        self.assertEqual(len(filtered_files), 2)

    def test_filter_by_moderation_status(self):
        filtered_files = filter_by_moderation_status(self.files, 'approved')
        self.assertEqual(len(filtered_files), 2)

    def test_filter_in_review(self):
        filtered_files = filter_in_review(self.files)
        self.assertEqual(len(filtered_files), 2)
        