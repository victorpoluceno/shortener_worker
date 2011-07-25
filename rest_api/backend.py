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


class UrlShortener(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(url):
        """Subclasses must implement this as a @staticmethod"""
        pass


class GoogleSandBox(UrlShortener):
    @staticmethod
    def create(long_url):
        # fake request to simulate network latency
        requests.post('https://google.com')
        return 'http://sandbox/%s' % random_key()


class Google(UrlShortener):
    @staticmethod
    def create(long_url):
        # using get api
        response = requests.post('http://goo.gl/api/url', 
                params={'url': long_url})
        results = json.loads(response.content)
        return results['short_url']
       

class Request(object):
    def __init__(self, backend='GoogleSandBox'):
        # check if settings specified a backend to use
        self.backend = getattr(settings, 'SHORTENER_BACKEND', backend)

        try:
            # str to class from current module
            klass = getattr(sys.modules[__name__], self.backend)
        except AttributeError:
            raise NameError("%s doesn't exist." % self.backend)
        
        # instatiate our shortener backend
        self.shortener = klass()

    def __getattr__(self, attr):
        try:
            return getattr(self.shortener, attr)
        except AttributeError:
            # raise again to show Request as the object
            raise AttributeError("'%s' object has no attribute '%s'" \
                    % (self.__class__.__name__, attr))
