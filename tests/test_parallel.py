import pytest

import embers.injectors.parallel as parallel


def test_parallel_run():
    def run(device, thread):
        thread.my_result = device

    def collect(thread):
        results.append(thread.my_result)

    devices = range(10)
    results = []

    parallel.parallel_run(devices, run, collect)

    results.sort()
    assert results == devices


def test_more_than_max_threads():
    def run(device, thread):
        pass
    devices = [0] * (parallel.MAX_THREADS + 3)

    parallel.parallel_run(devices, run)


def test_error_in_tread():
    def run(device, thread):
        assert device == 1
    devices = [0, 1]

    with pytest.raises(Exception):
        parallel.parallel_run(devices, run)
