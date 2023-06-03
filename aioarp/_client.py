import ipaddress

from aioarp._arp import ArpPacket, HardwareType, Protocol
from aioarp._async import async_send_arp
from aioarp._sync import sync_send_arp
from aioarp._utils import get_ip, get_mac

__all__ = (
    'build_arp_packet',
    'request',
    'arequest'
)


def build_arp_packet(
        interface: str,
        target_ip: str
) -> ArpPacket:
    try:
        ipaddress.IPv4Address(target_ip)
    except ipaddress.AddressValueError:
        raise Exception("Invalid IPv4 Address was received")

    hardware_type = HardwareType.ethernet
    protocol_type = Protocol.ip

    # TODO: catch interface not found error
    sender_mac = get_mac(interface)
    sender_ip = get_ip()
    target_mac = 'ff:ff:ff:ff:ff:ff'

    request_packet = ArpPacket(
        hardware_type,
        protocol_type,
        sender_mac,
        sender_ip,
        target_mac,
        target_ip,
    )
    return request_packet


def request(
        interface: str,
        target_ip: str,
) -> ArpPacket:
    request_packet = build_arp_packet(interface, target_ip)
    arp_response = sync_send_arp(request_packet, interface)
    return arp_response


async def arequest(
        interface: str,
        target_ip: str,
) -> ArpPacket:
    request_packet = build_arp_packet(interface, target_ip)
    arp_response = await async_send_arp(request_packet, interface)
    return arp_response
