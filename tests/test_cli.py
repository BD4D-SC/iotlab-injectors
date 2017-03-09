import pytest

from runner import run


def test_injectors_no_args():
    run("injectors")


def test_injectors_init_config():
    run("injectors --init-config")
    from embers.injectors.config import get_config
    config = get_config()
    assert config.broker_address
    assert config.root_auth


def test_injectors_init_config_with_broker():
    run("injectors --init-config --broker localhost")
    from embers.injectors.config import get_config
    config = get_config(force_reload=True)
    assert config.broker_address == "localhost"


def test_injectors_run_defaults():
    run("injectors --run")


PROTOCOLS = "http mqtt coap"
@pytest.mark.parametrize("protocol", PROTOCOLS.split())
def test_injectors_run_protocol(protocol):
    run("injectors --run --protocol " + protocol)


def test_injectors_run_many_parking():
    run("injectors --run --nb-devices 50 --dataset parking")
