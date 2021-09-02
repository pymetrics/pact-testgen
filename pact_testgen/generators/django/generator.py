from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Tuple
from pathlib import Path

from pact_testgen.models import TestFile
from pact_testgen.utils import to_camel_case, to_snake_case

path = Path(__file__).parent / "templates"
env = Environment(
    loader=FileSystemLoader(searchpath=path), autoescape=select_autoescape()
)
env.filters["camel_case"] = to_camel_case
env.filters["snake_case"] = to_snake_case


def generate_tests(test_file: TestFile) -> Tuple[str, str]:
    cases = []
    provider_state_setup_functions = []
    consumer_name = test_file.consumer.name
    provider_name = test_file.provider.name

    for test_case in test_file.test_cases:

        methods = env.get_template("test_methods.jinja").render(
            methods=test_case.test_methods,
            consumer_name=consumer_name,
            provider_name=provider_name,
            pact_version=test_file.pact_version,
        )

        assert methods

        setup_function_name = (
            f"setup_{to_snake_case(test_case.combined_provider_state_names)}"
        )

        case = env.get_template("test_case.jinja").render(
            ps_names=test_case.combined_provider_state_names,
            file=test_file,
            methods=methods,
            setup_function_name=setup_function_name,
        )
        cases.append(case)
        provider_state_setup_functions.append(
            {
                "method_name": setup_function_name,
                "provider_states": test_case.provider_state_names,
            }
        )

    all_tests = env.get_template("test_file.jinja").render(
        file=test_file, cases=cases, setup_functions=provider_state_setup_functions
    )

    provider_states = env.get_template("provider_states.jinja").render(
        setup_functions=provider_state_setup_functions
    )
    return all_tests, provider_states
