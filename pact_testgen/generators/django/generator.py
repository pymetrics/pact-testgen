import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from slugify import slugify

from pact_testgen.generators.models import RequestArgs, TestMethodArgs
from pact_testgen.models import Interaction, TestCase, TestFile

path = os.path.dirname(__file__) + "/templates"
env = Environment(
    loader=FileSystemLoader(searchpath=path), autoescape=select_autoescape()
)


def generate_tests(test_file: TestFile) -> str:
    cases = []
    consumer_name = test_file.consumer.name
    provider_name = test_file.provider.name

    for test_case in test_file.test_cases:
        args = []
        case_name = _get_test_class_name(test_case)

        for method in test_case.test_methods:
            args.append(_build_method_args(method))

        methods = env.get_template("test_methods.jinja").render(
            args=args, consumer_name=consumer_name, provider_name=provider_name
        )
        case = env.get_template("test_case.jinja").render(
            case_name=case_name, file=test_file, methods=methods
        )
        cases.append(case)

    all_tests = env.get_template("test_file.jinja").render(
        file=test_file, cases=cases
    )
    return all_tests


def _build_method_args(interaction: Interaction) -> TestMethodArgs:
    request_args = RequestArgs(
        method=interaction.request.method.value,
        path=interaction.request.path,
        data=json.dumps(interaction.request.body)
        if interaction.request.body
        else "",
    )

    test_method_args = TestMethodArgs(
        name=_get_test_method_name(interaction),
        expectation=repr(interaction.response.dict()),
        request=request_args,
    )

    return test_method_args


def _get_test_class_name(test_case: TestCase) -> str:
    provider_slugs = [
        slugify(x).replace("-", "_") for x in test_case.provider_state_names
    ]
    return "Test_{}".format("_".join(provider_slugs))


def _get_test_method_name(interaction: Interaction) -> str:
    description_slug = slugify(interaction.description).replace("-", "_")
    return "test_{}".format(description_slug)
