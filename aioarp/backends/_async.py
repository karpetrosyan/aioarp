import socket
import anyio
import select


class AsyncSocket:

    def __init__(self,
                 interface: str):
        sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        sock.bind((interface, 0))
        self.sock = sock

    async def receive_frame(self) -> bytes:

        while True:
            r, _, _ = select.select([self.sock], [], [], 0.00001)
            if r:
                return self.sock.recv(1)
            await anyio.sleep(0)

    async def write_frame(self, frame: bytes) -> None:

        while frame:
            _, w, _ = select.select([], [self.sock], [], 0.00001)

            nsent = self.sock.send(frame)
            frame = frame[nsent:]
            await anyio.sleep(0)