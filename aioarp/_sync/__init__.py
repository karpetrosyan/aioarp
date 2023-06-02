import ipaddress

from aioarp.arp import ArpPacket, EthPacket, Protocol, ETHERNET_HEADER_SIZE, ARP_HEADER_SIZE
from ..backends._sync import Socket


def send_arp(arp_packet: ArpPacket) -> ArpPacket:
    sock = Socket('enp0s3')
    ethernet_packet = EthPacket(
        target_mac=arp_packet.target_mac,
        sender_mac=arp_packet.sender_mac,
        proto=Protocol.arp
    )
    sock.write_frame(ethernet_packet.build_frame() + arp_packet.build_frame())

    while True:
        frame = sock.receive_frame()
        eth_header = frame[:ETHERNET_HEADER_SIZE]  # first 14 bytes

        try:
            eth_packet = EthPacket.parse(eth_header)
            if eth_packet.proto != Protocol.arp:
                continue

            arp_response = ArpPacket.parse(frame[ETHERNET_HEADER_SIZE: ETHERNET_HEADER_SIZE + ARP_HEADER_SIZE])  # get arp frame
            try:
                ipaddress.IPv4Address(arp_response.target_ip)
                return arp_response
            except ipaddress.AddressValueError:
                continue
        except BaseException:
            ...
