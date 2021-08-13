from django.test import TestCase

from library.models import Author


class AuthorTestCase(TestCase):
    def test_can_create_author(self):
        # Really just exists to make sure the test runner
        # is picking up these tests
        Author.objects.create()
