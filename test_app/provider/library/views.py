import json
from typing import Any, Dict, List, Type, Union

from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from library.models import Author, Book
from pydantic import BaseModel, ValidationError

ParsedJSON = Union[List, Dict[str, Any]]


class AuthorCreateUpdateRequest(BaseModel):
    name: str
    is_featured: bool


class AuthorSerializer(BaseModel):
    id: int
    name: str
    is_featured: bool


class BookSerializer(BaseModel):
    id: int
    title: str


def to_pydantic_model(model: Type[BaseModel], request: HttpRequest):
    return model.parse_raw(request.body)


@csrf_exempt
def create_author(request):
    if request.method == "POST":
        author_request = to_pydantic_model(AuthorCreateUpdateRequest, request)
        author = Author.objects.create(
            name=author_request.name, is_featured=author_request.is_featured
        )
        return JsonResponse(
            AuthorSerializer(
                id=author.id, name=author.name, is_featured=author.is_featured
            ).dict(),
            status=201,
        )
    return HttpResponseNotAllowed(permitted_methods=["POST"])


@csrf_exempt
def get_or_update_author(request, author_id):
    if request.method == "PATCH" or request.method == "POST":
        update_request = to_pydantic_model(AuthorCreateUpdateRequest, request)
        author = get_object_or_404(Author, id=author_id)
        author.name = update_request.name
        author.is_featured = update_request.is_featured
        author.save()
        return JsonResponse(
            AuthorSerializer(
                id=author.id, name=author.name, is_featured=author.is_featured
            ).dict()
        )
    elif request.method == "DELETE":
        author = get_object_or_404(Author, id=author_id)
        author.delete()
        return HttpResponse(status=204)
    elif request.method == "GET":
        author = get_object_or_404(Author, id=author_id)
        return JsonResponse(
            AuthorSerializer(
                id=author.id, name=author.name, is_featured=author.is_featured
            ).dict()
        )

    return HttpResponseNotAllowed(permitted_methods=["PATCH", "DELETE"])


def search_books(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=["GET"])

    books = Book.objects.all()
    if "authorId" in request.GET:
        author_id = int(request.GET["authorId"])
        books = books.filter(author_id=author_id)

    return JsonResponse(
        [BookSerializer(title=book.title, id=book.id).dict() for book in books],
        safe=False,
    )
