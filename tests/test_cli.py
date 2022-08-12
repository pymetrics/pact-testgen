from argparse import Namespace
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from pact_testgen import cli

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
def dir() -> str:
    """Yields a temporary directory as a str"""
    with TemporaryDirectory() as d:
        yield str(Path(d))


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
def namespace_pactfile(parser, filename, dir) -> Namespace:
    """
    Return a namespace created with args for the pact file use case"""
    return parser.parse_args([str(dir), "--pact-file", filename])


@pytest.fixture
def namespace_broker(parser, dir) -> Namespace:
    """
    Returns a default Namespace that should pass validation,
    for the Pact Broker use case.
    """
    return parser.parse_args(
        [
            dir,
            # fmt: off
            "--broker-base-url", "http://localhost",
            "--broker-username", "username",
            "--broker-password", "password",
            "--consumer-name", "TestConsumer",
            "--provider-name", "TestProvider",
            # fmt: on
        ]
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
    args = [dir, "-f", filename]

    ns = parser.parse_args(args)

    # ns.output_dir will be a Path object
    assert ns.output_dir == Path(dir)
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


def test_run_options_from_namespace_pactfile(namespace_pactfile):
    opts = cli.run_options_from_namespace(namespace_pactfile)
    assert opts.pact_file
    assert opts.broker_config is None


def test_run_options_from_namespace_broker(namespace_broker):
    opts = cli.run_options_from_namespace(namespace_broker)
    assert opts.broker_config is not None
    assert isinstance(opts.broker_config, cli.BrokerConfig)


@patch_env()
def test_get_env_namespace_does_not_contain_unset_values():
    ns = cli.get_env_namespace()
    assert ns == Namespace()


@patch_env({"PACT_BROKER_BASE_URL": ENV_DEFAULTS["PACT_BROKER_BASE_URL"]})
def test_broker_base_url_as_env_var(dir):
    args = [dir, "-s", "TestProvider", "-c", "TestConsumer"]
    opts = cli.build_run_options(args=args)
    assert opts.broker_config is not None
    assert opts.broker_config.base_url == ENV_DEFAULTS["PACT_BROKER_BASE_URL"]
    assert opts.consumer_name == "TestConsumer"
    assert opts.provider_name == "TestProvider"


@patch_env({"PACT_BROKER_BASE_URL": "http://from-env"})
def test_cli_args_override_env_vars(dir):
    args = [
        dir,
        "-b",
        ENV_DEFAULTS["PACT_BROKER_BASE_URL"],
        "-s",
        "TestProvider",
        "-c",
        "TestConsumer",
    ]
    opts = cli.build_run_options(args=args)
    assert opts.broker_config is not None
    assert opts.broker_config.base_url == ENV_DEFAULTS["PACT_BROKER_BASE_URL"]
