import pkgutil

import embers.datasets


def get_datasets():
    package = embers.datasets
    mods = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if modname == "lib":
            continue
        mods += [modname]
        #module = __import__(modname) #, fromlist="dummy")
    return mods


def get_dataset(dataset, event_type):
    package_name = "embers.datasets." + dataset + "." + event_type
    class_name = event_type.capitalize()
    package = __import__(package_name, fromlist=[class_name])
    return package.__dict__[class_name]()
