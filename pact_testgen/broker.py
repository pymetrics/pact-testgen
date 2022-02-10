import urllib
from typing import Dict, Optional, Tuple

import requests
from pydantic import BaseModel

from .models import Pact


class BrokerBasicAuthConfig(BaseModel):
    username: str
    password: str


class BrokerConfig(BaseModel):
    # Same env vars as pact broker CLI client
    # https://github.com/pact-foundation/pact_broker-client#usage---cli
    base_url: str
    auth: Optional[BrokerBasicAuthConfig]

    @property
    def auth_tuple(self) -> Optional[Tuple[str, str]]:
        """
        Returns auth value suitable for passing to requests.

        If username or password are present, will be Tuple[str,str],
        else None.
        """
        if self.auth:
            return (self.auth.username, self.auth.password)
        return None


def _build_contract_url(
    base_url: str, provider_name: str, consumer_name: str, version=None
) -> str:
    if version is None or version == "latest":
        version = "latest"
    else:
        version = f"version/{version}"

    path = urllib.parse.quote(
        f"/pacts/provider/{provider_name}/consumer/{consumer_name}/{version}"
    )
    return urllib.parse.urljoin(base_url, path)


def _make_broker_request(url: str, auth: Optional[Tuple[str, str]] = None) -> Dict:
    resp = requests.get(url, auth=auth)
    resp.raise_for_status()
    return resp.json()


def get_pact_from_broker(
    broker_config: BrokerConfig,
    provider_name: str,
    consumer_name: str,
    version=None,
) -> Pact:
    """
    Make an HTTP request to the Pact Broker to retrieve the desired contract.
    """
    url = _build_contract_url(
        broker_config.base_url, provider_name, consumer_name, version=version
    )
    data = _make_broker_request(url, auth=broker_config.auth_tuple)
    return Pact(**data)


def _remove_items_with_value_none(d: dict) -> Dict:
    return {k: v for k, v in d.items() if v is not None}
