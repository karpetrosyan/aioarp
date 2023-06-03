import ipaddress

from aioarp._arp import ArpPacket
from aioarp._arp import HardwareType, Protocol, Opcode
from aioarp._sync import send_arp as sync_send_arp
from aioarp._async import send_arp as async_send_arp
from aioarp._utils import get_ip
from aioarp._utils import get_mac


def request(
        interface: str,
        target_ip: str,
        opcode: Opcode = Opcode.request,
):
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
        opcode,
    )

    arp_response = sync_send_arp(request_packet, interface)
    return arp_response


async def arequest(
        interface: str,
        target_ip: str,
        opcode: Opcode = Opcode.request,
):
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
        opcode,
    )

    arp_response = await async_send_arp(request_packet, interface)
    return arp_response
