import pytest

from runner import run


def test_injectors_no_args():
    run("injectors")


def test_injectors_init_config():
    run("injectors --init-config")


def test_injectors_run_defaults():
    run("injectors --run")


PROTOCOLS = "http mqtt coap"
@pytest.mark.parametrize("protocol", PROTOCOLS.split())
def test_injectors_run_protocol(protocol):
    run("injectors --run --protocol " + protocol)


def test_injectors_run_many_parking():
    run("injectors --run --nb-devices 50 --events parking")


def test_injectors_no_config_no_init(tmpdir, monkeypatch):
    monkeypatch.chdir(tmpdir)
    with pytest.raises(Exception) as ex_info:
        run("injectors --run")

    assert "failed to load config.py" in ex_info.value.output
