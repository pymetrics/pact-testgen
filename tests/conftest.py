import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.absolute()


@pytest.fixture
def pactfile() -> str:
    with open(
        PROJECT_ROOT
        / "pact_samples"
        / "ApplicationServiceClient-ApplicationService-pact.json",
        "r",
    ) as f:
        return f.read()
