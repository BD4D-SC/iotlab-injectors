from runner import run


def test_datasets_no_args():
    run("datasets")


def test_datasets_list():
    ret = run("datasets --list")

    assert "synthetic" in ret
    assert "citypulse" in ret
