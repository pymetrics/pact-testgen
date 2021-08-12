"""Console script for pact_testgen."""
import argparse
import sys


def load_pact_file(path: str) -> str:
    # just a dumb placeholder that throws an IOError if
    # the file doesn't exist
    with open(path) as f:
        return f.read()


def run(base_class: str, pact_file: str):
    # placeholder code, obviously
    base_class_import_path, base_class = base_class.rsplit(".", 1)
    load_pact_file(pact_file)
    print(f"from {base_class_import_path} import {base_class}")
    print("from pact_testgen.verify import verify_response")
    print()
    print(f"class SomeProviderStateTests({base_class}):")
    print("    def test_some_integration(self):")
    print("        resp = self.client.get('/resource/1')")
    print("        verify_response(resp, matcher_goes_here_probably)")


def main():
    """Console script for pact_testgen."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pact_file", help="Path to a Pact file.")
    parser.add_argument(
        "--base-class",
        default="django.test.TestCase",
        help="Python path to the TestCase which generated test cases will subclass.",
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
