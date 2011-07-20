from django.test import TestCase

from rest_api.backend import Request, Google


class BackendTest(TestCase):
    def test_request_sandbox(self):
        request = Request()
        key = request.create('http://hakta.com')
        self.assertNotEqual(key, '')
        self.assertNotEqual(key, None)
        self.assertTrue('sandbox' in key)

        request = Request(backend=Google)
        key = request.create('http://hakta.com')
        self.assertNotEqual(key, '')
        self.assertNotEqual(key, None)
        self.assertTrue('goo.gl' in key)
