from pactman.mock.pact import Pact as PactmanPact
from pactman.verifier.result import LoggedResult, Result
from pactman.verifier.verify import ResponseVerifier

from pact_testgen.models import Response as PactResponse
from pact_testgen.utils import Response


def verify_response(
    consumer_name: str,
    provider_name: str,
    pact_response: PactResponse,
    actual_response: Response,
) -> bool:
    """
    Returns whether the actual response received from the API matches
    the contract specified in the supplied pact
    """
    pactman_pact = create_pactman_pact(consumer_name, provider_name)
    result = result_factory()
    verifier = ResponseVerifier(pactman_pact, pact_response.dict(exclude_none=True), result)
    return verifier.verify(actual_response)


def create_pactman_pact(consumer_name: str, provider_name: str) -> PactmanPact:
    """
    Creates a real Pactman Pact given the consumer and provider names
    """
    # TODO: Do we need to set any of the additional fields?
    # host_name, port, pact_dir, use_mocking_server
    consumer = {"name": consumer_name}
    provider = {"name": provider_name}
    return PactmanPact(consumer, provider)


def result_factory() -> Result:
    """
    Returns a new Pactman Result object
    """
    # TODO: Replace this with a more helpful Result subclass
    return LoggedResult()
