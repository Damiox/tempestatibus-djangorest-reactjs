from django.conf import settings
from django.test import SimpleTestCase
from flake8.api import legacy as flake8
from tempestatibus.api.tests.io import CaptureStdout


class Flake8ConformanceTestCase(SimpleTestCase):
    def test_flake8_conformance(self):
        with CaptureStdout() as stdout:
            flake8_style = flake8.get_style_guide(
                exclude=['*/env/*', '*/node_modules/*', '*/migrations/*'])
            report = flake8_style.check_files([settings.BASE_DIR])
        if report.total_errors > 0:
            self.fail(
                'Got some flake8 errors:\n{0}'.format(stdout),
            )
