import config

import threading
import Queue
import time

from stats import stats
from embers.datasets.lib.lookup import get_dataset


def run(devices, gateway, dataset, protocol, ev_per_hour, duration,
        offset, stats):
    EventSender.protocol = import_client(protocol)
    data_source = get_dataset(dataset, event_type=gateway["event_type"])
    data_source.offset = offset
    senders = [ EventSender(gateway, device) for device in devices ]
    _run(senders, data_source, duration, ev_per_hour, stats)


def _run(senders, data_source, duration, ev_per_hour, stats):
    start_time = time.time()
    end_time = start_time + duration * 60
    stats.start_time = start_time
    stats.nb_devices = len(senders)
    while end_time > time.time():
        t1 = time.time()
        send_next_events(senders, data_source, stats)
        t2 = time.time()
        sleep_time = 3600./ev_per_hour - t2 + t1
        if sleep_time < 0:
            stats.time_overflow.append(-sleep_time)
            sleep_time = 0
        if sleep_time + t2 > end_time:
            sleep_time = end_time - t2 if end_time > t2 else 0
        stats.send_time += (t2-t1)
        stats.nb_rounds += 1
        print("round {} send time: {:.2f}".format(stats.nb_rounds, t2-t1))
        stats.end_time = t2
        time.sleep(sleep_time)


def send_next_events(senders, data_source, stats):
    for i, sender in enumerate(senders):
        sender.send(data_source, i)
    error = None
    for sender in senders:
        sender.join()
        stats.nb_sent += 1 if not sender.error else 0
        error = error or sender.error
    if error:
        raise error


class EventSender:
    queue = Queue.Queue()

    def __init__(self, gateway, device):
        assert self.protocol
        broker = config.get_config().broker_address
        self.client = self.protocol(broker)
        self.client.auth = (device["uuid"], device["token"])
        self.gateway = gateway["uuid"]
        self.error = None

    def send(self, data_source, i):
        def run():
            self.queue.put(True)
            try:
                event = data_source.get_source(i + data_source.offset).next()
                self.client.publish(self.gateway, event)
            except Exception as e:
                self.error = e
            self.queue.get()
        self.thread = threading.Thread(target=run)
        self.thread.start()

    def join(self):
        self.thread.join()

    @classmethod
    def set_max_threads(self, nb_threads):
        self.queue = Queue.Queue(nb_threads)


def import_client(protocol):
    return __import__("embers.meshblu." + protocol,
                      fromlist=["Client"]).Client
