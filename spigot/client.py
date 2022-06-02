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
        self.connection = Connection(self.hostname, self.port)

    async def send_message(
        self, path: str, message_type: MessageType, message_data: str, encoding: str
    ) -> Response:
        message: HttpMessage | str = message_data
        if message_type is MessageType.HTTP:
            message = HttpMessage(self.hostname, path)

        await self.connection.open()
        response = await self.connection.send(str(message).encode(encoding))
        self.connection.close()

        return response
