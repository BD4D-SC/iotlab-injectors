from command_parser import Parser, command
from injectors_cli import EVENTS

import embers.datasets.lib.lookup as datasets
import embers.datasets.lib.descriptor as desc

import json


@command
def download(dataset, event_type, **_):
    """ download specified dataset """

    if not dataset or not event_type:
        print("please specify --dataset and --event-type")
        return 1

    ds = datasets.get_dataset(dataset, event_type)
    ds.download()


@command
def list(**_):
    """ list available datasets """
    for ds in datasets.get_datasets():
        events = get_supported_events(ds)
        states = get_download_states(ds, events)
        states = "".join(states)
        nb_dev = get_nb_devices(ds)
        output = ds
        if events: output += " %s" % ":".join(events)
        if states: output += " [%s]" % states
        if nb_dev: output += " (%s)" % nb_dev
        print(output)


@command
def show_descriptors(dataset, event_type, **_):
    """ show datasets descriptors """

    d_sets = [ dataset ] if dataset else datasets.get_datasets()
    events = [ event_type ] if event_type else EVENTS.split()

    for ds in d_sets:
        for ev in events:
            try:
                info = desc.Descriptor("embers.datasets."+ds, ev+".json")
                print(json.dumps(info.__dict__, indent=True))
            except:
                pass


def get_supported_events(dataset):
    events = []
    for ev in EVENTS.split():
        try:
            ds = datasets.get_dataset(dataset, ev)
            events.append(ev)
        except Exception:
            pass
    return events


def get_download_states(dataset, events):
    states = []
    for ev in events:
        ds = datasets.get_dataset(dataset, ev)
        if hasattr(ds, "is_downloaded"):
            state = "D" if ds.is_downloaded() else "_"
        else:
            state = ""
        states.append(state)
    return states


def get_nb_devices(dataset):
    try:
        ev = get_supported_events(dataset)[0]
        info = desc.Descriptor("embers.datasets."+dataset, ev+".json")
        return info.nb_sensors
    except:
        return None


def add_parameters(parser):

    parser.add_argument(
        "--dataset",
        choices=datasets.get_datasets(),
        help="dataset familly to download")

    parser.add_argument(
        "--event-type",
        choices=EVENTS.split(),
        help="dataset type (events) to download")


def main():
    parser = Parser()
    add_parameters(parser)
    return parser.parse_and_run()
