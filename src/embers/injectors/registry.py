from config import get_config
from config import get_broker_api


def GatewayMetadata(dataset):
    return {"type": "gateway", "dataset": str(dataset)}


def DeviceMetadata(dataset):
    return {"type": "device", "dataset": str(dataset)}


def register_gateway(dataset):
    metadata = GatewayMetadata(dataset)
    gateway = _lookup_devices(metadata)
    if gateway:
        return False
    else:
        return _register_device(metadata)


def register_device(dataset):
    metadata = DeviceMetadata(dataset)
    return _register_device(metadata)


def lookup_gateway(dataset):
    metadata = GatewayMetadata(dataset)
    ret = _lookup_devices(metadata)
    return ret[0] if ret else None


def lookup_devices(dataset):
    metadata = DeviceMetadata(dataset)
    return _lookup_devices(metadata)


def _register_device(metadata):
    api = get_broker_api()
    return api.register_device(metadata)


def _lookup_devices(metadata):
    api = get_broker_api()
    return api.get_devices(metadata)
