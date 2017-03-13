import argparse


class Parser(argparse.ArgumentParser):
    def __init__(self):
        super(Parser, self).__init__(add_help=False)
        self.add_argument("-h", "--help", action="help",
                          help=argparse.SUPPRESS)
        self.commands = self.add_mutually_exclusive_group()

    def add_command(self, command, help=None):
        self.commands.add_argument(
            "--" + command,
            action="store_const", const=command,
            dest="command",
            help=help)

    def add_commands(self):
        for cmd, func in command.func.items():
            self.add_command(cmd, help=func.__doc__)


def command(f):
    """ decorator to define parser commands """
    command.func[f.__name__.replace("_", "-")] = f


def run_command(opts):
    args = opts.__dict__
    return command.func[opts.command](**args)


import collections
command.func = collections.OrderedDict()
command.run = run_command
