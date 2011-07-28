import unittest
from unittest import TestCase

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_api.models import Url
from rest_api.tasks import url_short, \
        UrlAlreadyUpdatedError

WAIT_TIMEOUT = 5


class TaskNoEagerTest(TestCase):
    def setUp(self):
        query = Url.objects.all()
        query.exclude()

        self.url = Url.objects.create(long_url='hakta.com')
        self.url.save()

        settings.CELERY_ALWAYS_EAGER = False

    @unittest.skipIf(getattr(settings, 'BROKER_BACKEND', None), "memory")
    def test_url_short_task(self):
        result = url_short.delay(self.url.id)
        result.wait(timeout=WAIT_TIMEOUT)
        url_updated = Url.objects.get(pk=self.url.id)
        self.assertNotEqual(url_updated.key, '')
        self.assertNotEqual(url_updated.key, None)

        result = url_short.delay(9999)
        self.assertRaises(ObjectDoesNotExist, result.wait, (),
                {'timeout': WAIT_TIMEOUT})
        self.assertEqual(result.failed(), True)
        self.assertEqual(isinstance(result.result, ObjectDoesNotExist), True)
  
        url = Url.objects.create(long_url='test2.com')
        url.key = 'xxx'
        url.save()
        result = url_short.delay(url.id)
        self.assertRaises(UrlAlreadyUpdatedError, result.wait, (),
                {'timeout': WAIT_TIMEOUT})
        self.assertEqual(result.failed(), True)
        self.assertEqual(isinstance(result.result, UrlAlreadyUpdatedError),
                True)
        

if __name__ == '__main__':
    unittest.main()
