from celery.task import task

from rest_api.models import Url
from rest_api.backend import UrlShortener


class UrlAlreadyUpdatedError(Exception):
    pass


@task
def url_short(url_id):
    url = Url.objects.get(pk=url_id)
    if url.key:
        raise UrlAlreadyUpdatedError(
                'Url %s already updated, possible duplicate task!' % url)

    # request an url shortner for the given url
    short_url = UrlShortener().create(url.long_url)

    url.key = short_url
    url.save()
    return short_url
