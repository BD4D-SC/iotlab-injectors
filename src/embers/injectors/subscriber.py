import embers.meshblu.subscriber as subscriber
import embers.injectors.registry as registry
import embers.injectors.config as config

gateway_types = "parking traffic pollution"


def main():
    gw_type = parse_args(choices=gateway_types)

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
    sub.connect(broker_address, gw["token"])
    try:
        sub.loop_forever()
    except KeyboardInterrupt:
        pass
    sub.disconnect()


def on_message(sub, message):
    print(sub.message_count)


def on_subscribe(sub):
    print("subscribed to: " + sub.target_uuid)


def parse_args(choices):
    parser = Parser()
    for cmd in choices.split():
        parser.add_command(cmd)
    opts = parser.parse_args()
    if not opts.command:
        parser.print_usage()
        parser.exit(0)
    return opts.command


import argparse
class Parser(argparse.ArgumentParser):
    def __init__(self):
        super(Parser, self).__init__(add_help=False)
        self.add_argument("-h", "--help", action="help",
                          help=argparse.SUPPRESS)
        self.commands = self.add_mutually_exclusive_group()

    def add_command(self, command):
        self.commands.add_argument(
            "--" + command,
            action="store_const", const=command,
            dest="command")
