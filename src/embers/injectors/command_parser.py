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
