import pytest

from runner import run
from embers.injectors.config import get_config

class registered: pass  # a global namespace for this test


def test_registry_no_args():
    run("registry")


def test_registry_init():
    run("registry --init")


def test_get_config():
    config = get_config()
    assert config.broker_address
    assert config.root_auth

    registered.root_auth1 = config.root_auth


def test_registry_init_with_broker():
    run("registry --init --broker localhost")


def test_get_config_reload():
    config = get_config(force_reload=True)
    assert config.broker_address == "localhost"

    registered.root_auth2 = config.root_auth


def test_register_gw():
    ret = run("registry --register --gateway traffic")
    uuid = ret.split()[1]
    registered.uuid = uuid


def test_register_gw_already_registered():
    with pytest.raises(Exception):
        run("registry --register --gateway traffic")


def test_unregister_gw():
    run("registry --unregister --uuid " + registered.uuid)


def test_cleanup():
    run("registry --unregister --uuid " + registered.root_auth1[0])
    run("registry --unregister --uuid " + registered.root_auth2[0])
    import os
    os.remove("config.py")
