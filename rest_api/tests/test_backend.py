from django.test import TestCase

from rest_api.backend import Request, Google, GoogleSandBox, UrlShortener


class RequestTest(TestCase):
    def test__init__(self):
        from django.conf import settings
        if hasattr(settings, 'SHORTENER_BACKEND'):
            delattr(settings, 'SHORTENER_BACKEND')

        request = Request()
        self.assertEqual(request.backend, 'GoogleSandBox') 
        self.assertTrue(isinstance(request.shortener, GoogleSandBox))

        settings.SHORTENER_BACKEND = 'Google'
        request = Request()
        self.assertEqual(request.backend, settings.SHORTENER_BACKEND) 
        self.assertTrue(isinstance(request.shortener, Google))

        delattr(settings, 'SHORTENER_BACKEND')
        request = Request(backend='GoogleSandBox')
        self.assertEqual(request.backend, 'GoogleSandBox') 
        self.assertTrue(isinstance(request.shortener, GoogleSandBox))
    
        with self.assertRaises(NameError):
            Request(backend='X')

        Request.create()


class UrlShortenerTest(TestCase):
    def test_google_sandbox(self):
        request = GoogleSandBox()
        key = request.create('http://hakta.com')
        self.assertNotEqual(key, '')
        self.assertNotEqual(key, None)
        self.assertTrue('sandbox' in key)

    def test_google(self):
        request = Google()
        key = request.create('http://hakta.com')
        self.assertNotEqual(key, '')
        self.assertNotEqual(key, None)
        self.assertTrue('goo.gl' in key)

    def test_url_shortener(self):
        with self.assertRaises(TypeError):
            UrlShortener()
