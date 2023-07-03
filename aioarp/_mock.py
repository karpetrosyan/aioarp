import typing
from functools import wraps

from aioarp import get_default_interface
from aioarp import get_ip
from aioarp import get_mac

def mock_get_ip(ip: str) -> typing.Callable[[], str]:
    @wraps(get_ip)
    def inner():
        return ip

    return inner


def mock_get_mac(mac: str) -> typing.Callable[[str], str]:
    @wraps(get_mac)
    def inner(interface: typing.Optional[str]) -> str:
        return mac

    return inner


def mock_get_default_interface(interface: str) -> typing.Callable[[], str]:
    @wraps(get_default_interface)
    def inner() -> str:
        return interface
    return inner