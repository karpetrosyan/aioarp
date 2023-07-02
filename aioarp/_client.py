import typing

import aioarp

from ._arp import ArpPacket
from ._arp import HardwareType
from ._arp import ProtocolType
from ._async import async_send_arp
from ._backends._base import SocketInterface
from ._sync import sync_send_arp
from ._utils import get_ip
from ._utils import get_mac
from ._utils import is_valid_ipv4

__all__ = (
    'build_arp_packet',
    'request',
    'arequest'
)


def build_arp_packet(
        target_ip: str,
        interface: typing.Optional[str] = None,
) -> ArpPacket:
    if interface is None:
        interface = aioarp.get_default_interface()
    if not is_valid_ipv4(target_ip):
        raise aioarp.InvalidIpError("Invalid IPv4 Address was received")

    hardware_type = HardwareType.ethernet
    protocol_type = ProtocolType.ip

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
        target_ip: str,
        interface: typing.Optional[str] = None,
        sock: typing.Optional[SocketInterface] = None,
        timeout: typing.Optional[float] = None,
        wait_response: bool = True
) -> typing.Optional[ArpPacket]:
    request_packet = build_arp_packet(target_ip, interface)
    arp_response = sync_send_arp(request_packet, sock, interface, timeout, wait_response)
    return arp_response


async def arequest(
        target_ip: str,
        interface: typing.Optional[str] = None,
        sock: typing.Optional[SocketInterface] = None,
        timeout: typing.Optional[float] = None,
        wait_response: bool = True
) -> typing.Optional[ArpPacket]:
    request_packet = build_arp_packet(target_ip, interface)
    arp_response = await async_send_arp(request_packet, sock, interface, timeout, wait_response)
    return arp_response
