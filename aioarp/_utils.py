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
