import pytest

from runner import run


def test_registry_no_args():
    run("registry")


def test_registry_init():
    run("registry --init")

    from embers.injectors.config import get_config
    config = get_config()
    assert config.broker_address
    assert config.root_auth


def test_registry_init_with_broker():
    run("registry --init --broker localhost")

    from embers.injectors.config import get_config
    config = get_config(force_reload=True)
    assert config.broker_address == "localhost"


class registered: pass  # a global namespace

def test_register_gw():
    ret = run("registry --register --gateway traffic")
    uuid = ret.split()[1]
    registered.uuid = uuid


def test_register_gw_already_registered():
    with pytest.raises(Exception):
        run("registry --register --gateway traffic")


def test_unregister():
    run("registry --unregister --uuid {}".format(registered.uuid))
