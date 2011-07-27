from fabric.api import local, put, run, sudo

def run_tests(settings="settings"):
    local("python manage.py test rest_api --settings=%s" % settings)

def run_integration_tests(settings="settings_tests"):
    local("export PYTHONPATH=. && export DJANGO_SETTINGS_MODULE=%s "\
            "&& python rest_api/tests/test_integration.py" % settings)
