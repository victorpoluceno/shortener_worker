from django.test import TestCase

from django.contrib.auth.models import User

from gateway_backend.models import Url
from gateway_backend.tasks import url_short, \
        UrlAlreadyUpdatedError


class TaskTest(TestCase):
    def setUp(self):
        #TODO: replace by a fixture
        self.user = User.objects.create_user('tests', \
                email='victorpoluceno@gmail.com')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.url = Url.objects.create(long_url='hakta.com')
        self.url.save()

    def test_url_short_task(self):
        result = url_short.delay(self.url.id)
        url_updated = Url.objects.get(pk=self.url.id)
        self.assertNotEqual(url_updated.key, '')
        self.assertNotEqual(url_updated.key, None)

        result = url_short.delay(9999)
        self.assertEqual(result.failed(), True)
        self.assertEqual(isinstance(result.result, Url.DoesNotExist), True)
  
        url = Url.objects.create(long_url='test2.com')
        url.key = 'xxx'
        url.save()
        result = url_short.delay(url.id)
        self.assertEqual(result.failed(), True)
        self.assertEqual(isinstance(result.result, UrlAlreadyUpdatedError), 
                True)
