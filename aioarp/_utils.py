import ipaddress
import socket
import subprocess
import typing

import getmac

__all__ = (
    'is_valid_ipv4',
    'get_mac',
    'get_ip',
    'get_default_interface',
    'enforce_mac',
    'enforce_ip',
    'parse_mac',
    'parse_ip'
)

OUR_MAC = None
OUR_IP = None
OUR_INTERFACE = None


def is_valid_ipv4(ip: str) -> bool:
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def get_mac(interface: typing.Optional[str] = None) -> str:  # pragma: no cover
    if interface is None:
        interface = get_default_interface()
    global OUR_MAC
    if OUR_MAC:
        return OUR_MAC
    
    OUR_MAC = getmac.get_mac_address(interface)
    return typing.cast(str, OUR_MAC)


def get_ip() -> str:  # pragma: no cover
    global OUR_IP
    if OUR_IP:
        return OUR_IP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("1.1.1.1", 80))
        ip = typing.cast(str, s.getsockname()[0])
        OUR_IP = ip
        return OUR_IP


def enforce_mac(mac: str) -> bytes:
    mac_bytes = []
    for b in mac.split(':'):
        mac_bytes.append(int(b, 16))
    return bytes(mac_bytes)


def enforce_ip(ip: str) -> bytes:
    ip_bytes = []
    for b in ip.split('.'):
        ip_bytes.append(int(b))
    return bytes(ip_bytes)


def get_default_interface() -> str:  # pragma: no cover
    global OUR_INTERFACE
    if OUR_INTERFACE:
        return OUR_INTERFACE
    output = subprocess.check_output(['ip', 'route', 'list']).decode().split()
    for ind, word in enumerate(output):
        if word == 'dev':
            OUR_INTERFACE = output[ind + 1]
            return OUR_INTERFACE
    raise RuntimeError('Could not find default interface')    
        
def parse_mac(mac: bytes) -> str:
    mac_parts = []
    for b in mac:
        hex = f'{b:x}'
        if len(hex) == 1:
            hex = '0' + hex
        mac_parts.append(hex)
    return ':'.join(mac_parts)


def parse_ip(ip: bytes) -> str:
    ip_parts = []
    for b in ip:
        ip_parts.append(str(b))
    return '.'.join(ip_parts)
