import abc
import json
import random
import sys
import string

from django.conf import settings

import requests


def random_key(length=10):
    """Generate a random key mixing string and digits"""
    return ''.join(random.choice(string.letters + string.digits) 
        for i in xrange(length)) 


class Transport(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(url):
        """Subclasses must implement this as a @staticmethod"""
        pass


class GoogleSandBox(Transport):
    @staticmethod
    def create(long_url):
        # fake request to simulate network latency
        requests.post('https://google.com')
        return 'http://sandbox/%s' % random_key()


class Google(Transport):
    @staticmethod
    def create(long_url):
        # using get api
        response = requests.post('http://goo.gl/api/url', 
                params={'url': long_url})
        results = json.loads(response.content)
        return results['short_url']
       

class UrlShortener(object):
    def __init__(self, transport_name='GoogleSandBox'):
        # check if settings specified a backend to use
        self.transport_name = getattr(settings, 'SHORTENER_BACKEND', \
                transport_name)

        try:
            # str to class from current module
            klass = getattr(sys.modules[__name__], self.transport_name)
        except AttributeError:
            raise NameError("%s doesn't exist." % self.transport_name)
        
        # instatiate our shortener backend
        self.transport = klass

    def __getattr__(self, attr):
        return getattr(self.transport, attr)
