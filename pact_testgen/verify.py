from pactman.mock.pact import Pact as PactmanPact
from pactman.verifer.result import LoggedResult, Result
from pactman.verifier.verify import ResponseVerifier

from .models import (
    Pact,
    PactResponse,
)
from .utils import Response


def verify_response(
    pact: Pact,
    pact_response: PactResponse,
    actual_response: Response,
) -> bool:
    """
    Returns whether the actual response received from the API matches
    the contract specified in the supplied pact
    """
    pactman_pact = create_pactmanpact_from_pact(pact)
    result = result_factory()
    verifier = ResponseVerifier(pactman_pact, pact_response, result)
    return verifier.verify(actual_response)


def create_pactmanpact_from_pact(pact: Pact) -> PactmanPact:
    """
    Creates a real Pactman Pact out of a Pact pydantic model
    """
    # TODO: Do we need to set any of the additional fields?
    # host_name, port, pact_dir, use_mocking_server
    return PactmanPact(
        pact["consumer"],
        pact["provider"],
    )


def result_factory() -> Result:
    """
    Returns a new Pactman Result object
    """
    # TODO: Replace this with a more helpful Result subclass
    return LoggedResult()
