from command_parser import command
from command_parser import Parser

import registry
import injector


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


def main():
    parser = create_parser()
    opts = parser.parse_args()

    if opts.command:
        return command.run(opts)
    else:
        parser.print_usage()


@command
def run(nb_devices, dataset, protocol, ev_per_hour, duration, **_):
    """ run <nb> injectors on local node """

    print("running {nb} '{}+{}' injector{s} on local node".format(
          dataset, protocol, nb=nb_devices, s=s(nb_devices)))

    gateway = registry.lookup_gateway(dataset)
    if not gateway:
        gateway = registry.register_gateway(dataset)
        print("==> registered gateway '{}'".format(dataset))

    devices = registry.lookup_devices(dataset)
    if nb_devices > len(devices):
        more = nb_devices - len(devices)
        devices += [ registry.register_device(dataset) for i in range(more) ]
        print("==> registered {} more device{s}".format(more, s=s(more)))

    devices = devices[:nb_devices]

    print("sending {} event{s}/h (per injector) for {} min.".format(
          ev_per_hour, duration, s=s(ev_per_hour)))

    try:
        injector.run(devices, gateway, dataset, protocol,
                     ev_per_hour, duration)
    except KeyboardInterrupt:
        return 1


@command
def deploy(nb_devices, dataset, **_):
    """ deploy injectors on <nb> A8 nodes """

    print("deploying {nb} node{s} with '{}' injector{s}".format(
          dataset, nb=nb_devices, s=s(nb_devices)))
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

    parser.add_commands()

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
