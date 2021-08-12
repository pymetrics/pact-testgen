from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, Field, conint, constr


class Headers(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class Interaction(BaseModel):
    description: str
    matchingRules: Optional[List[MatchingRule]]
    providerStates: List[ProviderState]
    request: Request
    response: Response


class Match(Enum):
    regex = "regex"
    type = "type"


class Matcher(BaseModel):
    match: Match
    max: Optional[int]
    min: Optional[int]
    regex: Optional[str]


class MatchingBodyRule(BaseModel):
    matchers: List[Matcher]


class MatchingRule(BaseModel):
    body: Dict[str, MatchingBodyRule]


class Metadata(BaseModel):
    pactSpecification: Optional[PactSpecification]


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
    post = "post"
    POST = "POST"
    put = "put"
    PUT = "PUT"
    trace = "trace"
    TRACE = "TRACE"


class Pact(BaseModel):
    consumer: Pacticipant
    interactions: List[Interaction]
    metadata: Optional[Metadata]
    provider: Pacticipant


class Pacticipant(BaseModel):
    name: str


class PactSpecification(BaseModel):
    version: str


class ProviderState(BaseModel):
    name: str
    params: Optional[Dict]


class Request(BaseModel):
    body: Optional[Any]
    headers: Optional[Headers]
    method: Method
    path: str
    query: Optional[
        constr(regex=r"^$|^[^=&]+=[^=&]+&?$|^[^=&]+=[^=&]+(&[^=&]+=[^=&]+)*&?$")
    ] = None


class Response(BaseModel):
    body: Optional[Any]
    headers: Optional[Headers]
    status: conint(ge=100, le=599)
