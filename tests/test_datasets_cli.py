import pytest

from runner import run


def test_datasets_no_args():
    run("datasets")


def test_datasets_list():
    ret = run("datasets --list")

    assert "synthetic" in ret
    assert "citypulse" in ret


def test_citypulse_traffic_download():
    run("datasets --download --dataset citypulse --event traffic")

    import os
    assert os.path.isdir("embers.datasets.citypulse")

    import embers.datasets.citypulse.traffic as traffic
    t = traffic.Traffic()
    s = t.get_source(0)
    d = s.next()

    assert "vehicleCount" in d
    assert "avgSpeed" in d


def test_citypulse_pollution_download():
    run("datasets --download --dataset citypulse --event pollution")

    import embers.datasets.citypulse.pollution as pollution
    t = pollution.Pollution()
    s = t.get_source(0)
    d = s.next()

    assert "carbon_monoxide" in d
    assert "nitrogen_dioxide" in d


def test_synthetic_download_fails():
    with pytest.raises(Exception) as e:
        run("datasets --download --dataset synthetic --event traffic")

    assert "no attribute 'download'" in e.value.output
