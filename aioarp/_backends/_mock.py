import tempfile
import typing

from typing_extensions import TypeAlias

_Address: TypeAlias = typing.Tuple[typing.Any, ...]


class MockSocket:

    def __init__(self, to_receive: bytes, delay: typing.Optional[float] = None):
        self._file = tempfile.TemporaryFile('wb+')
        self._to_receive = to_receive

    def send(self, data: bytes) -> int:
        self._file.write(data)
        return len(data)

    def sendall(self, data: bytes) -> None:
        self._file.write(data)

    def recv(self, max_bytes: typing.Optional[int] = None) -> bytes:
        return self._to_receive

    def bind(self, address: typing.Union[_Address, bytes]) -> None: ...

    def settimeout(self, value: typing.Union[float, None]) -> None: ...
    
    def fileno(self) -> int:
        return self._file.fileno()

    def close(self) -> None:
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
