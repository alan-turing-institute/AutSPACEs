from django.test import RequestFactory, TestCase, Client
from django.core.paginator import Paginator
from server.apps.main.helpers import filter_by_tag, filter_by_moderation_status, filter_in_review, paginate_my_stories

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

        
# ------ test pagination -------- #

class TestPaginateMyStories(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_paginate_my_stories(self):
        request = self.factory.get('/my-stories/?page_test=2')  # mimic a request for the second page
        files = list(range(100))  # use simple list for testing
        paginator = Paginator(files, 10)  # 10 items per page
        page_key = 'page_test'  # the GET parameter to check in the request

        stories = paginate_my_stories(request, paginator, page_key)

        # Is the function correctly getting the page number from the request?
        self.assertEqual(stories.number, 2)

        # Check that the correct data is returned: the second set of 10 items.
        self.assertEqual(list(stories.object_list), list(range(10, 20)))

        # Check that page_range was correctly updated
        # For page 2 with 2 pages on each side and 1 page on each end, the range should be [1, 2, 3, 4, '…', 10]
        self.assertEqual(list(stories.page_range), [1, 2, 3, 4, '…', 10])

        # Check that offset was correctly set
        # For page 2 with 10 items per page, the offset should be 10
        self.assertEqual(stories.offset, 10)
        