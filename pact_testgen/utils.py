from dataclasses import dataclass, field
from typing import Any, Dict


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
            status_code=response.status_code,
        )


def to_camel_case(value: str) -> str:
    words = []
    split_on = {" ", "_", "-"}
    word = ""
    for char in value:
        if char in split_on:
            if word:
                words.append(word.capitalize())
            word = ""
        else:
            word += char

    return "".join(words)
