import socket
import time
import typing

from aioarp import _exceptions as exc
from aioarp._arp import ARP_HEADER_SIZE
from aioarp._arp import ETHERNET_HEADER_SIZE
from aioarp._arp import ArpPacket
from aioarp._arp import EthPacket
from aioarp._arp import ProtocolType
from aioarp._backends import Stream
from aioarp._backends._base import SocketInterface
from aioarp._utils import get_default_interface
from aioarp._utils import is_valid_ipv4
from aioarp.defaults import DEFAULT_READ_TIMEOUT
from aioarp.defaults import DEFAULT_REPLY_MISSING_TIME
from aioarp.defaults import DEFAULT_WRITE_TIMEOUT

__all__ = (
    'sync_send_arp',
)


def receive_arp(sock: Stream, target_ip: str, timeout: float) -> ArpPacket:
    start_time = time.time()
    while True:

        # Check if timeout was expired
        if time.time() - start_time > timeout:
            raise exc.NotFoundError()

        # Try to read frame
        try:
            frame = sock.receive_frame(timeout=DEFAULT_READ_TIMEOUT)
        except Exception as e:  # pragma: no cover
            raise exc.NotFoundError() from e

        # Extract the ethernet header
        eth_header = frame[:ETHERNET_HEADER_SIZE]

        try:
            eth_packet = EthPacket.parse(eth_header)
            if eth_packet.proto != ProtocolType.arp:
                continue


            arp_response = ArpPacket.parse(
                frame[ETHERNET_HEADER_SIZE: ETHERNET_HEADER_SIZE + ARP_HEADER_SIZE])
            if arp_response.sender_ip != target_ip:
                continue
            if is_valid_ipv4(arp_response.sender_ip):
                return arp_response
        except BaseException:  # pragma: no cover
            # TODO: catch concrete errors
            ...


def sync_send_arp(arp_packet: ArpPacket,
                         sock: typing.Optional[SocketInterface] = None,
                         interface: typing.Optional[str] = None,
                         timeout: typing.Optional[float] = None,
                         wait_response: bool = True) -> typing.Optional[ArpPacket]:
    ethernet_packet = EthPacket(
        target_mac=arp_packet.target_mac,
        sender_mac=arp_packet.sender_mac,
        proto=ProtocolType.arp
    )
    if interface is None:  # pragma: no cover
        interface = get_default_interface()
    if not sock:  # pragma: no cover
        sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    with Stream(interface=interface,
                    sock=sock) as stream:
        try:
            frame_to_send = ethernet_packet.build_frame() + arp_packet.build_frame()
            stream.write_frame(frame_to_send, timeout=DEFAULT_WRITE_TIMEOUT)
        except exc.WriteTimeoutError as e:  # pragma: no cover
            raise exc.NotFoundError from e
        
        if wait_response:
            return receive_arp(stream, arp_packet.target_ip, timeout or DEFAULT_REPLY_MISSING_TIME)
        return None  # pragma: no cover