#!/usr/bin/env python
"""
This script is a trick to setup a fake Django environment, since this reusable
app will be developed and tested outside any specifiv Django project.

Via ``settings.configure`` you will be able to set all necessary settings
for your app and run the tests as if you were calling ``./manage.py test``.

"""

from django.conf import settings
from django_nose import NoseTestSuiteRunner
import sys
import coverage
import forex.settings.test_settings as test_settings

if not settings.configured:
    settings.configure(**test_settings.__dict__)


class NoseCoverageTestRunner(NoseTestSuiteRunner):
    """Custom test runner that uses nose and coverage"""
    def run_tests(self, *args, **kwargs):
        cov = coverage.Coverage()
        cov.start()
        results = super(NoseCoverageTestRunner, self).run_tests(
            *args, **kwargs)
        cov.stop()
        cov.save()
        cov.html_report()
        return results


def runtests(*test_args):
    failures = NoseCoverageTestRunner(verbosity=2, interactive=True).run_tests(
        test_args)

    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
