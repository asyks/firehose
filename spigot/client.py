from __future__ import annotations

from .connection import Connection
from .message import HttpMessage
from .response import Response
from .types import MessageType


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
        self, path: str, message_type: MessageType, message_data: str, encoding: str
    ) -> Response:
        connection = self._get_connection()

        message: HttpMessage | str = message_data
        if message_type is MessageType.HTTP:
            message = HttpMessage(self.hostname, path)

        await connection.open()
        response = await connection.send(str(message).encode(encoding))
        connection.close()

        return response
