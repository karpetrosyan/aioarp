
import pytest

import aioarp
from aioarp import HardwareType, Protocol, build_arp_packet


def test_invalid_ip():
    with pytest.raises(aioarp.InvalidIpError):
        aioarp.build_arp_packet('test', '10.10.10.10.10')


def test_build_packet(monkeypatch):
    packet = build_arp_packet('test', '192.168.0.85')

    assert packet.sender_mac == '11:11:11:11:11:11'
    assert packet.sender_ip == '127.0.0.1'
    assert packet.hardware_type == HardwareType.ethernet
    assert packet.protocol_type == Protocol.ip
    assert packet.target_mac == 'ff:ff:ff:ff:ff:ff'
    assert packet.target_ip == '192.168.0.85'
