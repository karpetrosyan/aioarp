import socket
import typing

from aioarp import _exceptions as exc
from aioarp.backends._base import SocketInterface

# TODO: add error map

class Stream:

    def __init__(self,
                 interface: str,
                 sock: SocketInterface
                 ):
        self.sock = sock

    def receive_frame(self, timeout: float) -> bytes:
        self.sock.settimeout(timeout)
        try:
            frame = self.sock.recv(1123123)
        except socket.timeout:  # pragma: no cover
            raise exc.ReadTimeoutError()
        return frame

    def write_frame(self, frame: bytes, timeout: float) -> None:
        self.sock.settimeout(timeout)
        try:
            self.sock.sendall(frame)
        except socket.timeout:  # pragma: no cover
            raise exc.WriteTimeoutError()

    def __enter__(self) -> 'Stream':
        return self

    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:
        self.sock.close()
