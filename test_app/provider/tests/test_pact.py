from django.test import TestCase

from pact_testgen.models import Response as PactResponse
from pact_testgen.utils import Response
from pact_testgen.verify import verify_response

from library.models import Author, Book


class Test_nothing(TestCase):

    def setUp(self):
        # TODO: Implement me!
        pass

    def test_test_an_author_creation_request(self):
        raw_actual_response = self.client.generic(
            "POST",
            "/authors",
            {"name": "Neal Stephenson"}
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {'body': {'name': 'Neal Stephenson', 'id': 1}, 'headers': None, 'matchingRules': {'body': {'$.id': {'matchers': [{'match': 'type', 'max': None, 'min': None, 'regex': None}]}}}, 'status': 201}
        expected = PactResponse(**raw_expected_response)

        success = verify_response("LibraryClient", "Library", expected, actual)
        self.assertTrue(success)

    def test_test_a_book_search_request_for_a_non_existent_author(self):
        raw_actual_response = self.client.generic(
            "GET",
            "/books",

        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {'body': [], 'headers': None, 'matchingRules': None, 'status': 200}
        expected = PactResponse(**raw_expected_response)

        success = verify_response("LibraryClient", "Library", expected, actual)
        self.assertTrue(success)


class Test_author_id_1_exists(TestCase):

    def setUp(self):
        Author.objects.create(id=1, name="Douglas Adams")

    def test_test_a_request_for_author_id_1(self):
        raw_actual_response = self.client.generic(
            "GET",
            "/authors/1",

        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {'body': {'id': 1, 'name': 'Blake Crouch'}, 'headers': None, 'matchingRules': {'body': {'$': {'matchers': [{'match': 'type', 'max': None, 'min': None, 'regex': None}]}}}, 'status': 200}
        expected = PactResponse(**raw_expected_response)

        success = verify_response("LibraryClient", "Library", expected, actual)
        self.assertTrue(success)


class Test_an_author_with_id_1(TestCase):

    def setUp(self):
        Author.objects.create(id=1, name="Douglas Adams")

    def test_test_an_author_update_request(self):
        raw_actual_response = self.client.generic(
            "PATCH",
            "/authors/1",
            {"name": "Helene Wecker"}
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {'body': {'name': 'Helene Wecker', 'id': 1}, 'headers': None, 'matchingRules': {'body': {'$.id': {'matchers': [{'match': 'type', 'max': None, 'min': None, 'regex': None}]}}}, 'status': 200}
        expected = PactResponse(**raw_expected_response)

        success = verify_response("LibraryClient", "Library", expected, actual)
        self.assertTrue(success)

    def test_test_an_author_deletion_request(self):
        raw_actual_response = self.client.generic(
            "DELETE",
            "/authors/1",

        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {'body': None, 'headers': None, 'matchingRules': None, 'status': 204}
        expected = PactResponse(**raw_expected_response)

        success = verify_response("LibraryClient", "Library", expected, actual)
        self.assertTrue(success)


class Test_a_book_exists_with_author_id_1_an_author_with_id_1(TestCase):

    def setUp():
        author = Author.objects.create(id=1, name="Douglas Adams")
        book = Book.objects.create(id=1, title="Hitchiker's Guide to the Galaxy")

    def test_test_a_book_search_request_for_author_id_1(self):
        raw_actual_response = self.client.generic(
            "GET",
            "/books",

        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {'body': [{'id': 1, 'title': 'Dune'}], 'headers': None, 'matchingRules': {'body': {'$': {'matchers': [{'match': 'type', 'max': None, 'min': 1, 'regex': None}]}}}, 'status': 200}
        expected = PactResponse(**raw_expected_response)

        success = verify_response("LibraryClient", "Library", expected, actual)
        self.assertTrue(success)
