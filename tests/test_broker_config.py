from pact_testgen.broker import BrokerConfig


AUTH = {
    "username": "broker-username",
    "password": "broker-password",
}
DEFAULTS = {
    "base_url": "http://example.com",
    "auth": AUTH,
}


def test_auth_tuple_no_creds():
    config = BrokerConfig(base_url="http://example.com")
    assert config.auth_tuple is None


def test_auth_tuple_with_creds():
    config = BrokerConfig(**DEFAULTS)
    assert config.auth_tuple == (AUTH["username"], AUTH["password"])
