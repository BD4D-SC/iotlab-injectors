import config

import threading
import time


def run(devices, gateway, dataset, protocol, ev_per_hour, duration):
    EventSender.protocol = import_client(protocol)
    data_source = DataSource(dataset)
    devices = reset_devices(devices)
    senders = [ EventSender(gateway, device) for device in devices ]
    return _run(senders, data_source, duration, ev_per_hour)


def _run(senders, data_source, duration, ev_per_hour):
    start_time = time.time()
    end_time = start_time + duration * 60
    while end_time > time.time():
        t1 = time.time()
        send_next_events(senders, data_source)
        t2 = time.time()
        sleep_time = 3600./ev_per_hour - t2 + t1
        if sleep_time > 0:
            time.sleep(sleep_time)


def reset_devices(devices):
    api = config.get_broker_api()
    return [ api.reset_token(device["uuid"]) for device in devices ]


def send_next_events(senders, data_source):
    for i, sender in enumerate(senders):
        event = data_source.get_source(i).next()
        sender.send(event)
    for sender in senders:
        sender.join()


class EventSender:

    def __init__(self, gateway, device):
        assert self.protocol
        broker = config.get_config().broker_address
        self.client = self.protocol(broker)
        self.client.auth = (device["uuid"], device["token"])
        self.gateway = gateway["uuid"]

    def send(self, event):
        def run():
            self.client.publish(self.gateway, event)
        self.thread = threading.Thread(target=run)
        self.thread.start()

    def join(self):
        self.thread.join()



class DataSource:

    def __init__(self, dataset):
        pass

    def get_source(self, i):
        class it:
            def next(self): pass

        return it()


def import_client(protocol):
    return __import__("embers.meshblu." + protocol,
                      fromlist=["Client"]).Client
