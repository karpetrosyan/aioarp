import struct
import typing
from enum import Enum

from aioarp._utils import enforce_ip
from aioarp._utils import enforce_mac
from aioarp._utils import parse_ip
from aioarp._utils import parse_mac

ETHERNET_HEADER_SIZE = 14
ARP_HEADER_SIZE = 28

__all__ = (
    'ETHERNET_HEADER_SIZE',
    'ARP_HEADER_SIZE',
    'HardwareType',
    'ProtocolType',
    'Opcode',
    'EthPacket',
    'ArpPacket',
    'size_of'
)

class HardwareType(Enum):
    ethernet = 1


class ProtocolType(Enum):
    ip = 0x0800
    arp = 0x0806


class Opcode(Enum):
    request = 1
    response = 2


class Packet:

    @classmethod
    def parse(self, frame: bytes) -> "Packet":
        raise NotImplementedError()
    
    def build_frame(self) -> bytes:
        raise NotImplementedError()

class EthPacket(Packet):
    format = "!6s6sH"

    def __init__(self,
                 target_mac: str,
                 sender_mac: str,
                 proto: ProtocolType):
        self.target_mac = target_mac
        self.sender_mac = sender_mac
        self.proto = proto

    @classmethod
    def parse(cls, frame: bytes) -> "EthPacket":
        target_mac, sender_mac, proto = struct.unpack(
            '!6s6sH',
            frame
        )
        return cls(
            target_mac=parse_mac(target_mac),
            sender_mac=parse_mac(sender_mac),
            proto=ProtocolType(proto)
        )

    def build_frame(self) -> bytes:
        return struct.pack(
            self.format,
            enforce_mac(self.target_mac),
            enforce_mac(self.sender_mac),
            self.proto.value
        )

    def __repr__(self) -> str:
        return f"<EthPacket target={self.target_mac} source={self.sender_mac} proto={self.proto.name}>"


class ArpPacket:

    def __init__(self,
                 hardware_type: HardwareType,
                 protocol_type: ProtocolType,
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
    def parse(cls, frame: bytes) -> "ArpPacket":
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
        return cls(
            hardware_type=HardwareType(hardware_type),
            protocol_type=ProtocolType(protocol_type),
            opcode=Opcode(opcode),
            sender_mac=parse_mac(sender_mac),
            sender_ip=parse_ip(sender_ip),
            target_mac=parse_mac(target_mac),
            target_ip=parse_ip(target_ip)
        )

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

    def __repr__(self) -> str:
        return f"<ArpPacket target_ip={self.target_ip}>"


def size_of(type: typing.Union[HardwareType, ProtocolType]) -> int:
    if type is ProtocolType.ip:
        return 4
    elif type is HardwareType.ethernet:
        return 6
    else:
        raise NotImplementedError()
