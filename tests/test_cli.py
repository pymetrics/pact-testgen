import pytest
from pact_testgen import cli
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from argparse import Namespace
from .utils import patch_env


@pytest.fixture
def parser():
    return cli._build_parser()


@pytest.fixture
def filename():
    """Yields a file name which is guaranteed to exist"""
    with NamedTemporaryFile() as f:
        yield f.name


@pytest.fixture
def dir():
    """Yields a temporary directory as a Path object"""
    with TemporaryDirectory() as d:
        yield Path(d)


class ErrorCallable:
    """
    Callable which can be called once, subsequent calls are ignored.
    Remembers what it was called with.
    Mimics the behavior
    of ArgumentParser.error, and is intended
    to be passed to `cli.validate_namespace`.
    """

    def __init__(self):
        self.message = None
        self.was_called = False

    def __call__(self, message: str):
        if not self.was_called:
            self.message = message
            self.was_called = True


@pytest.fixture
def error() -> ErrorCallable:
    return ErrorCallable()


@pytest.fixture
def namespace_pactfile(filename, dir) -> Namespace:
    """
    Returns a default Namespace that should pass validation,
    for the Pact file use case.
    """
    return Namespace(
        pact_file=filename,
        output_dir=dir,
        base_class="django.test.TestCase",
        line_length=88,
        debug=False,
        quiet=False,
        merge_provider_state_file=False,
        broker_base_url=None,
        broker_username=None,
        broker_password=None,
        consumer_name=None,
        provider_name=None,
        consumer_version=None,
    )


@pytest.fixture
def namespace_broker(filename, dir) -> Namespace:
    """
    Returns a default Namespace that should pass validation,
    for the Pact Broker use case.
    """
    return Namespace(
        pact_file=None,
        output_dir=dir,
        base_class="django.test.TestCase",
        line_length=88,
        debug=False,
        quiet=False,
        merge_provider_state_file=False,
        broker_base_url="http://localhost",
        broker_username="username",
        broker_password="password",
        consumer_name="TestConsumer",
        provider_name="TestProvider",
        consumer_version=None,
    )


ENV_DEFAULTS = {
    "PACT_BROKER_BASE_URL": "http://localhost:9292",
    "PACT_BROKER_USERNAME": "username",
    "PACT_BROKER_PASSWORD": "password",
    "PACT_BROKER_PROVIDER_NAME": "TestProvider",
    "PACT_BROKER_CONSUMER_NAME": "TestConsumer",
    "PACT_BROKER_CONSUMER_VERSION": "1.0.0",
}


@patch_env(ENV_DEFAULTS)
def test_get_env_namespace():
    ns = cli.get_env_namespace()
    assert ns.broker_base_url == ENV_DEFAULTS["PACT_BROKER_BASE_URL"]
    assert ns.broker_username == ENV_DEFAULTS["PACT_BROKER_USERNAME"]
    assert ns.broker_password == ENV_DEFAULTS["PACT_BROKER_PASSWORD"]
    assert ns.consumer_name == ENV_DEFAULTS["PACT_BROKER_CONSUMER_NAME"]
    assert ns.provider_name == ENV_DEFAULTS["PACT_BROKER_PROVIDER_NAME"]
    assert ns.consumer_version == ENV_DEFAULTS["PACT_BROKER_CONSUMER_VERSION"]


def test_parser_defaults(parser, dir, filename):
    args = [str(dir), "-f", filename]

    ns = parser.parse_args(args)

    # ns.output_dir will be a Path object
    assert ns.output_dir == dir
    assert ns.pact_file == filename
    assert ns.base_class == "django.test.TestCase"
    assert ns.line_length == 88
    assert ns.quiet is False
    assert ns.merge_provider_state_file is False


def test_with_consumer_name_missing_provider_name(
    error: ErrorCallable, namespace_broker: Namespace
):
    namespace_broker.provider_name = None
    cli.validate_namespace(namespace_broker, error)
    assert error.was_called
    assert error.message == cli.ErrorMessage.MISSING_PROVIDER_OR_CONSUMER


def test_with_provider_name_missing_consumer_name(
    error: ErrorCallable, namespace_broker: Namespace
):
    namespace_broker.consumer_name = None
    cli.validate_namespace(namespace_broker, error)
    assert error.was_called

    assert error.message == cli.ErrorMessage.MISSING_PROVIDER_OR_CONSUMER


def test_require_consumer_name_when_given_broker_url(
    error: ErrorCallable, namespace_broker
):
    namespace_broker.consumer_name = None
    namespace_broker.provider_name = None
    cli.validate_namespace(namespace_broker, error)

    assert error.was_called
    assert error.message == cli.ErrorMessage.MISSING_PACTICIPANT


def test_require_provider_name_when_given_broker_url(
    error: ErrorCallable, namespace_broker
):
    namespace_broker.provider_name = None
    namespace_broker.consumer_name = None
    cli.validate_namespace(namespace_broker, error)

    assert error.was_called
    assert error.message == cli.ErrorMessage.MISSING_PACTICIPANT


def test_indeterminate_pactfile_source(
    error: ErrorCallable, filename: str, namespace_broker: Namespace
):
    namespace_broker.pact_file = Path(filename)
    cli.validate_namespace(namespace_broker, error)
    assert error.was_called
    assert error.message == cli.ErrorMessage.INDETERMINATE_SOURCE


def test_build_run_options_pactfile(namespace_pactfile):
    opts = cli.build_run_options(namespace_pactfile)
    assert opts.pact_file
    assert opts.broker_config is None


def test_build_run_options_broker(namespace_broker):
    opts = cli.build_run_options(namespace_broker)
    assert opts.broker_config is not None
    assert isinstance(opts.broker_config, cli.BrokerConfig)
