import time
import typing

from aioarp import _exceptions as exc
from aioarp._arp import ArpPacket, EthPacket, Protocol, ETHERNET_HEADER_SIZE, ARP_HEADER_SIZE
from aioarp._utils import is_valid_ipv4
from ..backends._sync import Socket


def receive_arp(sock: Socket, timeout: float) -> typing.Optional[ArpPacket]:
    start_time = time.time()
    while True:

        # Check if timeout was expired
        if time.time() - start_time > timeout:
            raise exc.NotFoundError()

        # Try to read frame
        try:
            frame = sock.receive_frame()
        except Exception as e:
            raise exc.NotFoundError() from e

        # Extract the ethernet header
        eth_header = frame[:ETHERNET_HEADER_SIZE]

        try:
            eth_packet = EthPacket.parse(eth_header)
            if eth_packet.proto != Protocol.arp:
                continue

            arp_response = ArpPacket.parse(
                frame[ETHERNET_HEADER_SIZE: ETHERNET_HEADER_SIZE + ARP_HEADER_SIZE])
            if is_valid_ipv4(arp_response.sender_ip):
                return arp_response
        except BaseException:
            # TODO: catch concrete errors
            ...


def send_arp(arp_packet: ArpPacket, interface: str) -> typing.Optional[ArpPacket]:
    sock = Socket(interface)
    ethernet_packet = EthPacket(
        target_mac=arp_packet.target_mac,
        sender_mac=arp_packet.sender_mac,
        proto=Protocol.arp
    )

    try:
        sock.write_frame(ethernet_packet.build_frame() + arp_packet.build_frame())
    except exc.WriteTimeoutError as e:
        raise exc.NotFoundError from e

    return receive_arp(sock)
