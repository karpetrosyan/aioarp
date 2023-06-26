import select
import socket
import typing

import anyio

from aioarp import _exceptions as exc

from ._base import SocketInterface

__all__ = (
    'AsyncStream',
)

class AsyncStream:

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

    async def receive_frame(self, timeout: float) -> bytes:
        frame: typing.Optional[bytes]
        with anyio.move_on_after(timeout):
            while True:
                r, _, _ = select.select([self.sock], [], [], 0.00001)
                if r:
                    frame = self.sock.recv(1123123)
                    break
                await anyio.sleep(0)  # pragma: no cover
        if not frame:   # pragma: no cover
            raise exc.ReadTimeoutError()
        return frame

    async def write_frame(self, frame: bytes, timeout: float) -> None:

        with anyio.move_on_after(timeout):
            while frame:
                _, w, _ = select.select([], [self.sock], [], 0.00001)

                nsent = self.sock.send(frame)
                frame = frame[nsent:]
                await anyio.sleep(0)
        if frame:  # pragma: no cover
            raise exc.WriteTimeoutError()

    def close(self) -> None:
        self.sock.close()

    def __enter__(self) -> "AsyncStream":  # pragma: no cover
        return self
    
    def __exit__(self) -> None:  # pragma: no cover
        self.close()

    async def __aenter__(self) -> "AsyncStream":
        return self

    async def __aexit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:
        self.close()
