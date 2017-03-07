import argparse


DEFAULTS = {
    "dataset": "parking",
    "protocol": "http",
    "nb_devices": 1,
    "ev_per_hour": 360,
    "duration": 1,
    "broker": "127.0.0.1",
}

PROTOCOLS = "http mqtt coap"

DATASETS = "parking traffic pollution"


def create_parser():
    parser = argparse.ArgumentParser()

    add_commands(parser)
    add_params(parser)
    add_datasets(parser)
    add_protocols(parser)

    parser.set_defaults(**DEFAULTS)

    return parser


def add_params(parser):
    parser.add_argument(
        "--nb-devices", type=int,
        metavar="<nb>",
        help="number of devices to operate   [%(default)s]")

    parser.add_argument(
        "--ev-per-hour", type=int,
        metavar="<int>",
        help="number of events per hour      [%(default)s]")

    parser.add_argument(
        "--duration", type=int,
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


def add_datasets(parser):
    choice = DATASETS
    parser.add_argument(
        "--dataset",
        choices=choice.split(),
        help="send events using specified dataset  [%(default)s]")


def add_commands(parser):
    group = parser.add_mutually_exclusive_group()

    for cmd, func in command.func.items():
        group.add_argument(
            "--" + cmd,
            action="store_const", const=cmd,
            dest="command",
            help=func.__doc__)


def command(f):
    """ decorator to define parser commands """
    command.func[f.__name__.replace("_", "-")] = f

import collections
command.func = collections.OrderedDict()
