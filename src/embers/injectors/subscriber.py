import embers.meshblu.subscriber as subscriber
import embers.injectors.registry as registry
import embers.injectors.config as config
import json

from command_parser import Parser

from injectors_cli import EVENTS as gateway_types



def main():
    opts = parse_args()
    gw_type = opts.command

    broker_address = config.get_config().broker_address

    gw = registry.lookup_gateway(gw_type)
    if gw:
        api = config.get_broker_api()
        gw = api.reset_token(gw["uuid"])
    else:
        gw = registry.register_gateway(gw_type)
        print("==> registered gateway '{}'".format(gw_type))

    sub = subscriber.get_subscriber(gw["uuid"])
    sub.on_message = on_message
    sub.on_subscribe = on_subscribe
    sub.opts = opts
    sub.connect(broker_address, gw["token"])
    try:
        sub.loop_forever()
    except KeyboardInterrupt:
        pass
    sub.disconnect()
    print("total messages: {}".format(sub.message_count))


def on_message(sub, message):
    if sub.opts.print_events:
        print(json.dumps(message.payload))
    if sub.opts.print_count:
        print(sub.message_count)
    if sub.opts.exit_after:
        if sub.message_count >= sub.opts.exit_after:
            sub.disconnect()


def on_subscribe(sub):
    print("subscribed to: " + sub.target_uuid)


def parse_args():
    parser = Parser()
    for cmd in gateway_types.split():
        parser.add_command(cmd)

    parser.add_argument(
        "--print-events",
        action="store_true")

    parser.add_argument(
        "--print-count",
        action="store_true")

    parser.add_argument(
        "--exit-after",
        metavar="<nb events>",
        type=int,
    )

    opts = parser.parse_args()
    if not opts.command:
        parser.print_usage()
        parser.exit(0)
    return opts
