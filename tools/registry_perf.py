#!/usr/bin/env python

import embers.injectors.registry as registry

import argparse
import time


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", help=argparse.SUPPRESS)
parser.add_argument("--nb-devices", type=int, metavar="<int>", help="number of devices")


def main():
    opts = parser.parse_args()
    if not opts.nb_devices:
        parser.print_help()
        return

    devices, t = register(opts.nb_devices)
    print("registration   (s): {}".format(t))
    failed, t = unregister(devices)
    print("unregistration (s): {}{}".format(t, " FAILED" if failed else ""))


def register(nb_devices, events="traffic"):
    t = time.time()
    devices = registry.register_devices(events, nb_devices)
    t = time.time() - t

    return devices, t


def unregister(devices):
    t = time.time()
    try:
        failed = False
        registry.unregister_devices(devices)
    except:
        failed = True
    t = time.time() - t

    return failed, t



if __name__ == "__main__":
    main()
