from abc import ABC, abstractmethod, abstractproperty
from pact_testgen.models import TestCase


class BaseDialect(ABC):
    @abstractmethod
    def get_setup_function_name(self, test_case: TestCase):
        ...

    @abstractproperty
    def method_template(self):
        ...

    @abstractproperty
    def test_case_template(self):
        ...

    @abstractproperty
    def test_file_template(self):
        ...

    @abstractproperty
    def provider_state_template(self):
        ...
