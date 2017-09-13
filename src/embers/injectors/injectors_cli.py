from command_parser import command
from command_parser import Parser

import registry
import injector
import embers.datasets.lib.lookup as datasets


DEFAULTS = {
    "events": "traffic",
    "protocol": "http",
    "nb_devices": 1,
    "ev_per_hour": 3600,
    "duration": .1,
    "dataset": "synthetic",
    "offset": "0",
    "broker": "127.0.0.1",
    "insecure": False,
}

PROTOCOLS = "http mqtt coap https"

EVENTS = "parking traffic pollution"


def main():
    parser = create_parser()
    return parser.parse_and_run()


@command
def run(nb_devices, events, dataset, protocol, ev_per_hour, duration,
        offset, insecure, **_):
    """ run <nb> injectors on local node """

    print("running {nb} '{}+{}' injector{s} on local node".format(
          events, protocol, nb=nb_devices, s=s(nb_devices)))

    gateway, devices = register_devices(events, nb_devices)

    print("sending {} event{s}/h (per injector) for {} min.".format(
          ev_per_hour, duration, s=s(ev_per_hour)))

    stats = injector.stats()

    try:
        injector.run(devices, gateway, dataset, protocol,
                     ev_per_hour, duration, offset, stats)
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        print("fatal: {}".format(e))
        return 2
    finally:
        unregister_devices(devices)
        stats.dump()


def register_devices(events, nb_devices):
    gateway = registry.lookup_gateway(events)
    if not gateway:
        gateway = registry.register_gateway(events)
        print("==> registered gateway '{}'".format(events))

    devices = registry.register_devices(events, nb_devices)

    return gateway, devices


def unregister_devices(devices):
    try:
        registry.unregister_devices(devices)
    except:
        print("failed to unregister devices")


@command
def deploy(nb_devices, events, **_):
    """ deploy injectors on <nb> A8 nodes """

    print("deploying {nb} node{s} with '{}' injector{s}".format(
          events, nb=nb_devices, s=s(nb_devices)))
    pass


@command
def init_config(broker, **_):
    """ initialize config.py (root_auth) """
    import config
    config.init_config(broker)


def s(nb):
    return "s" if nb != 1 else ""


def create_parser():
    parser = Parser()

    add_params(parser)
    add_datasets(parser)
    add_events(parser)
    add_protocols(parser)
    add_options(parser)

    parser.set_defaults(**DEFAULTS)

    return parser


def add_params(parser):
    parser.add_argument(
        "--nb-devices", type=int,
        metavar="<nb>",
        help="number of devices to operate   [%(default)s]")

    parser.add_argument(
        "--offset", type=int,
        metavar="<nb>",
        help="offset in dataset for devices  [%(default)s]")

    parser.add_argument(
        "--ev-per-hour", type=int,
        metavar="<int>",
        help="number of events per hour      [%(default)s]")

    parser.add_argument(
        "--duration", type=float,
        metavar="<min>",
        help="number of minutes to run for   [%(default)s]")

    parser.add_argument(
        "--broker",
        metavar="<address>",
        help="broker to use as destination   [%(default)s]")


def add_protocols(parser):
    choice = PROTOCOLS
    parser.add_argument(
        "--protocol",
        choices=choice.split(),
        help="send events using specified protocol [%(default)s]")


def add_events(parser):
    choice = EVENTS
    parser.add_argument(
        "--events",
        choices=choice.split(),
        help="send events of specified type  [%(default)s]")


def add_datasets(parser):
    choices = datasets.get_datasets()
    parser.add_argument(
        "--dataset",
        choices=choices,
        help="dataset to use as events source [%(default)s]")


def add_options(parser):
    parser.add_argument(
        "--insecure",
        action=InsecureAction,
        nargs=0,
        help="do not check server certificate [%(default)s]")

    parser.add_argument(
        "--fiware",
        action=UseFiwareAction,
        nargs=0,
        help="use FiWare data format for payload [%(default)s]")

    parser.add_argument(
        "--max-threads",
        action=MaxThreadsAction,
        help="use at most specified nb of threads [no limit]")


import argparse

class InsecureAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import embers.meshblu.https as https
        https.set_insecure()

        setattr(namespace, self.dest, values)

class UseFiwareAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import embers.datasets.lib as datasets
        datasets.use_fiware_format = True

        setattr(namespace, self.dest, values)

class MaxThreadsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        injector.EventSender.set_max_threads(int(values))
