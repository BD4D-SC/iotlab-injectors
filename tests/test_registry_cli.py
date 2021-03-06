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

    registered.root_auth1 = config.root_auth[0]


def test_registry_init_with_broker(config):
    run("registry --init --broker localhost")

    config.reload()
    assert config.broker_address == "localhost"

    registered.root_auth2 = config.root_auth[0]


def test_registery_list():
    ret = run("registry --list")

    assert registered.root_auth1 in ret
    assert registered.root_auth2 in ret


def test_list_and_unregister_pollution_gw():
    ret = run("registry --list")
    target = "gateway pollution"
    for line in ret.split('\n'):
        if target in line:
            uuid = line.split()[0]
            run("registry --unregister --uuid " + uuid)


def test_register_gw():
    ret = run("registry --register --gateway --events pollution")
    uuid = ret.split()[1]
    registered.uuid = uuid

    assert registered.uuid in run("registry --list")


def test_register_gw_already_registered():
    with pytest.raises(Exception):
        run("registry --register --gateway --events pollution")


def test_unregister_gw():
    run("registry --unregister --uuid " + registered.uuid)

    assert registered.uuid not in run("registry --list")


def test_register_list_unregister_device():
    ret = run("registry --register --events pollution --device")

    uuid = ret.split()[1]
    ret = run("registry --list --device")

    assert uuid in ret

    run("registry --unregister --uuid " + uuid)


def test_register_device_no_gw():
    with pytest.raises(Exception) as e:
        run("registry --register --device")

    assert "please specify --events" in e.value.output


def test_unregister_unexisting_device():
    run("registry --unregister --uuid this-device-does-not-exist")


def test_unregister_root_auths():
    run("registry --unregister --uuid " + registered.root_auth1)
    run("registry --unregister --uuid " + registered.root_auth2)
    import os
    os.remove("config.py")
