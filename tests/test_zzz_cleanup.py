import pytest

from runner import run


def test_check_init_needed():
    try:
       run("registry --list")
    except:
       run("registry --init")


def test_unregister_superfluous_root_auth(config):
    ret = run("registry --list")
    for line in ret.split('\n'):
        if "root_auth" not in line:
            continue
        uuid = line.split()[0]
        if uuid == config.root_auth_uuid:
            continue
        run("registry --unregister --uuid " + uuid)


@pytest.fixture
def config():
    from embers.injectors.config import get_config
    config = get_config(force_reload=True)
    config.root_auth_uuid = config.root_auth[0]
    return config
