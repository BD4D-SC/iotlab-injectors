import embers.meshblu.http as http

CONFIG_FILE = "config.py"


class config: pass  # namespace


def get_config(force_reload=False):
    if force_reload or not hasattr(get_config, "config_loaded"):
        execfile(CONFIG_FILE, config.__dict__)
        get_config.config_loaded = True
    assert config.broker_address
    assert config.root_auth
    return config()


def get_broker_api(auth=None):
    config = get_config()
    api = http.Client(config.broker_address)
    api.auth = config.root_auth if auth is None else auth
    return api


def init_config(broker_address):
    no_auth = ()
    api = get_broker_api(no_auth)
    reg = api.register_device({"type":"root_auth"})

    root_auth = ( reg['uuid'], reg['token'] )

    conf = "root_auth = {}\nbroker_address = '{}'\n"
    open(CONFIG_FILE, 'w') \
         .write(conf.format(root_auth, broker_address))
