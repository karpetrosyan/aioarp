import socket
import typing

from aioarp import _exceptions as exc
from aioarp.backends._base import SocketInterface


# TODO: add error map

class Stream:

    def __init__(self,
                 interface: str,
                 sock: typing.Optional[SocketInterface] = None
                 ):
        if sock:
            self.sock = sock
        else:
            self.sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        self.sock.bind((interface, 0))

    def receive_frame(self, timeout: float) -> bytes:
        self.sock.settimeout(timeout)
        try:
            frame = self.sock.recv(1123123)
        except socket.timeout:
            raise exc.ReadTimeoutError()
        return frame

    def write_frame(self, frame: bytes, timeout: float) -> None:
        self.sock.settimeout(timeout)
        try:
            self.sock.sendall(frame)
        except socket.timeout:
            raise exc.WriteTimeoutError()

    def __enter__(self) -> 'Stream':
        return self

    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:
        self.sock.close()
