import socket
import typing

import aioarp
from aioarp._arp import ArpPacket, HardwareType, Protocol
from aioarp._async import async_send_arp
from aioarp._backends._async import AsyncStream
from aioarp._backends._base import SocketInterface
from aioarp._backends._sync import Stream
from aioarp._sync import sync_send_arp
from aioarp._utils import get_ip, get_mac, is_valid_ipv4

__all__ = (
    'build_arp_packet',
    'request',
    'arequest'
)


def build_arp_packet(
        interface: str,
        target_ip: str
) -> ArpPacket:
    if not is_valid_ipv4(target_ip):
        raise aioarp.InvalidIpError("Invalid IPv4 Address was received")

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
        timeout: typing.Optional[float] = None,
        sock: typing.Optional[SocketInterface] = None
) -> ArpPacket:
    if not sock:  # pragma: no cover
        sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    with Stream(interface=interface,
                    sock=sock) as stream:
        request_packet = build_arp_packet(interface, target_ip)
        arp_response = sync_send_arp(request_packet, stream, timeout)
        return arp_response


async def arequest(
        interface: str,
        target_ip: str,
        timeout: typing.Optional[float] = None,
        sock: typing.Optional[SocketInterface] = None
) -> ArpPacket:
    if not sock:  # pragma: no cover
        sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    with AsyncStream(interface=interface,
                    sock=sock) as stream:
        request_packet = build_arp_packet(interface, target_ip)
        arp_response = await async_send_arp(request_packet, stream, timeout)
        return arp_response
