from fabric.api import local

def run_tests(settings="settings"):
    local("python manage.py test rest_api --settings=%s" % settings)

def run_integration_tests(settings="settings_tests"):
    local("python manage.py syncdb --noinput --settings=%s" % settings)
    local("export PYTHONPATH=. && export DJANGO_SETTINGS_MODULE=%s "\
            "&& python rest_api/tests/test_integration.py" % settings)
