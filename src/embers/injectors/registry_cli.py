from command_parser import command
from parser import create_parser
from parser import DATASETS
import config
import registry


@command
def init(broker, **_):
    """ initialize config.py (root_auth) """
    config.init_config(broker)


@command
def list(gateway, device, **_):
    """ list registered devices """

    api = config.get_broker_api()
    ret = api.get_devices()
    for device in ret:
        line = "{uuid} {type}"
        line += " {dataset}" if device.has_key("dataset") else ""
        if not device.has_key("type"): device["type"] = "unknown"
        print(line.format(**device))


@command
def register(gateway, device, **_):
    """ register specified device """

    if not gateway:
        print("please specify --gateway <dataset>")
        return 1

    if device:
        ret = registry.register_device(dataset=gateway)
    else:
        ret = registry.register_gateway(dataset=gateway)
        if not ret:
            print("gateway already registered")
            return 1

    print("uuid: {}".format(ret["uuid"]))


@command
def unregister(uuid, **_):
    """ unregister specified device """

    if not uuid:
        print("please specify --uuid <uuid>")
        return 1

    api = config.get_broker_api()
    ret = api.unregister_device(uuid)


def add_parameters(parser):
    choice = DATASETS
    parser.add_argument(
        "--gateway",
        choices=choice.split(),
        help="gateway|device type (dataset) to register")

    parser.add_argument(
        "--broker",
        metavar="<address>",
        help="broker to use as destination [%(default)s]")

    parser.add_argument(
        "--uuid",
        metavar="<uuid>",
        help="device to unregister")

    parser.add_argument(
        "--device",
        action="store_true",
        help="register a device (instead of a gateway)")


def main():
    patch_parser_module()

    parser = create_parser()
    opts = parser.parse_args()

    if opts.command:
        return command.run(opts)
    else:
        parser.print_usage()


def patch_parser_module():
    import parser
    parser.add_protocols = lambda x: True
    parser.add_datasets = lambda x: True
    parser.add_params = add_parameters
    parser.DEFAULTS = {
        "broker": parser.DEFAULTS["broker"],
    }
