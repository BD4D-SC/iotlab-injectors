from command_parser import Parser, command
from injectors_cli import EVENTS

import embers.datasets.lib.lookup as datasets


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
        output = ds
        if events: output += " %s" % ":".join(events)
        print(output)


def get_supported_events(dataset):
    events = []
    for ev in EVENTS.split():
        try:
            ds = datasets.get_dataset(dataset, ev)
            events.append(ev)
        except Exception:
            pass
    return events


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
