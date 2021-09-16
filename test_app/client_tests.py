from pathlib import Path
from pactman.mock.matchers import EachLike
import pytest
from pactman import Consumer, Provider, Like

from client import LibraryClient

PACTS_DIR = Path(__file__).parent / "pactfiles"


@pytest.fixture(scope="session")
def pact():
    return Consumer("LibraryClient").has_pact_with(
        Provider("Library"), pact_dir=PACTS_DIR, version="3.0.0"
    )


@pytest.fixture
def library_client(pact):
    return LibraryClient(url_root=pact.uri)


def test_create_author(pact, library_client: LibraryClient):
    name = "Neal Stephenson"
    request_body = {"name": name}
    expected = {"name": name, "id": Like(1)}

    (
        pact.given(None)
        .upon_receiving("An author creation request")
        .with_request("POST", "/authors", body=request_body)
        .will_respond_with(201, body=expected)
    )

    with pact:
        library_client.create_author(name=name)


def test_get_author(pact, library_client: LibraryClient):
    expected = Like({"id": 1, "name": "Blake Crouch"})

    (
        pact.given("An Author", id=1)
        .upon_receiving("A request for author ID 1")
        .with_request("GET", "/authors/1")
        .will_respond_with(200, body=expected)
    )

    with pact:
        library_client.get_author(1)


def test_update_author(pact, library_client: LibraryClient):
    (
        pact.given("An Author", id=1)
        .upon_receiving("An author update request")
        .with_request("PATCH", "/authors/1", body={"name": "Helene Wecker"})
        .will_respond_with(200, body={"name": "Helene Wecker", "id": Like(1)})
    )

    with pact:
        library_client.update_author(1, "Helene Wecker")


def test_delete_author(pact, library_client: LibraryClient):
    (
        pact.given("An Author", id=1)
        .upon_receiving("An author deletion request")
        .with_request("DELETE", "/authors/1")
        .will_respond_with(204)
    )

    with pact:
        library_client.delete_author(1)


def test_get_books_by_author_no_author(pact, library_client: LibraryClient):
    (
        pact.given(None)
        .upon_receiving("A book search request for a non-existent author")
        .with_request("GET", "/books", query={"authorId": ["100"]})
        .will_respond_with(200, body=[])
    )

    with pact:
        library_client.get_books_by_author(100)


def test_get_books_by_author_success(pact, library_client: LibraryClient):
    expected = EachLike({"id": 1, "title": "Dune"})
    (
        pact.given("An Author", id=1)
        .and_given("A Book exists with author ID 1")
        .upon_receiving("A book search request for author ID 1")
        .with_request("GET", "/books", query={"authorId": ["1"]})
        .will_respond_with(200, body=expected)
    )

    with pact:
        library_client.get_books_by_author(1)
