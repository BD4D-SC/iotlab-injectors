import threading
MAX_THREADS = 100

def parallel_run(params, run, collect=lambda th:th):
    class runner(threading.Thread):
        def run(self):
            try:
                run(self.param, self)
            except Exception as e:
                self.error = e

    t = []
    for param in params:
        th = runner()
        th.param = param
        th.error = None
        th.start()
        t.append(th)
        if len(t) == MAX_THREADS:
            join_all(t, collect)
    join_all(t, collect)


def join_all(t, func=lambda th:th):
    error = None
    while len(t):
        th = t.pop()
        th.join()
        error = error or th.error
        if error: continue
        func(th)
    if error:
        raise error
