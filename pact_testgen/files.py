import json
from pathlib import Path

from pact_testgen.models import Pact


def load_pact_file(path: str) -> Pact:
    """Loads the file at the supplied path into a Pact model"""
    with open(Path(path), "r") as f:
        pact = json.load(f)
        return Pact(**pact)
