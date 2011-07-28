from django.test import TestCase

from gateway_backend.backend import Transport, Google, GoogleSandBox, UrlShortener


class RequestTest(TestCase):
    def test__init__(self):
        from django.conf import settings
        if hasattr(settings, 'SHORTENER_BACKEND'):
            delattr(settings, 'SHORTENER_BACKEND')

        request = UrlShortener()
        self.assertEqual(request.transport_name, 'GoogleSandBox') 
        self.assertTrue(request.transport, GoogleSandBox)

        settings.SHORTENER_BACKEND = 'Google'
        request = UrlShortener()
        self.assertEqual(request.transport_name, settings.SHORTENER_BACKEND) 
        self.assertTrue(request.transport, Google)

        delattr(settings, 'SHORTENER_BACKEND')
        request = UrlShortener(transport_name='GoogleSandBox')
        self.assertEqual(request.transport_name, 'GoogleSandBox') 
        self.assertTrue(request.transport, GoogleSandBox)
    
        with self.assertRaises(NameError):
            UrlShortener(transport_name='X')

        self.assertNotEqual(UrlShortener().create('hakta.com'), None)
        self.assertNotEqual(UrlShortener().create('hakta.com'), '')


class UrlShortenerTest(TestCase):
    def test_google_sandbox(self):
        shortener = GoogleSandBox()
        key = shortener.create('http://hakta.com')
        self.assertNotEqual(key, '')
        self.assertNotEqual(key, None)
        self.assertTrue('sandbox' in key)

    def test_google(self):
        shortener = Google()
        key = shortener.create('http://hakta.com')
        self.assertNotEqual(key, '')
        self.assertNotEqual(key, None)
        self.assertTrue('goo.gl' in key)

    def test_url_shortener(self):
        with self.assertRaises(TypeError):
            Transport()
