import pytest

from runner import run


def test_injectors_no_args():
    run("injectors")


def test_injectors_run_defaults():
    run("injectors --run")


PROTOCOLS = "http mqtt coap"
@pytest.mark.parametrize("protocol", PROTOCOLS.split())
def test_injectors_run_protocol(protocol):
    run("injectors --run --protocol " + protocol)


def test_injectors_run_many_parking():
    run("injectors --run --nb-devices 50 --dataset parking")
