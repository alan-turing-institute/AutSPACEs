from unittest.mock import mock_open, patch
from urllib.error import HTTPError

from django.test import TestCase, Client, RequestFactory
from django.conf import settings
from openhumans.models import OpenHumansMember
from openhumans.settings import openhumans_settings
import requests_mock
import vcr


OH_BASE_URL = openhumans_settings['OPENHUMANS_OH_BASE_URL']
OH_API_BASE = OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'
OH_OAUTH2_REDIRECT_URI = '{}/complete'.format(settings.OPENHUMANS_APP_BASE_URL)
OH_GET_URL = OH_API_BASE + '/project/exchange-member/'


class LoginTestCase(TestCase):
    """
    Tests for index page and upload feature
    """

    def setUp(self):
        """
        Set up the app for following tests
        """
        settings.DEBUG = True
        self.factory = RequestFactory()
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='12345678',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()

    def test_index_logged_out(self):
        """
        Test index page when logged out
        """
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_logged_in(self):
        """
        Test if redirection happens when user logs in.
        """
        c = Client()
        c.login(username=self.user.username, password='foobar')
        response = c.get("/")
        self.assertRedirects(response, '/overview')

    def test_list_files_logged_out(self):
        """
        Test the list_files function when logged out.
        """
        c = Client()
        response = c.get("/list")
        self.assertRedirects(response, '/')
