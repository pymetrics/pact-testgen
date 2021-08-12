"""Console script for pact_testgen."""
import argparse
import json
import sys

from generators.django.generator import generate_tests
from .pact_testgen import convert_to_test_cases
from models import Pact


def load_pact_file(path: str) -> Pact:
    """ Loads the file at the supplied path into a Pact model """
    with open(path, "r") as f:
        pact = json.load(f)
        return Pact(**pact)


def run(base_class: str, pact_file: str):
    """ Loads the pact file, and writes thei generated template(s) to stdout """
    pact = load_pact_file(pact_file)
    test_file = convert_to_test_cases(pact)
    template = generate_tests(test_file)
    print(template)


def main():
    """Console script for pact_testgen."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pact_file", help="Path to a Pact file.")
    parser.add_argument(
        "--base-class",
        default="django.test.TestCase",
        help=(
            "Python path to the TestCase which generated test cases "
            "will subclass."
        ),
    )
    # Reserve -b for Pact Broker support
    args = parser.parse_args()
    try:
        run(base_class=args.base_class, pact_file=args.pact_file)
        return 0
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
