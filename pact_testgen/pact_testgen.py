"""Main module."""
import json
import sys
from collections import defaultdict
from pathlib import Path

from pact_testgen.dialects.base import PythonFormatter
from pact_testgen.dialects.django import Dialect
from pact_testgen.files import (
    load_pact_file,
    write_provider_state_file,
    write_test_file,
)
from pact_testgen.generator import generate_tests
from pact_testgen.models import (
    Interaction,
    Pact,
    RequestArgs,
    TestCase,
    TestFile,
    TestMethodArgs,
)


def run(
    base_class: str,
    pact_file: str,
    output_dir: Path,
    test_file_name="test_pact.py",
    provider_state_file_name="provider_states.py",
    line_length=88,
    quiet=False,
):
    """Loads the pact file, and writes the generated output files to output_dir"""
    pact = load_pact_file(pact_file)
    test_file = convert_to_test_cases(pact, base_class)
    dialect = Dialect()
    test_file, provider_state_file = generate_tests(test_file, dialect)
    format = PythonFormatter(line_length=line_length).format
    test_file_path = output_dir / test_file_name
    provider_state_file_path = output_dir / provider_state_file_name
    write_test_file(format(test_file), test_file_path)
    wrote_ps_file = write_provider_state_file(
        format(provider_state_file), provider_state_file_path
    )
    if not quiet:
        print(f"Wrote test file {test_file_path}")
        if wrote_ps_file:
            print(f"Wrote provider state file {provider_state_file_path}")
        else:
            print(
                "provider_states.py already exists, not overwriting.", file=sys.stderr
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
        # We need a hashable collection to key on, but also need to rememeber
        # name order so that test case names are deterministic based on the
        # order defined in the Pact contract.
        provider_state_key = frozenset([ps.name for ps in interaction.providerStates])
        provider_states_interactions[provider_state_key].append(interaction)

    cases = []

    for (
        _,
        interactions,
    ) in provider_states_interactions.items():
        cases.append(
            TestCase(
                # Interactions have been grouped by the set of
                # provider states, and we know there is at least
                # one interaction, so we can use the provider states
                # of the first interaction.
                provider_state_names=[ps.name for ps in interactions[0].providerStates],
                test_methods=[_build_method_args(i) for i in interactions],
            )
        )

    return TestFile(
        base_class=base_class,
        consumer=pact.consumer,
        import_path=base_class_import_path,
        provider=pact.provider,
        test_cases=cases,
        pact_version=pact.version,
    )


def _build_method_args(interaction: Interaction) -> TestMethodArgs:
    request_args = RequestArgs(
        method=interaction.request.method.value,
        path=interaction.request.path,
        data=json.dumps(interaction.request.body) if interaction.request.body else "",
    )

    test_method_args = TestMethodArgs(
        description=interaction.description,
        expectation=repr(interaction.response.dict()),
        request=request_args,
    )

    return test_method_args
