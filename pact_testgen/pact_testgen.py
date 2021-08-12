"""Main module."""
from dataclasses import dataclass, field
from typing import Any, Dict

from .models import Pact, TestCase


@dataclass
class Response:
    text: str
    headers: Dict[str, Any] = field(default_factory=dict)
    status_code: int = 200

    @classmethod
    def from_django_response(cls, response):
        return cls(
            text=response.content,
            headers=dict(response.headers),
            status_code=response.status_code
        )



def convert_to_test_cases(Pact) -> TestCase:
    """
    Given a Pact file, create TestCase representations
    according to the following:


    - One test case per provider state name.

    - Each interaction for a given provider state name
      becomes a test method.
    """
    # TODO: Implement me!
    raise NotImplementedError()
