import json
from pathlib import Path
from typing import Any, Dict

import pytest

from pact_testgen.models import Pact

PROJECT_ROOT = Path(__file__).parent.parent.absolute()


@pytest.fixture
def pactfile() -> str:
    """
    A sample Pact file as a string.
    """
    with open(
        PROJECT_ROOT
        / "test_app"
        / "pactfiles"
        / "LibraryClient-Library-pact.json",
        "r",
    ) as f:
        return f.read()


@pytest.fixture
def pactfile_dict(pactfile) -> Dict[str, Any]:
    """
    A sample Pact file, parsed to a Python dict.
    """
    return json.loads(pactfile)


@pytest.fixture
def pact(pactfile) -> Pact:
    """
    A sample Pact file, as a Pact object.
    """
    return Pact.parse_raw(pactfile)
