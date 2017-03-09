from parser import command, create_parser
from registry import register_gateway


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
    print("sending {} event{s}/h (per injector) for {} min.".format(
          ev_per_hour, duration, s=s(ev_per_hour)))
    pass


@command
def deploy(nb_devices, dataset, **_):
    """ deploy injectors on <nb> A8 nodes """

    print("deploying {nb} node{s} with '{}' injector{s}".format(
          dataset, nb=nb_devices, s=s(nb_devices)))
    pass


@command
def register_gw(dataset, broker, **_):
    """ register gateway for specified dataset """

    print("registering '{}' gateway on {}".format(
          dataset, broker))
    if register_gateway(dataset) is False:
        print("gateway '{}' already registered".format(dataset))
        return 1


@command
def init_config(broker, **_):
    """ initialize config.py (root_auth) """
    import config
    config.init_config(broker)


def s(nb):
    return "s" if nb != 1 else ""


if __name__ == "__main__":
    _ = main()
    import sys
    sys.exit(_)
