"""Main module."""
from collections import defaultdict

from pact_testgen.models import Pact, TestCase, TestFile


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
        provider_state_names = frozenset(
            [ps.name for ps in interaction.providerStates]
        )
        provider_states_interactions[provider_state_names].append(interaction)

    cases = []

    for (
        provider_state_names,
        interactions,
    ) in provider_states_interactions.items():
        cases.append(
            TestCase(
                provider_state_names=provider_state_names,
                test_methods=interactions,
            )
        )

    return TestFile(
        base_class=base_class,
        consumer=pact.consumer,
        import_path=base_class_import_path,
        provider=pact.provider,
        test_cases=cases,
    )
