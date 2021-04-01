from io import BytesIO

from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings
from openhumans.models import OpenHumansMember
import vcr


class IndexPageTestCase(TestCase):
    """
    Test cases for the index page.
    """

    def setUp(self):
        """
        Set up the app for following tests.
        """
        settings.DEBUG = True

    def test_index_page_content(self):
        """
        Test whether content is rendered properly.
        """
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


class LoginTestCase(TestCase):
    """
    Test the login logic of the OH API
    """

    def setUp(self):
        settings.DEBUG = True
        settings.OPENHUMANS_APP_BASE_URL = "http://127.0.0.1"

    def test_log_out_logged_out(self):
        """
        Tests logout function
        """
        c = Client()
        response = c.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_overview_logged_out(self):
        """
        Tests overview function when logged out
        """
        c = Client()
        response = c.get("/overview")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_log_out(self):
        """
        Tests logout function
        """
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='1234567890abcdef',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()
        c = Client()
        c.login(username=self.user.username, password='foobar')
        response = c.post('/logout')
        self.assertEqual(response.wsgi_request.user.username, '')
        self.assertRedirects(response, "/")

    def test_upload_logged_out(self):
        c = Client()
        response = c.get("/upload/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
