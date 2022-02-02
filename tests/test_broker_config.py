from pact_testgen.broker import BrokerConfig

from .utils import patch_env


DEFAULTS = {
    "base_url": "http://example.com",
    "username": "broker-username",
    "password": "broker-password",
}

# i.e. ENV_DEFAULTS = {"PACT_BROKER_BASE_URL": ...}
ENV_DEFAULTS = {f"pact_broker_{k}".upper(): v for k, v in DEFAULTS.items()}


@patch_env(ENV_DEFAULTS)
def test_set_from_env():
    config = BrokerConfig()
    assert config.base_url == DEFAULTS["base_url"]
    assert config.username == DEFAULTS["username"]
    assert config.password == DEFAULTS["password"]


@patch_env(ENV_DEFAULTS)
def test_none_init_values_defaults_to_env():
    config = BrokerConfig(base_url=None, username=None, password=None)
    assert config.base_url == DEFAULTS["base_url"]
    assert config.username == DEFAULTS["username"]
    assert config.password == DEFAULTS["password"]


@patch_env(ENV_DEFAULTS)
def test_init_values_override_env():
    values = {
        "base_url": "http://example.com:8000",
        "username": "new-username",
        "password": "new-password",
    }
    config = BrokerConfig(**values)
    assert config.base_url == values["base_url"]
    assert config.username == values["username"]
    assert config.password == values["password"]


@patch_env()
def test_auth_tuple_no_creds():
    config = BrokerConfig(base_url="http://example.com")
    assert config.auth_tuple is None


@patch_env()
def test_auth_tuple_with_creds():
    config = BrokerConfig(**DEFAULTS)
    assert config.auth_tuple == (DEFAULTS["username"], DEFAULTS["password"])
