import json
from django.test import TestCase

from pact_testgen.public import Response, verify_response

from .provider_states import (
    setup_nothing,
    setup_an_author_with_id_1_exists,
    setup_an_author_with_id_1_exists_a_book_exists_with_author_id_1,
)


class TestNothing(TestCase):
    def setUp(self):
        setup_nothing()

    def an_author_creation_request(self):
        raw_actual_response = self.client.generic(
            "POST",
            "/authors",
            json.dumps({"name": "Neal Stephenson"}),
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

    def a_book_search_request_for_a_non_existent_author(self):
        raw_actual_response = self.client.generic(
            "GET", "/books", content_type="application/json"
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


class TestAnAuthorWithId1Exists(TestCase):
    def setUp(self):
        setup_an_author_with_id_1_exists()

    def a_request_for_author_id_1(self):
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

    def an_author_update_request(self):
        raw_actual_response = self.client.generic(
            "PATCH",
            "/authors/1",
            json.dumps({"name": "Helene Wecker"}),
            content_type="application/json",
        )
        actual = Response.from_django_response(raw_actual_response)

        raw_expected_response = {
            "body": {"name": "Helene Wecker", "id": 1},
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

    def an_author_deletion_request(self):
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


class TestAnAuthorWithId1ExistsABookExistsWithAuthorId1(TestCase):
    def setUp(self):
        setup_an_author_with_id_1_exists_a_book_exists_with_author_id_1()

    def a_book_search_request_for_author_id_1(self):
        raw_actual_response = self.client.generic(
            "GET", "/books", content_type="application/json"
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
