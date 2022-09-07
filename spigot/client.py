from __future__ import annotations

from .connection import Connection
from .message import Message
from .response import Response


class Client:
    def __init__(
        self,
        hostname: str,
        port: int,
    ) -> None:
        super().__init__()
        self.hostname = hostname
        self.port = port

    def _get_connection(self) -> Connection:
        return Connection(self.hostname, self.port)

    async def send_message(
        self,
        message: Message,
    ) -> Response:
        connection = self._get_connection()

        await connection.open()
        response = await connection.send(bytes(message))
        connection.close()

        return response
