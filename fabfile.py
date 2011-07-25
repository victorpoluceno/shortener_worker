from fabric.api import local, put, run, sudo

def run_tests(settings="settings"):
    local("python manage.py test rest_api --settings=%s" % settings)

def run_integration_test(settings="settings_test"):
    local("export PYTHONPATH=.")
    local("export DJANGO_SETTINGS_MODULE=%s" % settings)
    local("python rest_api/tests/test_integration.py")
