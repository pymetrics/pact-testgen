"""Console script for pact_testgen."""
import argparse
import os
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional

from pact_testgen import __version__
from pact_testgen.broker import BrokerBasicAuthConfig, BrokerConfig
from pact_testgen.files import merge_is_available
from pact_testgen.pact_testgen import RunOptions, run


def directory(path: str) -> Path:
    path = Path(path)
    if path.is_dir():
        return path
    raise argparse.ArgumentError()


ENV_MAP = {
    # CLI store name -> env var name
    "broker_base_url": "PACT_BROKER_BASE_URL",
    "broker_username": "PACT_BROKER_USERNAME",
    "broker_password": "PACT_BROKER_PASSWORD",
    "consumer_name": "PACT_BROKER_CONSUMER_NAME",
    "provider_name": "PACT_BROKER_PROVIDER_NAME",
    "consumer_version": "PACT_BROKER_CONSUMER_VERSION",
}


class ErrorMessage:
    MISSING_PROVIDER_OR_CONSUMER = (
        "Must specify both --provider-name and --consumer-name, or neither."
    )
    MISSING_PACTICIPANT = (
        "Must specify consumer and provider names with pact broker URL."
    )
    INDETERMINATE_SOURCE = "Specify either pact file or pact broker options, not both."
    MISSING_SOURCE = "Must provide a pact file with -f, or pact broker options."
    MISSING_CONSUMER_NAME = "Must specify consumer name with consumer version."
    MERGE_NOT_AVAILABLE = "Merge provider state file is only available in Python 3.9+."


def get_env_namespace(mapping: Dict[str, str] = ENV_MAP) -> argparse.Namespace:
    """
    Create a Namespace populated from environment variables.
    Takes a mapping of namespace store names -> env var names.
    """
    ns_kwargs = {}
    for store_name, env_var in mapping.items():
        value = os.environ.get(env_var)
        if value is not None:
            ns_kwargs[store_name] = value
    return argparse.Namespace(**ns_kwargs)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_dir", help="Output for generated Python files.", type=directory
    )
    parser.add_argument("-f", "--pact-file", help="Path to a Pact file.")
    parser.add_argument(
        "--base-class",
        default="django.test.TestCase",
        help=("Python path to the TestCase which generated test cases will subclass."),
    )
    parser.add_argument(
        "--line-length",
        type=int,
        default=88,
        help="Target line length for generated files.",
    )
    parser.add_argument("--debug", action="store_true")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s v{version}".format(version=__version__),
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Silence output")
    parser.add_argument(
        "-m",
        "--merge-provider-state-file",
        action="store_true",
        help="Attempt to merge new provider state functions into existing "
        "provider state file. Only available on Python 3.9+.",
    )
    # Options related to pact broker are the same as those for the pact broker CLI
    # client, as much as possible
    # https://github.com/pact-foundation/pact_broker-client#usage---cli

    broker_group = parser.add_argument_group("pact broker arguments")

    broker_group.add_argument(
        "-b",
        "--broker-base-url",
        help="Pact broker base url. Optionally configure by setting the "
        "PACT_BROKER_BASE_URL environment variable.",
    )
    broker_group.add_argument("-u", "--broker-username", help="Pact broker username.")
    broker_group.add_argument("-p", "--broker-password", help="Pact broker password.")
    broker_group.add_argument(
        "-c",
        "--consumer-name",
        help="Consumer name used to retrieve Pact contract from the pact broker.",
    )
    broker_group.add_argument(
        "-s",
        "--provider-name",
        help="Provider name used to retrieve Pact contract from the pact broker.",
    )
    broker_group.add_argument(
        "-v",
        "--consumer-version",
        # Note we don't actually set default="latest" here, that happens
        # later when constructing the URL. Here, we rely on consumer_version=None
        # if it isn't specified.
        help="Consumer version number. Used to retrieve the Pact contract from the "
        "Pact broker. Optional, defaults to 'latest'.",
    )
    return parser


def validate_namespace(args: argparse.Namespace, error_func: Callable[[str], None]):

    # Either both, or neither, i.e. logical XNOR
    if bool(args.consumer_name) ^ bool(args.provider_name):
        error_func(ErrorMessage.MISSING_PROVIDER_OR_CONSUMER)

    if args.broker_base_url and not args.consumer_name:
        error_func(ErrorMessage.MISSING_PACTICIPANT)

    if args.pact_file and args.consumer_name:
        error_func(ErrorMessage.INDETERMINATE_SOURCE)

    if not (args.pact_file or args.consumer_name):
        error_func(ErrorMessage.MISSING_SOURCE)

    if args.consumer_version and not args.consumer_name:
        error_func(ErrorMessage.MISSING_CONSUMER_NAME)

    if args.merge_provider_state_file and not merge_is_available():
        error_func(ErrorMessage.MERGE_NOT_AVAILABLE)


def run_options_from_namespace(args: argparse.Namespace) -> RunOptions:
    if args.consumer_name:
        if args.broker_username and args.broker_password:
            auth = BrokerBasicAuthConfig(
                username=args.broker_username,
                password=args.broker_password,
            )
        else:
            auth = None
        broker_config = BrokerConfig(base_url=args.broker_base_url, auth=auth)
    else:
        broker_config = None

    return RunOptions(
        base_class=args.base_class,
        pact_file=args.pact_file,
        broker_config=broker_config,
        provider_name=args.provider_name,
        consumer_name=args.consumer_name,
        consumer_version=args.consumer_version,
        output_dir=args.output_dir,
        line_length=args.line_length,
        merge_ps_file=args.merge_provider_state_file,
    )


def build_run_options(args: Optional[List[str]] = None) -> RunOptions:
    # Pass args in for testing purposes, leave none to parse args
    # provided at CLI.
    parser = _build_parser()
    # Parse CLI args, adding or overriding to a Namespace created from env vars.
    ns = parser.parse_args(args=args, namespace=get_env_namespace())
    validate_namespace(ns, error_func=parser.error)
    return run_options_from_namespace(ns)


def main():
    """Console script for pact_testgen."""
    opts = None
    try:
        opts = build_run_options()
        run(opts)
        return 0
    except Exception as e:
        if not opts or opts.debug:
            raise
        print(f"An error occurred: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
