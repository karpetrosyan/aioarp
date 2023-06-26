import socket
import typing

from aioarp import _exceptions as exc
from aioarp._backends._base import SocketInterface

__all__ = (
    'Stream',
)
class Stream:

    def __init__(self,
                 interface: str,
                 sock: typing.Optional[SocketInterface] = None
                 ):
        self.sock: SocketInterface
        if not sock:  # pragma: no cover
            self.sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        else:
            self.sock = sock
        self.sock.bind((interface, 0))

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

    def close(self) -> None:
        self.sock.close()

    def __enter__(self) -> "Stream":
        return self
    
    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:
        self.close()

    async def __aenter__(self) -> "Stream":  # pragma: no cover
        return self

    async def __aexit__(self, 
                        exc_type: typing.Any, 
                        exc_val: typing.Any, 
                        exc_tb: typing.Any) -> None:  # pragma: no cover
        self.close()
