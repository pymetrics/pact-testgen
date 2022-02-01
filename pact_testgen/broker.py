import urllib
from typing import Optional, Tuple

import requests
from pydantic import BaseSettings, Field
from .models import Pact


class BrokerConfig(BaseSettings):
    # Same env vars as pact broker CLI client
    # https://github.com/pact-foundation/pact_broker-client#usage---cli
    base_url: str
    username: str = Field(default="")
    password: str = Field(default="")

    class Config:
        env_prefix = "pact_broker_"

    @property
    def auth_tuple(self) -> Optional[Tuple[str, str]]:
        """
        Returns auth value suitable for passing to requests.

        If username or password are present, will be Tuple[str,str],
        else None.
        """
        if self.username or self.password:
            return (self.username, self.password)
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
    resp = requests.get(url, auth=broker_config.auth_tuple)
    resp.raise_for_status()
    return Pact(**resp.json())
