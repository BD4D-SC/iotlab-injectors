from parser import command, create_parser

import registry
import injector


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
