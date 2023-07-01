
import pytest

import aioarp
from aioarp import HardwareType
from aioarp import ProtocolType
from aioarp import build_arp_packet

def test_invalid_ip():
    with pytest.raises(aioarp.InvalidIpError):
        aioarp.build_arp_packet('10.10.10.10.10', 'test')


def test_build_packet():
    packet = build_arp_packet('192.168.0.85', 'test')

    assert packet.sender_mac == '11:11:11:11:11:11'
    assert packet.sender_ip == '127.0.0.1'
    assert packet.hardware_type == HardwareType.ethernet
    assert packet.protocol_type == ProtocolType.ip
    assert packet.target_mac == 'ff:ff:ff:ff:ff:ff'
    assert packet.target_ip == '192.168.0.85'

def test_build_packet_without_interface():
    packet = build_arp_packet('192.168.0.85')

    assert packet.sender_mac == '11:11:11:11:11:11'
