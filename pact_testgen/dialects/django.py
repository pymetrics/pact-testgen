from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

from pact_testgen.models import TestCase
from pact_testgen.utils import to_camel_case, to_snake_case

from .base import BaseDialect


class Dialect(BaseDialect):
    def __init__(self):
        path = Path(__file__).parent / "templates" / "django"
        env = Environment(
            loader=FileSystemLoader(searchpath=path), autoescape=select_autoescape()
        )
        env.filters["camel_case"] = to_camel_case
        env.filters["snake_case"] = to_snake_case

        self.template_env = env

    def get_setup_function_name(self, test_case: TestCase) -> str:
        return f"setup_{to_snake_case(test_case.combined_provider_state_names)}"

    @property
    def method_template(self):
        return self.template_env.get_template("test_methods.jinja")

    @property
    def test_case_template(self):
        return self.template_env.get_template("test_case.jinja")

    @property
    def test_file_template(self):
        return self.template_env.get_template("test_file.jinja")

    @property
    def provider_state_template(self):
        return self.template_env.get_template("provider_states.jinja")
