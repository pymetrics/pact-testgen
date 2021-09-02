from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, conint, Field

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Pacticipant(BaseModel):
    name: str


class Matcher(BaseModel):
    match: Literal["equality", "regex", "type"]
    max: Optional[int]
    min: Optional[int]
    regex: Optional[str]


class MatchingBodyRule(BaseModel):
    matchers: List[Matcher]


class MatchingRule(BaseModel):
    body: Dict[str, MatchingBodyRule]


class ProviderState(BaseModel):
    name: str
    params: Optional[Dict]


class Headers(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class Method(Enum):
    connect = "connect"
    CONNECT = "CONNECT"
    delete = "delete"
    DELETE = "DELETE"
    get = "get"
    GET = "GET"
    head = "head"
    HEAD = "HEAD"
    options = "options"
    OPTIONS = "OPTIONS"
    patch = "patch"
    PATCH = "PATCH"
    post = "post"
    POST = "POST"
    put = "put"
    PUT = "PUT"
    trace = "trace"
    TRACE = "TRACE"


class PactRequest(BaseModel):
    body: Optional[Any]
    headers: Optional[Headers]
    method: Method
    path: str
    query: Optional[Dict[str, List[str]]]


class PactResponse(BaseModel):
    body: Optional[Any]
    headers: Optional[Headers]
    matchingRules: Optional[MatchingRule]
    status: conint(ge=100, le=599)


class Interaction(BaseModel):
    description: str
    providerStates: List[ProviderState]
    request: PactRequest
    response: PactResponse


class PactSpecification(BaseModel):
    version: str


class Metadata(BaseModel):
    pactSpecification: Optional[PactSpecification]


class Pact(BaseModel):
    consumer: Pacticipant
    interactions: List[Interaction]
    metadata: Optional[Metadata]
    provider: Pacticipant

    @property
    def version(self):
        if self.metadata is None or self.metadata.pactSpecification is None:
            return "2.0.0"
        return self.metadata.pactSpecification.version


# Input to template function


class RequestArgs(BaseModel):
    method: str
    path: str
    data: str = ""
    content_type: str = "application/json"


class TestMethodArgs(BaseModel):
    description: str = Field(
        ..., description="Unformatted name of test method to generate"
    )
    expectation: str = Field(
        ..., description="String representation of pact expectation dictionary"
    )
    request: RequestArgs


class TestCase(BaseModel):
    provider_state_names: List[str]
    test_methods: List[TestMethodArgs]

    @property
    def combined_provider_state_names(self):
        return " ".join(self.provider_state_names)


class TestFile(BaseModel):
    pact_version: str
    base_class: str
    consumer: Pacticipant
    import_path: str
    provider: Pacticipant
    test_cases: List[TestCase]
