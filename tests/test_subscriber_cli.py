from runner import run

from embers.injectors.parallel import parallel_run


def test_subscriber_no_args():
    run("subscriber")


def test_subscriber_exit_after():

    def subscriber():
        run("subscriber --traffic --exit-after 2")

    def injector():
        run("injectors --run --event traffic --duration 0.02")

    run("registry --init")
    parallel_run([subscriber, injector], lambda func, thread: func())


