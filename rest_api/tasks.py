from celery.task import task
from celery.task.sets import subtask

from rest_api.models import Url
from rest_api.backend import Request

#TODO: read long_url from memcache
#TODO: ensure with retry that if we made a resquest we have to save the result 
#TODO: should we ensure that user are logged and have permission here two?


class UrlAlreadyUpdatedError(Exception):
    pass


@task(ignore_result=False)
def url_short(url_id):
    url = Url.objects.get(pk=url_id)
    if url.key:
        raise UrlAlreadyUpdatedError(
                'Url %s already updated, possible duplicate task!' % url)

    # request an url shortner for the given url
    short_url = Request().create(url.long_url)

    url.key = short_url
    url.save()

    return short_url
