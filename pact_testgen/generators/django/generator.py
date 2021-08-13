import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import TestFile


path = os.path.dirname(__file__) + "/templates"
print(path)
env = Environment(
    loader=FileSystemLoader(searchpath=path), autoescape=select_autoescape()
)


def generate_tests(test_file: TestFile) -> str:
    # TODO: Actually use the test_case
    method_names = ["method_1", "method_2"]
    case_name = "TestChris"
    methods = env.get_template("test_methods.jinja").render(method_names=method_names)
    case = env.get_template("test_case.jinja").render(
        case_name=case_name, methods=methods
    )

    return case
