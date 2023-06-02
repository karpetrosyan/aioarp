import typing
import struct
import socket
import logging
import ipaddress
from enum import Enum


ETHERNET_HEADER_SIZE = 14
ARP_HEADER_SIZE = 28

def enforce_mac(mac: str) -> bytes:
    mac_bytes = []
    for b in mac.split(':'):
        mac_bytes.append(int(b, 16))
    return bytes(mac_bytes)

def enforce_ip(ip: str) -> bytes:
    ip_bytes = []
    for b in ip.split('.'):
        ip_bytes.append(int(b))
    return bytes(ip_bytes)

def parse_mac(mac: bytes) -> str:
    mac_parts = []
    for b in mac:
        hex = f'{b:x}'
        if len(hex) == 1:
            hex = '0' + hex
        mac_parts.append(hex)
    return ':'.join(mac_parts)

def parse_ip(ip: bytes) -> str:
    ip_parts = []
    for b in ip:
        ip_parts.append(str(b))
    return '.'.join(ip_parts)

class HardwareType(Enum):
    ethernet = 1

class Protocol(Enum):
    ip = 0x0800
    arp = 0x0806

class Opcode(Enum):
    request = 1
    response = 2

class EthPacket:
    format = "!6s6sH"

    def __init__(self,
                 target_mac: str,
                 sender_mac: str,
                 proto: Protocol):
        self.target_mac = target_mac
        self.sender_mac = sender_mac
        self.proto = proto

    @classmethod
    def parse(cls, frame: bytes):
        target_mac, sender_mac, proto = struct.unpack(
            '!6s6sH',
            frame
        )
        return cls(
            target_mac=parse_mac(target_mac),
            sender_mac=parse_mac(sender_mac),
            proto=Protocol(proto)
        )


    def build_frame(self) -> bytes:
        return struct.pack(
            self.format,
            enforce_mac(self.target_mac),
            enforce_mac(self.sender_mac),
            self.proto.value
        )

    def __repr__(self):
        return f"<EthPacket target={self.target_mac} source={self.sender_mac} proto={self.proto.name}>"

class ArpPacket:

    def __init__(self,
        hardware_type: HardwareType,
        protocol_type: Protocol,
        sender_mac: str,
        sender_ip: str,
        target_mac: str,
        target_ip: str,
        opcode: Opcode = Opcode.request):
        self.hardware_type = hardware_type
        self.protocol_type = protocol_type
        self.opcode = opcode
        self.sender_mac = sender_mac
        self.sender_ip = sender_ip
        self.target_mac = target_mac
        self.target_ip = target_ip

    @property
    def hardware_length(self) -> int:
        return size_of(self.hardware_type)

    @property
    def protocol_length(self) -> int:
        return size_of(self.protocol_type)

    @classmethod
    def parse(cls, frame: bytes):
        hardware_format = '6s'
        protocol_format = '4s'
        packing_format = ''.join([
            "!"
            "H",  # hardware type
            "H",  # protocol type
            'B',  # hardware_length
            'B',  # protocol_length
            'H',  # opcode: Opcode = Opcode.request
            hardware_format,  # sender_mac
            protocol_format,  # sender_ip: int
            hardware_format,  # target_map: int
            protocol_format,  # target_ip: int
        ])

        (
            hardware_type,
            protocol_type,
            hardware_length,
            protocol_length,
            opcode,
            sender_mac,
            sender_ip,
            target_mac,
            target_ip
        ) = struct.unpack(
            packing_format,
            frame
        )
        try:
            return cls(
            hardware_type=hardware_type,
            protocol_type=protocol_type,
            opcode=Opcode(opcode),
            sender_mac=parse_mac(sender_mac),
            sender_ip=parse_ip(sender_ip),
            target_mac=parse_mac(target_mac),
            target_ip=parse_ip(target_ip)
        )
        except Exception as e:
            print('invalid', e)

    def build_frame(self) -> bytes:
        hardware_format = str(self.hardware_length) + 's'
        protocol_format = str(self.protocol_length) + 's'
        packing_format = ''.join([
            "!"
            "H",  # hardware type
            "H",  # protocol type
            'B',  # hardware_length
            'B',  # protocol_length
            'H',  # opcode: Opcode = Opcode.request
            hardware_format,  # sender_mac
            protocol_format,  # sender_ip: int
            hardware_format,  # target_map: int
            protocol_format,  # target_ip: int
        ])

        return struct.pack(
            packing_format,
            self.hardware_type.value,
            self.protocol_type.value,
            self.hardware_length,
            self.protocol_length,
            self.opcode.value,
            enforce_mac(self.sender_mac),
            enforce_ip(self.sender_ip),
            enforce_mac(self.target_mac),
            enforce_ip(self.target_ip),
        )

    def __repr__(self):
        return f"<ArpPacket target_ip={self.target_ip}>"

def size_of(type: typing.Union[HardwareType, Protocol]) -> int:
    if type is Protocol.ip:
        return 4
    elif type is HardwareType.ethernet:
        return 6
    else:
        raise Exception



async def send_arp(arp_packet: ArpPacket) -> ArpPacket:
    sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    sock.bind(('enp0s3', 0))
    ethernet_packet = EthPacket(
        target_mac=arp_packet.target_mac,
        sender_mac=arp_packet.sender_mac,
        proto=Protocol.arp
    )
    print('sending')
    sock.sendall(ethernet_packet.build_frame() + arp_packet.build_frame())
    print('sent')

    while True:
        frame = sock.recv(123123132)
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
        except BaseException as e:
            raise

packet = ArpPacket(
    hardware_type=HardwareType.ethernet,
    protocol_type=Protocol.ip,
    sender_mac="08:00:27:26:3e:1b",
    sender_ip="10.0.2.15",
    target_mac="ff:ff:ff:ff:ff:ff",
    target_ip="10.0.2.2",
)

import asyncio
arp_response = asyncio.run(send_arp(packet))
print(arp_response)


