from __future__ import annotations

from .constants import DEFAULT_HTTP_VERSION


class HttpMessage:
    def __init__(
        self, hostname: str, path: str, version: str = DEFAULT_HTTP_VERSION
    ) -> None:
        super().__init__()
        self.hostname = hostname
        self.path = path
        self.version = version

    def __str__(self) -> str:
        super().__init__()
        return (
            f"GET {self.path} {self.version}\r\n"
            f"Host: {self.hostname}\r\n"
            "accept: */*\r\n"
            "\r\n"
        )
