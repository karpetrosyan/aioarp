import typing
from functools import wraps

from aioarp import get_ip, get_mac


def mock_get_ip(ip: str) -> typing.Callable[[], str]:
    @wraps(get_ip)
    def inner():
        return ip

    return inner


def mock_get_mac(mac: str) -> typing.Callable[[str], str]:
    @wraps(get_mac)
    def inner(interface: str) -> str:
        return mac

    return inner
