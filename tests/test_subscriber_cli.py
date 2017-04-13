from runner import run

from embers.injectors.parallel import parallel_run
import time


def test_subscriber_no_args():
    run("subscriber")


def test_subscriber_exit_after():

    def subscriber():
        run("subscriber --traffic --exit-after 2")

    def injector():
        run("injectors --run --event traffic --duration 0.02")

    run("registry --init")
    parallel_run([subscriber, injector], lambda func, thread: func())


def test_subscriber_auto_register_print_all():

    def subscriber():
        out.text = run("subscriber --traffic --exit-after 2 \
                       --print-count --print-event")

    def injector():
        time.sleep(0.5)  # let subscriber start first, so it registers
        run("injectors --run --event traffic --duration 0.02")

    class out: pass  # namespace

    run("registry --unregister --event traffic")
    parallel_run([subscriber, injector], lambda func, thread: func())

    out.line = out.text.split('\n')

    assert "registered" in out.line[0]
    assert "Traffic_0.2" in out.line[4]
    assert "1" == out.line[3]
