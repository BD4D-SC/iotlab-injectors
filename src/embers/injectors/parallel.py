import threading
MAX_THREADS = 100

def parallel_run(params, run, collect=lambda th:th):
    class runner(threading.Thread):
        def run(self):
            run(self.param, self)

    t = []
    for param in params:
        th = runner()
        th.param = param
        th.start()
        t.append(th)
        if len(t) == MAX_THREADS:
            join_all(t, collect)
    join_all(t, collect)


def join_all(t, func=lambda th:th):
    while len(t):
        th = t.pop()
        th.join()
        func(th)
