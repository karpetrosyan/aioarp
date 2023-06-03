import time
import typing

from aioarp import _exceptions as exc
from aioarp._arp import ArpPacket, EthPacket, Protocol, ETHERNET_HEADER_SIZE, ARP_HEADER_SIZE
from aioarp._utils import is_valid_ipv4
from ..backends._async import AsyncSocket


async def receive_arp(sock: AsyncSocket, timeout: float) -> typing.Optional[ArpPacket]:
    start_time = time.time()
    while True:

        # Check if timeout was expired
        if time.time() - start_time > timeout:
            raise exc.NotFoundError()

        # Try to read frame
        try:
            frame = await sock.receive_frame()
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


async def send_arp(arp_packet: ArpPacket, interface: str) -> typing.Optional[ArpPacket]:
    sock = AsyncSocket(interface)
    ethernet_packet = EthPacket(
        target_mac=arp_packet.target_mac,
        sender_mac=arp_packet.sender_mac,
        proto=Protocol.arp
    )

    try:
        await sock.write_frame(ethernet_packet.build_frame() + arp_packet.build_frame())
    except exc.WriteTimeoutError as e:
        raise exc.NotFoundError from e

    return await receive_arp(sock)
