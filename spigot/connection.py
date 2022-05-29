from __future__ import annotations

from asyncio import StreamReader, StreamWriter, open_connection

from .constants import DEFAULT_ENCODING
from .response import Response


class Connection:
    def __init__(self, hostname: str, port: int) -> None:
        super().__init__()
        self.hostname = hostname
        self.port = port
        self.reader: StreamReader
        self.writer: StreamWriter

    async def open(self) -> None:
        self.reader, self.writer = await open_connection(self.hostname, self.port)

    def close(self) -> None:
        self.writer.close()

    def write(self, data: bytes) -> None:
        self.writer.write(data)

    async def send(self, message: bytes, encoding: str = DEFAULT_ENCODING) -> Response:
        self.write(message)

        response = Response(encoding)
        while True:
            line = await self.reader.readline()
            if not line:
                break

            response.write(line)

        return response
