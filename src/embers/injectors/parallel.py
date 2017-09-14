import threading
import Queue
MAX_THREADS = 100

def parallel_run(params, run, collect=lambda th:th):
    class runner(threading.Thread):
        def run(self):
            try:
                run(self.param, self)
                collect(self)
            except Exception as e:
                self.error = e
            queue.get()

    queue = Queue.Queue(MAX_THREADS)

    t = []
    for param in params:
        queue.put(True)
        th = runner()
        th.param = param
        th.error = None
        th.start()
        t.append(th)
    join_all(t)


def join_all(t):
    error = None
    for th in t:
        th.join()
        error = error or th.error
    if error:
        raise error
