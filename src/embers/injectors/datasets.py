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
