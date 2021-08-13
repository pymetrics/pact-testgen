import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

from pact_testgen.generators.models import RequestArgs, TestMethodArgs
from pact_testgen.models import TestFile, Interaction

path = os.path.dirname(__file__) + "/templates"
env = Environment(
    loader=FileSystemLoader(searchpath=path), autoescape=select_autoescape()
)


def generate_tests(test_file: TestFile) -> str:
    # TODO: Actually use the test_case
    method_names = ["method_1", "method_2"]
    case_name = "TestChris"
    expected_body = {"key1": "val1", "key2": {"nested_key1": "val2"}}
    args = []
    for case in test_file.test_cases:
        for method in case.test_methods:
            args.append(_build_request_args(method))
    methods = env.get_template("test_methods.jinja").render(
        method_names=method_names, expected_body=expected_body
    )
    case = env.get_template("test_case.jinja").render(
        case_name=case_name, file=test_file, methods=methods
    )

    return case


def _build_request_args(interaction: Interaction) -> TestMethodArgs:
    request_args = RequestArgs(
        method=interaction.request.method.value,
        path=interaction.request.path,
        data=json.dumps(interaction.request.body)
        if interaction.request.body
        else "",
    )

    test_method_args = TestMethodArgs(
        name=interaction.description,
        expectation=repr(interaction.response.dict()),
        request=request_args,
    )

    return test_method_args
