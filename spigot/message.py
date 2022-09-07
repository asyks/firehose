from __future__ import annotations
from abc import ABC

from .constants import DEFAULT_ENCODING, DEFAULT_HTTP_VERSION


class Message(ABC):
    def __init__(self, encoding: str = DEFAULT_ENCODING) -> None:
        self.encoding = encoding

    def __str__(self) -> str:
        ...

    def __bytes__(self) -> bytes:
        return str(self).encode(self.encoding)


class RawMessage(Message):
    def __init__(self, data: str, encoding: str = DEFAULT_ENCODING) -> None:
        super().__init__(encoding=encoding)
        self.data = data

    def __str__(self) -> str:
        return self.data


class HttpMessage(Message):
    def __init__(
        self,
        hostname: str,
        path: str,
        encoding: str = DEFAULT_ENCODING,
        version: str = DEFAULT_HTTP_VERSION,
    ) -> None:
        super().__init__(encoding=encoding)
        self.hostname = hostname
        self.path = path
        self.version = version

    def __str__(self) -> str:
        return (
            f"GET {self.path} {self.version}\r\n"
            f"Host: {self.hostname}\r\n"
            "accept: */*\r\n"
            "\r\n"
        )

    def __bytes__(self) -> bytes:
        return str(self).encode(self.encoding)
