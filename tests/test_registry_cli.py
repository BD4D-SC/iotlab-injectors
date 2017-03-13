import pytest

from runner import run
from test_lib import config

class registered: pass  # a global namespace for this test


def test_registry_no_args():
    run("registry")


def test_registry_init():
    run("registry --init")


def test_registry_init_result(config):
    config.reload()
    assert config.broker_address
    assert config.root_auth

    registered.root_auth1 = config.root_auth


def test_registry_init_with_broker(config):
    run("registry --init --broker localhost")

    config.reload()
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


def test_unregister_root_auths():
    run("registry --unregister --uuid " + registered.root_auth1[0])
    run("registry --unregister --uuid " + registered.root_auth2[0])
    import os
    os.remove("config.py")
