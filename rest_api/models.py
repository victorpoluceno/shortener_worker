from django.db import models
from django.contrib.auth.models import User


class Url(models.Model):
    long_url = models.CharField(max_length=250)#, unique=True) #FIXME
    key = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return "<%s, %s>"  % (self.id, self.long_url)
