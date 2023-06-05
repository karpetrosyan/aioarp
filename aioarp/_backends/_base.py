import typing

from typing_extensions import TypeAlias
from typing_extensions import Protocol

_Address: TypeAlias = typing.Tuple[typing.Any, ...]


class SocketInterface(Protocol):

    def send(self, data: bytes) -> int: ...

    def sendall(self, data: bytes) -> None: ...

    def recv(self, bufsize: int) -> bytes: ...

    def bind(self, address: typing.Union[_Address, bytes]) -> None: ...

    def fileno(self) -> int: ...

    def settimeout(self, value: typing.Union[float, None]) -> None: ...

    def close(self) -> None: ...
