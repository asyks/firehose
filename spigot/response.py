from __future__ import annotations

from io import BytesIO

from .constants import DEFAULT_ENCODING


class Response:
    def __init__(self, encoding: str = DEFAULT_ENCODING) -> None:
        super().__init__()
        self.stream = BytesIO(b"")
        self.encoding = encoding

    @property
    def content_bytes(self) -> bytes:
        self.stream.seek(0)

        return self.stream.read()

    @property
    def content_str(self) -> str:
        self.stream.seek(0)

        return self.stream.read().decode(self.encoding)

    def write(self, data: bytes) -> None:
        self.stream.write(data)
