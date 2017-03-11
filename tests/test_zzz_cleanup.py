import pytest

from runner import run
from test_lib import config


def test_init_config():
    run("registry --init")


def test_unregister_parking():
    ret = run("registry --list")
    for line in ret.split('\n'):
        if "parking" not in line:
            continue
        uuid = line.split()[0]
        run("registry --unregister --uuid " + uuid)


def test_unregister_superfluous_root_auth(config):
    ret = run("registry --list")
    for line in ret.split('\n'):
        if "root_auth" not in line:
            continue
        uuid = line.split()[0]
        if uuid == config.root_auth_uuid:
            continue
        run("registry --unregister --uuid " + uuid)
