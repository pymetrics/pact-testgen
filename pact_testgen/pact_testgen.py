"""Main module."""
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict

from .models import Pact, TestFile, TestCase


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


def convert_to_test_cases(pact: Pact, base_class: str) -> TestFile:
    """
    Given a Pact file, create TestFile representations
    according to the following:


    - One test case per provider state name.

    - Each interaction for a given provider state name
      becomes a test method.
    """
    base_class_import_path, base_class = base_class.rsplit(".", 1)

    provider_states_interactions = defaultdict(list)

    for interaction in pact.interactions:
        provider_state_names = frozenset([ps.name for ps in interaction.providerStates])
        provider_states_interactions[provider_state_names].append(interaction)

    cases = []

    for provider_state_names, interactions in provider_states_interactions.items():
        cases.append(
            TestCase(provider_state_names=provider_state_names, test_methods=interactions)
        )

    return TestFile(
        base_class=base_class, import_path=base_class_import_path, test_cases=cases
    )


def verify_pact(pact_response, actual_response):
    # TODO:
    raise NotImplementedError()
