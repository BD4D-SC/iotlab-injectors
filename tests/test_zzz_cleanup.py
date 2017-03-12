import pytest

from runner import run
from test_lib import api
from test_lib import config


def test_init_config():
    run("registry --init")


def test_unregister_parking(api):
    devices = api.get_devices({"dataset": "parking"})
    for device in devices:
        api.unregister_device(device["uuid"])


def test_unregister_superfluous_root_auth(api, config):
    devices = api.get_devices({"type": "root_auth"})
    for device in devices:
        if device["uuid"] == config.root_auth_uuid:
            continue
        api.unregister_device(device["uuid"])
