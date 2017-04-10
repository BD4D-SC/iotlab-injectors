import pytest


def test_package_import():
    import embers.injectors


def test_config_not_found(tmpdir, monkeypatch, config):
    monkeypatch.chdir(tmpdir)
    with pytest.raises(SystemExit):
        config.reload()


@pytest.fixture
def config():
    from embers.injectors.config import get_config
    config = get_config()
    config.root_auth_uuid = config.root_auth[0]
    config.reload = lambda: get_config(force_reload=True)
    return config


@pytest.fixture
def api():
    from embers.injectors.config import get_broker_api
    return get_broker_api()
