import socket


class Socket:

    def __init__(self,
                 interface: str):
        sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        sock.bind((interface, 0))
        self.sock = sock

    def receive_frame(self) -> bytes:
        return self.sock.recv(1)

    def write_frame(self, frame: bytes) -> None:
        self.sock.sendall(frame)
