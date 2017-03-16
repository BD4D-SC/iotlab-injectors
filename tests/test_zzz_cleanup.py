import pytest

from runner import run
from test_lib import api
from test_lib import config


def test_init_config(config):
    run("registry --init")
    config.reload()


def test_unregister_parking(api):
    devices = api.get_devices({"event_type": "parking"})
    for device in devices:
        api.unregister_device(device["uuid"])


def test_unregister_superfluous_root_auth(api, config):
    devices = api.get_devices({"type": "root_auth"})
    for device in devices:
        if device["uuid"] == config.root_auth_uuid:
            continue
        api.unregister_device(device["uuid"])
