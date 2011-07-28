from django.test import TestCase
from django.db import IntegrityError

from rest_api.models import Url

class UrlTest(TestCase):
    def test_create(self):
        url = Url.objects.create(long_url='http://hakta.com')
        url.save()

        self.assertEqual(url.long_url, 'http://hakta.com')
        self.assertEqual(url.key, '')

    def test_unique(self):
        query = Url.objects.all()
        query.delete()

        url = Url.objects.create(long_url='http://hakta.com')
        url.save()

        with self.assertRaises(IntegrityError):
            url = Url.objects.create(long_url='http://hakta.com')
