"""Console script for pact_testgen."""
import argparse
import sys
from pathlib import Path
from pact_testgen import __version__
from pact_testgen.pact_testgen import run
from pact_testgen.files import merge_is_available


def directory(path: str) -> Path:
    path = Path(path)
    if path.is_dir():
        return path
    raise argparse.ArgumentError()


def main():
    """Console script for pact_testgen."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pact_file", help="Path to a Pact file.")
    parser.add_argument(
        "output_dir", help="Output for generated Python files.", type=directory
    )
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
    # Reserve -b for Pact Broker support
    args = parser.parse_args()

    if args.merge_provider_state_file and not merge_is_available():
        print(
            "Merge provider state file is only available in Python 3.9+.",
            file=sys.stderr,
        )
        return 1

    try:
        run(
            base_class=args.base_class,
            pact_file=args.pact_file,
            output_dir=args.output_dir,
            line_length=args.line_length,
            merge_ps_file=args.merge_provider_state_file,
        )
        return 0
    except Exception as e:
        if args.debug:
            raise
        print(f"An error occurred: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
