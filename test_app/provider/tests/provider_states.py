"""
Provider state setup functions for Pact contract
verification tests.
"""
from library.models import Author, Book


def setup_nothing():
    # - Nothing
    pass


def setup_an_author_id_1():
    # - An Author id 1
    # TODO:
    Author.objects.create(id=1, name="Blake Crouch")


def setup_an_author_id_1_a_book_exists_with_author_id_1():
    # - An Author id 1
    # - A Book exists with author ID 1
    author = Author.objects.create(id=1, name="Frank Herbert")
    Book.objects.create(id=1, author=author, title="Dune")
