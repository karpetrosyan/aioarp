from aioarp import ArpPacket
from aioarp import EthPacket
from aioarp import HardwareType
from aioarp import Opcode
from aioarp import ProtocolType

class TestEth:

    def test_eth_parse(self):
        eth_header = (
            b"\x11\x11\x11\x11\x11\x11\x11"
            b"\x11\x11\x11\x11\x11\x08\x06"
        )

        eth_packet = EthPacket.parse(frame=eth_header)
        assert eth_packet.sender_mac == '11:11:11:11:11:11'
        assert eth_packet.target_mac == '11:11:11:11:11:11'
        assert eth_packet.proto == ProtocolType.arp

    def test_build(self):
        assert EthPacket(
            sender_mac='11:11:11:11:11:11',
            target_mac='11:11:11:11:11:11',
            proto=ProtocolType.ip
        ).build_frame() == (
                   b"\x11\x11\x11\x11\x11\x11\x11"
                   b"\x11\x11\x11\x11\x11\x08\x00"
               )


class TestArp:

    def test_parse(self):
        arp_header = (
            b"\x00\x01\x08\x00\x06\x04"
            b"\x00\x01\x11\x11\x11\x11"
            b"\x11\x11\x7f\x00\x00\x01"
            b"\x11\x11\x11\x11\x11\x11"
            b"\x7f\x00\x00\x01"
        )
        arp_packet = ArpPacket.parse(frame=arp_header)
        assert arp_packet.hardware_type == HardwareType.ethernet
        assert arp_packet.protocol_type == ProtocolType.ip
        assert arp_packet.hardware_length == 6
        assert arp_packet.protocol_length == 4
        assert arp_packet.opcode == Opcode.request
        assert arp_packet.sender_mac == '11:11:11:11:11:11'
        assert arp_packet.sender_ip == '127.0.0.1'
        assert arp_packet.target_mac == '11:11:11:11:11:11'
        assert arp_packet.target_ip == '127.0.0.1'

    def test_build(self):
        assert ArpPacket(
            hardware_type=HardwareType.ethernet,
            protocol_type=ProtocolType.ip,
            sender_mac='11:11:11:11:11:11',
            sender_ip='127.0.0.1',
            target_mac='11:11:11:11:11:11',
            target_ip='127.0.0.1',
        ).build_frame() == (
            b"\x00\x01\x08\x00\x06\x04"
            b"\x00\x01\x11\x11\x11\x11"
            b"\x11\x11\x7f\x00\x00\x01"
            b"\x11\x11\x11\x11\x11\x11"
            b"\x7f\x00\x00\x01"
        )

