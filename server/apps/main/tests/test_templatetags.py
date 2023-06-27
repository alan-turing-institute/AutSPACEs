from django.test import RequestFactory, TestCase
from server.apps.main.templatetags.custom_tags import url_replace

class UrlReplaceTest(TestCase):

    def setUp(self):
        # Create a request instance with some GET parameters
        self.factory = RequestFactory()
        self.request = self.factory.get('/example', {'param1': 'value1', 'param2': 'value2'})

    def test_url_replace(self):
        # Use the template tag to change 'param1' to 'newvalue'
        result = url_replace(self.request, 'param1', 'newvalue')

        # Check that the output URL has the correct parameters
        self.assertEqual(result, '?param1=newvalue&param2=value2')

    def test_url_replace_new_param(self):
        # Use the template tag to add 'param3' 
        result = url_replace(self.request, 'param3', 'value3')

        # Check that the output URL has the correct parameters
        self.assertEqual(result, '?param1=value1&param2=value2&param3=value3')
