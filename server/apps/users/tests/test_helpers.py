from django.test import TestCase
from server.apps.users.helpers import update_session_success_or_confirm

class UserHelper(TestCase):
    """
    Tests for the user profile helpers
    """

    def setUp(self):
        '''
        Set-up for test with basic variables etc.
        '''
        pass

    def test_update_session_success_or_confirm(self):
        """
        Test that correct answers are fed to session
        """
        response = update_session_success_or_confirm('experience', None, False, None, None)
        self.assertEqual("Your experience will not be publicly accessible on AutSPACEs", response['s_or_c_whn_1'])

        response = update_session_success_or_confirm('experience', None, False, True, "message goes here")
        self.assertEqual("message goes here", response['s_or_c_whn_2'])

