from command_parser import Parser, command
from injectors_cli import EVENTS
from injectors_cli import DEFAULTS as _DEFAULTS
import config
import registry


DEFAULTS = {
    "broker": _DEFAULTS["broker"],
}


@command
def init(broker, **_):
    """ initialize config.py (root_auth) """
    config.init_config(broker)


@command
def list(gateway, device, **_):
    """ list registered devices """

    selector = {}
    if gateway: selector["event_type"] = gateway
    if device:  selector["type"] = "device"

    api = config.get_broker_api()
    ret = api.get_devices(selector)
    for device in ret:
        line = "{uuid} {type}"
        line += " {event_type}" if device.has_key("event_type") else ""
        if not device.has_key("type"): device["type"] = "unknown"
        print(line.format(**device))


@command
def register(gateway, device, **_):
    """ register specified device """

    if not gateway:
        print("please specify --gateway <event type>")
        return 1

    if device:
        ret = registry.register_device(event_type=gateway)
    else:
        ret = registry.register_gateway(event_type=gateway)
        if not ret:
            print("gateway already registered")
            return 1

    print("uuid: {}".format(ret["uuid"]))


@command
def unregister(uuid, gateway, **_):
    """ unregister specified device """

    selector = {}
    if gateway: selector["event_type"] = gateway
    if uuid:  selector["uuid"] = uuid

    if not selector:
        print("please specify --uuid <uuid> or --gateway <event type>")
        return 1

    api = config.get_broker_api()
    for device in api.get_devices(selector):
        ret = api.unregister_device(device["uuid"])


def add_parameters(parser):
    choice = EVENTS
    parser.add_argument(
        "--gateway",
        choices=choice.split(),
        help="gateway|device type (events) to register")

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
    parser = Parser()
    add_parameters(parser)
    parser.set_defaults(**DEFAULTS)
    return parser.parse_and_run()
