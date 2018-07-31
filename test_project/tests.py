from django.test import TestCase
from django.urls import reverse


class DjangoTracerTests(TestCase):

    def test_request_exists(self):
        url = reverse('request-test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'VIEW')

        # Pull out our request from headers
        header = response.get('X-Request-ID', None)

        # Make sure it exists
        self.assertIsNotNone(header)

        # Make sure it's 36 characters long (uuid4)
        self.assertEqual(len(header), 36)

        # Since it's a UUID it should have 4 hyphens in it's string
        # representation
        self.assertEqual(header.count('-'), 4)
