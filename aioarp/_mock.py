import typing
from functools import wraps

from aioarp import LocalNetwork

def mock_get_ip(ip: str) -> typing.Callable[[], str]:
    @wraps(LocalNetwork.get_ip)
    def inner(self, ):
        return ip

    return inner


def mock_get_mac(mac: str) -> typing.Callable[[str], str]:
    @wraps(LocalNetwork.get_mac)
    def inner(self, interface: typing.Optional[str]) -> str:
        return mac

    return inner


def mock_get_default_interface(interface: str) -> typing.Callable[[], str]:
    @wraps(LocalNetwork.get_default_interface)
    def inner(self, ) -> str:
        return interface
    return inner