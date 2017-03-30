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
def list(events, device, gateway, **_):
    """ list registered devices """

    selector = {}
    if events:  selector["event_type"] = events
    if device:  selector["type"] = "device"
    if gateway: selector["type"] = "gateway"

    api = config.get_broker_api()
    ret = api.get_devices(selector)
    for device in ret:
        line = "{uuid} {type}"
        line += " {event_type}" if device.has_key("event_type") else ""
        if not device.has_key("type"): device["type"] = "unknown"
        print(line.format(**device))


@command
def register(events, device, **_):
    """ register specified device """

    if not events:
        print("please specify --events <event type>")
        return 1

    if device:
        ret = registry.register_device(event_type=events)
    else:
        ret = registry.register_gateway(event_type=events)
        if not ret:
            print("gateway already registered")
            return 1

    print("uuid: {}".format(ret["uuid"]))


@command
def unregister(uuid, events, device, gateway, root_auth, **_):
    """ unregister specified device """

    if root_auth:
        return unregister_root_auths()

    selector = {}
    if events: selector["event_type"] = events
    if uuid:   selector["uuid"] = uuid
    if device:  selector["type"] = "device"
    if gateway: selector["type"] = "gateway"

    if not selector:
        print("please specify --uuid <uuid> or --events <event type>")
        return 1

    api = config.get_broker_api()
    devices = api.get_devices(selector)
    registry.unregister_devices(devices)


def unregister_root_auths():
    api = config.get_broker_api()
    devices = api.get_devices({"type": "root_auth"})
    devices = [ dev for dev in devices if dev["uuid"] != api.auth[0] ]
    registry.unregister_devices(devices)


@command
def reset(uuid, **_):
    """ reset specified device token """

    if not uuid:
        print("please specify --uuid <uuid>")
        return 1

    api = config.get_broker_api()
    ret = api.reset_token(uuid)
    print("token: " + ret["token"])


def add_parameters(parser):
    parser.add_argument(
        "--broker",
        metavar="<address>",
        help="broker to use as destination [%(default)s]")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--uuid",
        metavar="<uuid>",
        help="device to unregister")
    group.add_argument(
        "--root-auth",
        action="store_true",
        help="unregister all root-auth devices (but local one)")

    parser.add_argument(
        "--events",
        choices=EVENTS.split(),
        help="gateway|device type (events) to register")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--device",
        action="store_true",
        help="register a device (instead of a gateway)")
    group.add_argument(
        "--gateway",
        action="store_true",
        help="register a gateway (optional, this is the default)")


def main():
    parser = Parser()
    add_parameters(parser)
    parser.set_defaults(**DEFAULTS)
    return parser.parse_and_run()
