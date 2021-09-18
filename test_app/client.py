import requests
from urllib.parse import urljoin


class LibraryClient:
    def __init__(self, url_root: str):
        self.url_root = url_root
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "LibraryClient/1.0 (Python)"})

    def make_request(self, method: str, path: str, json=None, params=None):
        url = urljoin(self.url_root, path)
        return self.session.request(method, url, json=json, params=params)

    # CRUD methods

    def create_author(self, name: str, is_featured=False):
        return self.make_request(
            "POST", "/authors", json={"name": name, "is_featured": is_featured}
        )

    def get_author(self, author_id: int):
        return self.make_request("GET", f"/authors/{author_id}")

    def update_author(self, author_id, name: str, is_featured=False):
        return self.make_request(
            "PATCH",
            f"/authors/{author_id}",
            json={"name": name, "is_featured": is_featured},
        )

    def delete_author(self, author_id):
        return self.make_request("DELETE", f"/authors/{author_id}")

    def create_book(self, title: str, author_id):
        return self.make_request(
            "POST", "/books", json={"title": title, "author": author_id}
        )

    def get_book(self, book_id: int):
        return self.make_request("GET", f"/books/{book_id}")

    def update_book(self, book_id, title: str):
        return self.make_request("PATCH", f"/books/{book_id}", json={"title": title})

    def delete_book(self, book_id):
        return self.make_request("DELETE", f"/books/{book_id}")

    # Search

    def get_books_by_author(self, author_id: int):
        return self.make_request("GET", "/books", params={"authorId": author_id})
