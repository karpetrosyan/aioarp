import socket
import fcntl
import struct
import ipaddress

__all__ = (
    'is_valid_ipv4',
    'get_mac',
    'get_ip',
    'enforce_mac',
    'enforce_ip',
    'parse_mac',
    'parse_ip'
)

def is_valid_ipv4(ip: str) -> bool:
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def get_mac(interface) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(interface, 'utf-8')[:15]))
        return ':'.join('%02x' % b for b in info[18:24])


def get_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("1.1.1.1", 80))
        return s.getsockname()[0]


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
