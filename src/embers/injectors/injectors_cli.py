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
    "fiware": False,
}

PROTOCOLS = "http mqtt coap https"

EVENTS = "parking traffic pollution"


def main():
    parser = create_parser()
    return parser.parse_and_run()


@command
def run(nb_devices, events, dataset, protocol, ev_per_hour, duration,
        offset, insecure, reuse_devices, **_):
    """ run <nb-devices> injectors """

    print("running {nb} '{}+{}' injector{s} on local node".format(
          events, protocol, nb=nb_devices, s=s(nb_devices)))

    if reuse_devices:
        gateway, devices = reuse_devices(events, nb_devices, offset)
    else:
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
        if not reuse_devices:
            unregister_devices(devices)
        stats.dump()


@command
def init_config(broker, **_):
    """ initialize config.py (root_auth) """
    import config
    config.init_config(broker)


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


def lookup_register_devices(events, nb_devices, offset):
    devices = registry.lookup_devices(events)
    devices = devices[offset:offset+nb_devices]
    devices = registry.reset_devices(devices)

    nb_extra_needed = nb_devices - len(devices)
    gateway, extra = register_devices(events, nb_devices=nb_extra_needed)

    return gateway, devices+extra


def file_lookup_register_devices(events, nb_devices, offset):
    devices = registry.load_devices(events)
    targets = devices[offset:offset+nb_devices]
    replace = check_working(targets, events)
    if replace:
        targets = replace
        devices = devices[0:offset] + targets + devices[offset+nb_devices:]

    nb_extra = offset+nb_devices - len(devices)
    gateway, extra = register_devices(events, nb_devices=nb_extra)

    if extra or replace:
        registry.save_devices(events, devices+extra)

    return gateway, targets+extra


def check_working(targets, events):
    working = registry.check_devices(targets)
    if working == targets:
        return []
    nb_dead = len(targets) - len(working)
    replace = registry.register_devices(events, nb_dead)
    print("replaced {} device{s}".format(nb_dead, s=s(nb_dead)))
    return working + replace


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
        metavar="<int>",
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

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--reuse-devices",
        action='store_const',
        const=lookup_register_devices,
        help="re-use available devices, do not register/unregister")

    group.add_argument(
        "--file-reuse-devices",
        action='store_const',
        const=file_lookup_register_devices,
        dest="reuse_devices",
        help="re-use devices listed in local file")

    parser.add_argument(
        "--max-threads",
        metavar="<nb>",
        action=MaxThreadsAction,
        type=int,
        help="use at most <nb> threads for sending data [no limit]")


import argparse

class InsecureAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import embers.meshblu.https as https
        https.set_insecure()

class UseFiwareAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import embers.datasets.lib as datasets
        datasets.use_fiware_format = True

class MaxThreadsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        injector.EventSender.set_max_threads(int(values))
