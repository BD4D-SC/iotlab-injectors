from config import get_config
from config import get_broker_api


def GatewayMetadata(dataset):
    return {"type": "gateway", "dataset": str(dataset)}


def DeviceMetadata(dataset):
    return {"type": "device", "dataset": str(dataset)}


def register_gateway(dataset):
    metadata = GatewayMetadata(dataset)
    api = get_broker_api()
    ret = api.get_devices(metadata)

    if ret["devices"]:
        return False
    else:
        return api.register_device(metadata)
