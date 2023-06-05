import tempfile
import typing


class MockSocket:

    def __init__(self, to_receive: bytes):
        self._file = tempfile.TemporaryFile('wb+')
        self._to_receive = to_receive

    def send(self, data: bytes) -> int:
        self._file.write(data)
        return 0

    def sendall(self, data: bytes) -> None:
        self._file.write(data)

    def recv(self, max_bytes: typing.Optional[int] = None) -> bytes:
        return self._to_receive

    def bind(self, address: typing.Tuple[str, int]) -> None:
        ...

    def fileno(self) -> int:
        return self._file.fileno()

    def close(self) -> None:
        self._file.close()
