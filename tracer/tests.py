from django.test import TestCase
from django.urls import reverse


class DjangoTracerTests(TestCase):

    def test_request_exists(self):
        url = reverse('request-test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
