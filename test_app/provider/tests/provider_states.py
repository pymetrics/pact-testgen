"""
Provider state setup functions for Pact contract
verification tests.
"""
from library.models import Author, Book


def setup_nothing():
    pass


def setup_an_author_with_id_1_exists():
    Author.objects.create(id=1, name="Blake Crouch")


def setup_an_author_with_id_1_exists_a_book_exists_with_author_id_1():
    author = Author.objects.create(id=1, name="Frank Herbert")
    Book.objects.create(id=1, author=author, title="Dune")
