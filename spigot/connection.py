from __future__ import annotations

from asyncio import StreamReader, StreamWriter, open_connection
from io import StringIO

from .constants import DEFAULT_ENCODING
from .types import Response, to_bytes


class Connection:
    def __init__(
        self, hostname: str, port: int, encoding: str = DEFAULT_ENCODING
    ) -> None:
        super().__init__()
        self.hostname = hostname
        self.port = port
        self.encoding = encoding
        self.reader: StreamReader
        self.writer: StreamWriter

    async def open(self) -> None:
        self.reader, self.writer = await open_connection(self.hostname, self.port)

    def close(self) -> None:
        self.writer.close()

    def write(self, data: str | bytes) -> None:
        self.writer.write(to_bytes(data, self.encoding))

    async def send(self, message: str | bytes) -> Response:
        self.write(message)

        response = Response(data=StringIO(''))
        while True:
            line = await self.reader.readline()
            if not line:
                break

            response.data.write(line.decode(self.encoding))

        response.data.seek(0)

        return response
