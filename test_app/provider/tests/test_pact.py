import json
from django.test import TestCase

from pact_testgen.public import Response, verify_response

from .provider_states import (
    setup_an_author_id_1,
    setup_an_author_id_1_a_book_exists_with_author_id_1,
)


class TestNoInitialState(TestCase):
    def test_an_author_creation_request(self):
        raw_actual_response = self.client.generic(
            "POST",
            "/authors",
            data='{"name": "Neal Stephenson", "is_featured": false}',
            content_type="application/json",
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {
            "body": {"name": "Neal Stephenson", "id": 1},
            "headers": None,
            "matchingRules": {
                "body": {
                    "$.id": {
                        "matchers": [
                            {"match": "type", "max": None, "min": None, "regex": None}
                        ]
                    }
                }
            },
            "status": 201,
        }

        result = verify_response(
            "LibraryClient", "Library", raw_expected_response, actual, version="3.0.0"
        )
        result.assert_success()

    def test_a_book_search_request_for_a_non_existent_author(self):
        raw_actual_response = self.client.generic(
            "GET",
            "/books",
            QUERY_STRING="authorId=100",
            content_type="application/json",
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {
            "body": [],
            "headers": None,
            "matchingRules": None,
            "status": 200,
        }

        result = verify_response(
            "LibraryClient", "Library", raw_expected_response, actual, version="3.0.0"
        )
        result.assert_success()


class TestAnAuthorId1(TestCase):
    def setUp(self):
        setup_an_author_id_1()

    def test_a_request_for_author_id_1(self):
        raw_actual_response = self.client.generic(
            "GET", "/authors/1", content_type="application/json"
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {
            "body": {"id": 1, "name": "Blake Crouch"},
            "headers": None,
            "matchingRules": {
                "body": {
                    "$": {
                        "matchers": [
                            {"match": "type", "max": None, "min": None, "regex": None}
                        ]
                    }
                }
            },
            "status": 200,
        }

        result = verify_response(
            "LibraryClient", "Library", raw_expected_response, actual, version="3.0.0"
        )
        result.assert_success()

    def test_an_author_update_request(self):
        raw_actual_response = self.client.generic(
            "PATCH",
            "/authors/1",
            data='{"name": "Helene Wecker", "is_featured": true}',
            content_type="application/json",
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {
            "body": {"name": "Helene Wecker", "id": 1, "is_featured": True},
            "headers": None,
            "matchingRules": {
                "body": {
                    "$.id": {
                        "matchers": [
                            {"match": "type", "max": None, "min": None, "regex": None}
                        ]
                    }
                }
            },
            "status": 200,
        }

        result = verify_response(
            "LibraryClient", "Library", raw_expected_response, actual, version="3.0.0"
        )
        result.assert_success()

    def test_an_author_deletion_request(self):
        raw_actual_response = self.client.generic(
            "DELETE", "/authors/1", content_type="application/json"
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {
            "body": None,
            "headers": None,
            "matchingRules": None,
            "status": 204,
        }

        result = verify_response(
            "LibraryClient", "Library", raw_expected_response, actual, version="3.0.0"
        )
        result.assert_success()


class TestAnAuthorId1ABookExistsWithAuthorId1(TestCase):
    def setUp(self):
        setup_an_author_id_1_a_book_exists_with_author_id_1()

    def test_a_book_search_request_for_author_id_1(self):
        raw_actual_response = self.client.generic(
            "GET", "/books", QUERY_STRING="authorId=1", content_type="application/json"
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {
            "body": [{"id": 1, "title": "Dune"}],
            "headers": None,
            "matchingRules": {
                "body": {
                    "$": {
                        "matchers": [
                            {"match": "type", "max": None, "min": 1, "regex": None}
                        ]
                    }
                }
            },
            "status": 200,
        }

        result = verify_response(
            "LibraryClient", "Library", raw_expected_response, actual, version="3.0.0"
        )
        result.assert_success()

    def test_a_book_search_request_for_author_id_2(self):
        raw_actual_response = self.client.generic(
            "GET", "/books", QUERY_STRING="authorId=2", content_type="application/json"
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {
            "body": [],
            "headers": None,
            "matchingRules": None,
            "status": 200,
        }

        result = verify_response(
            "LibraryClient", "Library", raw_expected_response, actual, version="3.0.0"
        )
        result.assert_success()
