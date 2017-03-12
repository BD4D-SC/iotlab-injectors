import pytest


def test_package_import():
    import embers.injectors


@pytest.fixture
def config():
    from embers.injectors.config import get_config
    config = get_config(force_reload=True)
    config.root_auth_uuid = config.root_auth[0]
    return config


@pytest.fixture
def api():
    from embers.injectors.config import get_broker_api
    return get_broker_api()
