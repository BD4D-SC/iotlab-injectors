from config import get_config
from config import get_broker_api
from parallel import parallel_run


def GatewayMetadata(event_type):
    return {"type": "gateway", "event_type": str(event_type)}


def DeviceMetadata(event_type):
    return {"type": "device", "event_type": str(event_type)}


def register_gateway(event_type):
    metadata = GatewayMetadata(event_type)
    gateway = _lookup_devices(metadata)
    if gateway:
        return False
    else:
        return _register_device(metadata)


def register_device(event_type):
    metadata = DeviceMetadata(event_type)
    return _register_device(metadata)


def lookup_gateway(event_type):
    metadata = GatewayMetadata(event_type)
    ret = _lookup_devices(metadata)
    return ret[0] if ret else None


def lookup_devices(event_type):
    metadata = DeviceMetadata(event_type)
    return _lookup_devices(metadata)


def _register_device(metadata):
    api = get_broker_api()
    return api.register_device(metadata)


def _lookup_devices(metadata):
    api = get_broker_api()
    return api.get_devices(metadata)


def register_devices(event_type, nb_devices):
    devices = []
    def collect(thread):
        devices.append(thread.device)
    def run(x, thread):
        thread.device = register_device(event_type)

    parallel_run([1]*nb_devices, run, collect)
    return devices


def unregister(uuid, auth):
    api = get_broker_api()
    api.auth = (auth["uuid"], auth["token"])
    api.unregister_device(uuid)


def unregister_devices(devices):
    def _unregister(uuid, auth, res):
        unregister(uuid, auth)

    apply_to_devices(devices, _unregister)


def reset(uuid, auth):
    api = get_broker_api()
    api.auth = (auth["uuid"], auth["token"])
    return api.reset_token(uuid)


def reset_devices(devices):
    result = []
    def collect(res):
        result.append(res.auth)
    def _reset(uuid, auth, res):
        res.auth = reset(uuid, auth)

    apply_to_devices(devices, _reset, collect)
    return result


def apply_to_devices(devices, func, collect=lambda res:res):
    # workaround Meshblu rate-limiting using temporary auth devices
    auth = register_devices("unreg_auth", min(10, len(devices)))
    params = [ {"uuid": device["uuid"], "auth": auth[i % len(auth)] }
               for i, device in enumerate(devices) ]

    parallel_run(params, lambda param, th: func(res=th, **param), collect)
    parallel_run(auth, lambda x, th: unregister(x["uuid"], x))
