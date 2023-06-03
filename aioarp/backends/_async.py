import select
import socket
import typing

import anyio
from anyio.abc import AsyncResource

from aioarp import _exceptions as exc

# TODO: add error map

class AsyncSocket(AsyncResource):

    def __init__(self,
                 interface: str):
        sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        sock.bind((interface, 0))
        self.sock = sock

    async def receive_frame(self, timeout: float) -> bytes:
        frame: typing.Optional[bytes]
        with anyio.move_on_after(timeout):
            while True:
                r, _, _ = select.select([self.sock], [], [], 0.00001)
                if r:
                    frame = self.sock.recv(1123123)
                    break
                await anyio.sleep(0)
        if not frame:
            raise exc.ReadTimeoutError()
        return frame

    async def write_frame(self, frame: bytes, timeout: float) -> None:

        with anyio.move_on_after(timeout):
            while frame:
                _, w, _ = select.select([], [self.sock], [], 0.00001)

                nsent = self.sock.send(frame)
                frame = frame[nsent:]
                await anyio.sleep(0)
        if frame:
            raise exc.WriteTimeoutError()

    async def aclose(self) -> None:
        self.sock.close()
