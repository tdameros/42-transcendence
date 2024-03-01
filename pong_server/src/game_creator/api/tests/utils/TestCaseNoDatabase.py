from django.test import TestCase


class TestCaseNoDatabase(TestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass
