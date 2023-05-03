from django.test import TestCase
from django.template import Template, Context
from unittest.mock import MagicMock
import logging


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
        rendered_string = Template(
            "{% load story_filters %}"
            "{{ files|filter_by_tag:'tag2'|length }}"
        ).render(Context({'files': self.files}))

        self.assertEqual(int(rendered_string), 2)

    def test_filter_by_moderation_status(self):
        rendered_string = Template(
            "{% load story_filters %}"
            "{{ files|filter_by_moderation_status:'approved'|length }}"
        ).render(Context({'files': self.files}))

        self.assertEqual(int(rendered_string), 2)

    def test_filter_in_review(self):
        rendered_string = Template(
            "{% load story_filters %}"
            "{{ files|filter_in_review|length }}"
        ).render(Context({'files': self.files}))

        self.assertEqual(int(rendered_string), 2)
