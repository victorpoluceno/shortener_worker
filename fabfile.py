from fabric.api import local, run, settings

def run_tests(settings_file="settings"):
    local("python manage.py test gateway_backend --settings=%s" % settings_file)

def run_integration_tests(settings_file="settings_tests"):
    local("python manage.py syncdb --noinput --settings=%s" % settings_file)
    with settings(warn_only=True):
        if local("test -e celeryd.pid").failed:
            local("python manage.py celeryd_detach --settings=%s" % settings_file)

    local("export PYTHONPATH=. && export DJANGO_SETTINGS_MODULE=%s "\
            "&& python gateway_backend/tests/test_integration.py" % settings_file)

def deploy():
    local("dotcloud push shortener")
    local('dotcloud run shortener.www "cd current && python manage.py '\
            'syncdb --settings=settings_production --noinput"')
